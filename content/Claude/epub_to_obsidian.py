#!/usr/bin/env python3
"""
epub_to_obsidian.py
Convierte epubs de "Portavoz de la Gracia" a notas Obsidian estructuradas.

Produce:
  - {BookTitle}.md           → índice con wikilinks a cada artículo
  - {BookTitle}/             → carpeta con un .md por artículo
      {ArticleTitle}.md

Uso:
  python3 epub_to_obsidian.py <archivo.epub>           # un solo epub
  python3 epub_to_obsidian.py <carpeta/>               # todos los epubs en carpeta
  python3 epub_to_obsidian.py <carpeta/> --force       # sobreescribir existentes
"""

import sys
import os
import re
import unicodedata
from pathlib import Path
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup, NavigableString, Tag


# ─────────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────────

def clean_text(text: str) -> str:
    """Limpia espacios y saltos de línea extra."""
    return re.sub(r'\s+', ' ', text).strip()

def safe_filename(name: str) -> str:
    """Convierte un título a nombre de archivo seguro para Obsidian."""
    # Normalizar unicode pero conservar acentos y ñ
    name = name.replace(':', ' -').replace('/', '-').replace('\\', '-')
    name = name.replace('"', '').replace("'", '').replace('?', '').replace('!', '')
    name = re.sub(r'[<>|*]', '', name)
    return name.strip(' .')

def yaml_escape(value: str) -> str:
    """Escapa un valor para el frontmatter YAML."""
    if any(c in value for c in [':', '#', '[', ']', '{', '}', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`']):
        return f'"{value}"'
    return value


# ─────────────────────────────────────────────
# PARSER DE EPUB
# ─────────────────────────────────────────────

AUTHOR_YEARS_RE = re.compile(r'^(.+?)\s*\((\d{4}[^)]*)\)\s*$')
FOOTNOTE_BACK_RE = re.compile(r'\[←(\d+)\]')
NOTE_HREF_RE = re.compile(r'back_note_(\d+)')


def parse_epub(epub_path: str) -> dict:
    """
    Parsea un epub y devuelve:
    {
        'title': str,
        'authors': [str],   # autores únicos
        'publisher': str,
        'year': str,
        'copyright': str,
        'articles': [...]
    }
    """
    book = epub.read_epub(epub_path)

    # ── Metadata ──
    def meta(tag):
        vals = book.get_metadata('DC', tag)
        return vals[0][0].strip() if vals else ''

    # Usar el nombre del archivo como título (más fiable que el metadata del epub)
    title = Path(epub_path).stem
    publisher = meta('publisher')
    date_raw = meta('date')
    year = date_raw[:4] if date_raw and date_raw[:4].isdigit() and date_raw[:4] != '0101' else ''
    rights = meta('rights')

    # ── Leer todos los documentos ──
    splits = {}
    for item in book.get_items_of_type(ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        splits[item.get_name()] = soup

    # ── Clasificar splits ──
    article_splits = []   # [(split_name, soup)]
    footnote_splits = []  # [(split_name, soup)]

    for name, soup in sorted(splits.items()):
        raw_text = soup.get_text()
        # Líneas sin colapsar (para detectar patrones por línea)
        raw_lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
        # Texto completo colapsado (para búsquedas generales)
        stripped = clean_text(raw_text)

        # Saltar portada y TOC
        if name == 'titlepage.xhtml':
            continue
        first_line = raw_lines[0] if raw_lines else ''
        if re.search(r'^(Portavoz de la Gracia|Tabla de contenido|Contenido)\b', first_line):
            # TOC o portada interior — saltar salvo que tenga notas
            if not re.search(r'[←]', stripped):
                continue

        # Detectar páginas de notas al pie
        if re.search(r'\[←\d+\]', stripped) or soup.find('dl', class_='footnote'):
            footnote_splits.append((name, soup))
            continue

        # Detectar artículos: tienen un título + autor con años en las primeras líneas
        if any(AUTHOR_YEARS_RE.match(l) for l in raw_lines[:6]):
            article_splits.append((name, soup))
            continue

        # Saltar "Recursos de Chapel Library" y similares
        if re.search(r'Recursos de Chapel|Resources of Chapel', stripped):
            continue

    # ── Parsear notas al pie ──
    # Estructura: { note_num: {'text': str, 'source_split': str} }
    all_footnotes = {}
    for fname, soup in footnote_splits:
        for dl in soup.find_all('dl', class_='footnote'):
            # Extraer número de nota
            dt = dl.find('dt')
            if not dt:
                continue
            a_back = dt.find('a')
            if not a_back:
                continue
            # El href del [←N] apunta al artículo source
            back_href = a_back.get('href', '')
            # back_href es "index_split_002.html#back_note_1"
            source_file = back_href.split('#')[0] if '#' in back_href else ''
            note_num_match = re.search(r'(\d+)', a_back.get_text())
            if not note_num_match:
                continue
            note_num = int(note_num_match.group(1))

            # Texto de la nota
            dd = dl.find('dd')
            note_text = clean_text(dd.get_text()) if dd else ''
            # Limpiar nota: quitar número inicial si está
            note_text = re.sub(r'^\[←\d+\]\s*', '', note_text)

            all_footnotes[note_num] = {
                'text': note_text,
                'source': source_file
            }

    # ── Parsear artículos ──
    articles = []
    all_authors = []

    for split_name, soup in article_splits:
        body = soup.find('body')
        if not body:
            continue

        paragraphs_html = body.find_all(['p', 'h1', 'h2', 'h3', 'blockquote'])
        if not paragraphs_html:
            continue

        # Extraer título y autor de los primeros elementos
        article_title = ''
        article_author = ''
        author_years = ''
        author_slug = ''  # nombre sin años para wikilink
        content_paragraphs = []
        header_done = False

        # Recopilar notas que pertenecen a este split
        article_footnotes = {
            num: data['text']
            for num, data in all_footnotes.items()
            if data['source'] == split_name
        }

        for elem in paragraphs_html:
            text = clean_text(elem.get_text())
            if not text:
                continue

            if not header_done:
                # Primer elemento no vacío = título
                if not article_title:
                    article_title = text
                    continue
                # Segundo = autor con años
                m = AUTHOR_YEARS_RE.match(text)
                if m:
                    article_author = m.group(1).strip()
                    author_years = m.group(2).strip()
                    author_slug = article_author
                    header_done = True
                    continue
                # Si no tiene años, puede ser autor sin fecha o parte del contenido
                if not article_author and len(text) < 60:
                    article_author = text
                    author_slug = text
                    header_done = True
                    continue
                else:
                    header_done = True

            # ── Convertir párrafo HTML a markdown ──
            para_md = html_elem_to_md(elem, split_name)
            if para_md:
                content_paragraphs.append(para_md)

        if article_author and article_author not in all_authors:
            all_authors.append(article_author)

        articles.append({
            'title': article_title,
            'author': article_author,
            'author_years': author_years,
            'author_slug': author_slug,
            'paragraphs': content_paragraphs,
            'footnotes': article_footnotes,
            'source_split': split_name,
        })

    return {
        'title': title,
        'authors': all_authors,
        'publisher': publisher,
        'year': year,
        'copyright': rights,
        'articles': articles,
    }


def html_elem_to_md(elem, split_name: str) -> str:
    """
    Convierte un elemento BeautifulSoup a markdown.
    Maneja:
      - <sup><a href="...#note_N">N</a></sup>  →  [^N]
      - <b>, <strong>                           →  **texto**
      - <i>, <em>                               →  _texto_
      - <a href="...">                          →  texto plano (links internos)
    """
    result = []

    def process_node(node):
        if isinstance(node, NavigableString):
            result.append(str(node))
            return

        tag = node.name
        if tag == 'sup':
            # Buscar referencia a nota
            a = node.find('a')
            if a:
                href = a.get('href', '')
                m = re.search(r'note_(\d+)', href)
                if m:
                    result.append(f'[^{m.group(1)}]')
                    return
            # Si no, texto plano
            result.append(node.get_text())
            return
        elif tag in ('b', 'strong'):
            inner = node.get_text()
            if inner.strip():
                result.append(f'**{inner.strip()}**')
            return
        elif tag in ('i', 'em'):
            inner = node.get_text()
            if inner.strip():
                result.append(f'_{inner.strip()}_')
            return
        elif tag == 'a':
            # Links internos → solo texto
            result.append(node.get_text())
            return
        else:
            for child in node.children:
                process_node(child)

    for child in elem.children:
        process_node(child)

    text = ''.join(result)
    text = clean_text(text)

    # Quitar número de nota inline que a veces queda pegado al texto
    # (ya fue convertido a [^n] arriba)
    return text


# ─────────────────────────────────────────────
# GENERADOR DE MARKDOWN
# ─────────────────────────────────────────────

def build_related_tags(title: str, author: str) -> list:
    """Genera tags relacionados basados en el título."""
    tags = []
    title_lower = title.lower()

    mapping = {
        'santif': '[[Santificación]]',
        'justif': '[[Justificación]]',
        'cristo': '[[Cristología]]',
        'unión': '[[Unión con Cristo]]',
        'bautis': '[[El bautismo]]',
        'iglesia': '[[Eclesiología]]',
        'oración': '[[Oración]]',
        'fe': '[[Fe]]',
        'gracia': '[[Gracia]]',
        'evangelio': '[[El Evangelio]]',
        'pecado': '[[Pecado]]',
        'arrepentim': '[[Arrepentimiento]]',
        'salvación': '[[Salvación]]',
        'espíritu': '[[Espíritu Santo]]',
        'biblia': '[[La Escritura]]',
        'escritura': '[[La Escritura]]',
        'hogar': '[[El hogar cristiano]]',
        'matrimonio': '[[Matrimonio]]',
        'maternidad': '[[Maternidad]]',
        'paternidad': '[[Paternidad]]',
        'mortif': '[[Mortificación]]',
        'resurrección': '[[Resurrección]]',
        'expiación': '[[Expiación]]',
        'depravación': '[[Depravación]]',
        'adoración': '[[Adoración]]',
        'avivamiento': '[[Avivamiento]]',
    }
    for key, tag in mapping.items():
        if key in title_lower:
            tags.append(tag)

    return tags if tags else ['[[Vida cristiana]]']


def render_index(data: dict, output_dir: Path) -> str:
    """Genera el contenido del archivo índice."""
    title = data['title']
    authors = data['authors']
    publisher = data['publisher'] or 'Chapel Library'
    year = data['year']
    copyright_text = data['copyright']

    author_display = 'Varios' if len(authors) > 1 else (authors[0] if authors else 'Desconocido')

    lines = ['---']
    lines.append('type: journal')
    lines.append(f'title: {yaml_escape(title)}')
    lines.append(f'author: {author_display}')
    lines.append(f'publisher: "[[{publisher}]]"')
    if year:
        lines.append(f'year: {year}')
    lines.append('tags:')
    lines.append('  - resources/Chapel')
    lines.append('link: https://www.chapellibrary.org/spanish')
    lines.append('related:')
    # Related tags genéricos del título
    for tag in build_related_tags(title, author_display):
        lines.append(f'  - {yaml_escape(tag)}')
    if copyright_text:
        lines.append(f'copyright: {yaml_escape(copyright_text)}')
    lines.append('---')
    lines.append('')
    lines.append('')

    # Lista de artículos como wikilinks
    folder_name = safe_filename(title)
    for article in data['articles']:
        art_title = article['title']
        art_file = safe_filename(art_title)
        lines.append(f'- [[{folder_name}/{art_file}|{art_title}]]')

    lines.append('')
    return '\n'.join(lines)


def render_article(article: dict, book_title: str, book_publisher: str) -> str:
    """Genera el contenido markdown de un artículo."""
    title = article['title']
    author = article['author']
    author_years = article['author_years']
    paragraphs = article['paragraphs']
    footnotes = article['footnotes']

    # Frontmatter
    lines = ['---']
    lines.append('type: article')
    lines.append(f'title: {yaml_escape(title)}')

    # Autor con wikilink entre comillas (requerido para YAML válido con corchetes)
    if author:
        lines.append(f'author: "[[{author}]]"')

    lines.append(f'parent: "[[{book_title}]]"')
    lines.append(f'journal: "[[Portavoz de la gracia]]"')

    # Related tags
    related = build_related_tags(title, author)
    if f'[[{book_title}]]' not in related:
        related.insert(0, f'[[{book_title}]]')
    lines.append('related:')
    for tag in related:
        lines.append(f'  - {yaml_escape(tag)}')

    lines.append('---')
    lines.append('')

    # Título y autor como cabecera (igual que en las notas existentes)
    lines.append(title)
    lines.append('')
    if author_years:
        lines.append(f'{author} ({author_years})')
    elif author:
        lines.append(author)
    lines.append('')

    # Cuerpo — incluye "Tomado de...", separador y bio tal como vienen del epub
    for para in paragraphs:
        if para:
            lines.append(para)
            lines.append('')

    # Notas al pie
    if footnotes:
        for num in sorted(footnotes.keys()):
            note_text = footnotes[num]
            lines.append(f'[^{num}]: {note_text}')

    return '\n'.join(lines)


# ─────────────────────────────────────────────
# ESCRITURA DE ARCHIVOS
# ─────────────────────────────────────────────

def convert_epub(epub_path: str, output_base: Path, force: bool = False):
    """Convierte un epub en notas Obsidian."""
    print(f"\n📖 Procesando: {Path(epub_path).name}")

    data = parse_epub(epub_path)
    title = data['title']
    folder_name = safe_filename(title)

    index_path = output_base / f'{folder_name}.md'
    folder_path = output_base / folder_name

    # Verificar si ya existe
    if not force and folder_path.exists():
        print(f"  ⏩ Ya convertido ({folder_name}/). Usa --force para sobreescribir.")
        return

    if not data['articles']:
        print(f"  ⚠️  No se encontraron artículos en {Path(epub_path).name}")
        return

    # Crear carpeta
    folder_path.mkdir(parents=True, exist_ok=True)

    # Escribir índice
    index_content = render_index(data, folder_path)
    index_path.write_text(index_content, encoding='utf-8')
    print(f"  ✅ Índice: {index_path.name}")

    # Escribir artículos
    for article in data['articles']:
        art_filename = safe_filename(article['title']) + '.md'
        art_path = folder_path / art_filename
        art_content = render_article(article, title, data['publisher'])
        art_path.write_text(art_content, encoding='utf-8')
        print(f"     → {art_filename}")

    print(f"  📁 {len(data['articles'])} artículos generados")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    force = '--force' in args
    args = [a for a in args if not a.startswith('--')]
    target = args[0]
    target_path = Path(target)

    if target_path.is_file() and target_path.suffix == '.epub':
        output_base = target_path.parent
        convert_epub(str(target_path), output_base, force=force)

    elif target_path.is_dir():
        epubs = sorted(target_path.glob('*.epub'))
        if not epubs:
            print(f"No se encontraron archivos .epub en {target_path}")
            sys.exit(1)
        print(f"Encontrados {len(epubs)} archivos epub")
        for epub_file in epubs:
            convert_epub(str(epub_file), target_path, force=force)
        print(f"\n✨ Conversión completada.")
    else:
        print(f"Error: {target} no es un epub o carpeta válida")
        sys.exit(1)


if __name__ == '__main__':
    main()
