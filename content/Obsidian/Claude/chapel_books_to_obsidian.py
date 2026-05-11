#!/usr/bin/env python3
"""
chapel_books_to_obsidian.py
Convierte libros de Chapel Library (epub) a notas Obsidian.

Reglas:
  - ≤ 5 capítulos  → un solo archivo .md
  - > 5 capítulos  → carpeta con índice + un .md por capítulo
  - Autor: se busca en el Índice de Autores; si no existe, se crea en Biblioteca/Autores/
  - Related: se mapea desde el Índice de Temas Bíblicos

Uso:
  python3 chapel_books_to_obsidian.py <archivo.epub>  [--output <carpeta>]
  python3 chapel_books_to_obsidian.py <carpeta/>      [--output <carpeta>] [--force]
"""

import sys
import os
import re
from pathlib import Path
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup, NavigableString

# ─────────────────────────────────────────────────────────────
# RUTAS DEL VAULT
# ─────────────────────────────────────────────────────────────
VAULT = Path("/sessions/pensive-sweet-turing/mnt/Obsidian")
AUTHORS_DIR    = VAULT / "Biblioteca" / "Autores"
AUTHOR_INDEX   = VAULT / "Claude" / "Indice de Autores.md"
TOPICS_INDEX   = VAULT / "Claude" / "Indice de temas biblicos.md"
DEFAULT_OUTPUT = VAULT / "Biblioteca" / "Libros"

# Umbral: si el libro tiene MÁS de esto capítulos → carpeta; si no → archivo único
SINGLE_FILE_THRESHOLD = 5

# ─────────────────────────────────────────────────────────────
# NORMALIZACIÓN DE NOMBRES DE AUTORES
# (metadato del epub → nombre canónico en el vault)
# ─────────────────────────────────────────────────────────────
AUTHOR_NORMALIZE = {
    "Juan Bunyan":          "John Bunyan",
    "John Charles Ryle":    "J. C. Ryle",
    "Joel Beeke":           "Joel R. Beeke",
    "Benjamin Keach":       "Benjamín Keach",
    "Robert Murray McCheyne": "Robert Murray M'Cheyne",
    "Vario":                "Varios",
    "varios":               "Varios",
}


# ─────────────────────────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────────────────────────

def clean_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()

def safe_filename(name: str, max_len: int = 80) -> str:
    name = name.replace(':', ' -').replace('/', '-').replace('\\', '-')
    name = name.replace('"', '').replace('?', '').replace('!', '')
    name = re.sub(r'[<>|*]', '', name)
    name = name.strip(" .'")
    # Truncar a max_len caracteres sin cortar palabras a la mitad
    if len(name) > max_len:
        name = name[:max_len].rsplit(' ', 1)[0].strip(" .'")
    return name

def yaml_str(value: str) -> str:
    """Envuelve en comillas si el valor tiene caracteres especiales YAML."""
    if any(c in value for c in [':', '#', '[', ']', '{', '}', '&', '*', '|', '<', '>']):
        return f'"{value}"'
    return value


# ─────────────────────────────────────────────────────────────
# CARGA DE ÍNDICE DE AUTORES
# ─────────────────────────────────────────────────────────────

def load_known_authors() -> set:
    """Carga todos los autores conocidos del índice + los archivos existentes en Autores/."""
    known = set()
    # Del índice md
    if AUTHOR_INDEX.exists():
        for line in AUTHOR_INDEX.read_text(encoding='utf-8').splitlines():
            m = re.search(r'\[\[(.+?)\]\]', line)
            if m:
                known.add(m.group(1).strip())
    # De los archivos .md en Biblioteca/Autores/
    if AUTHORS_DIR.exists():
        for f in AUTHORS_DIR.glob('*.md'):
            known.add(f.stem)
    return known


def create_author_note(author_name: str):
    """Crea un archivo de autor nuevo en Biblioteca/Autores/ si no existe."""
    AUTHORS_DIR.mkdir(parents=True, exist_ok=True)
    path = AUTHORS_DIR / f"{safe_filename(author_name)}.md"
    if not path.exists():
        content = "---\ntype: author\ntags:\n  - Biblioteca/Autores\n---\n"
        path.write_text(content, encoding='utf-8')
        print(f"     ✨ Autor nuevo creado: Biblioteca/Autores/{path.name}")
    return author_name


# ─────────────────────────────────────────────────────────────
# CARGA DE TEMAS BÍBLICOS
# ─────────────────────────────────────────────────────────────

def load_topics() -> list:
    """Carga la lista de temas bíblicos del índice."""
    topics = []
    seen = set()
    if not TOPICS_INDEX.exists():
        return topics
    for line in TOPICS_INDEX.read_text(encoding='utf-8').splitlines():
        m = re.search(r'\[\[(.+?)\]\]', line)
        if m:
            raw = m.group(1).strip()
            topic = raw.split('/')[-1]
            if topic not in seen:
                seen.add(topic)
                topics.append(topic)
    return topics


def match_topics(title: str, chapter_titles: list, topics: list, max_topics: int = 4) -> list:
    """
    Busca temas relevantes usando el título del libro y los títulos de capítulos.
    Prioriza: 1) coincidencia exacta con el título, 2) más palabras coincidentes.
    """
    import unicodedata

    def norm(s):
        return ''.join(c for c in unicodedata.normalize('NFD', s.lower())
                       if unicodedata.category(c) != 'Mn')

    norm_title  = norm(title)
    search_text = norm(title + ' ' + ' '.join(chapter_titles))
    matched = []

    for topic in topics:
        norm_topic = norm(topic)
        words = [w for w in re.split(r'\s+', norm_topic) if len(w) >= 4]
        if not words:
            continue
        hits = sum(1 for w in words if w in search_text)
        if hits < max(1, len(words) // 2):
            continue
        # Bonus si el tema coincide directamente con el título del libro
        exact_bonus = 10 if norm_topic == norm_title or norm_topic in norm_title else 0
        matched.append((exact_bonus + hits, topic))

    matched.sort(key=lambda x: -x[0])
    # Deduplicar manteniendo orden
    seen = set()
    result = []
    for _, t in matched:
        if t not in seen:
            seen.add(t)
            result.append(t)
        if len(result) >= max_topics:
            break
    return result


# ─────────────────────────────────────────────────────────────
# PARSER DE EPUB
# ─────────────────────────────────────────────────────────────

FOOTNOTE_RE = re.compile(r'\[←\d+\]')
CHAPTER_NUM_RE = re.compile(r'^(\d+[\.\:\-]\s+|Capítulo\s+\d+[\:\-\s])', re.IGNORECASE)

def is_skip_split(name: str, soup: BeautifulSoup, raw_lines: list, stripped: str) -> bool:
    """Retorna True si este split debe ignorarse (portada, TOC, copyright, recursos)."""
    if name == 'titlepage.xhtml':
        return True
    first = raw_lines[0] if raw_lines else ''
    # TOC / tabla de contenido
    if re.match(r'^(Contenido|Índice|Tabla de contenido|Index)\s*$', first, re.IGNORECASE):
        return True
    # Portada interior (título del libro solo, sin contenido)
    # Excepto si es un encabezado de sección reconocible (DIRECTION, CHAPTER, etc.)
    if len(raw_lines) <= 3 and not re.search(r'\[←', stripped):
        if not re.search(r'\b(DIRECTION|CHAPTER|SERMON|LECTURE)\s+[IVXLCDM\d]+', stripped, re.IGNORECASE):
            return True
    # Copyright / aviso legal / créditos de traducción
    # Detectar por primera línea o por contenido predominante
    if re.match(r'^(copyright|traducido|publicado originalmente|este folleto|este librito|este libro fue|impreso en)', first, re.IGNORECASE):
        return True
    if len(raw_lines) <= 6 and re.search(r'(traducido|copyright|chapel library|publicado originalmente|dominio público)', stripped, re.IGNORECASE):
        return True
    # Recursos de Chapel Library
    if re.search(r'Recursos de Chapel|Resources of Chapel', stripped, re.IGNORECASE):
        return True
    # Google Books / Internet Archive attribution pages
    if re.match(r'^About this Book', first, re.IGNORECASE):
        return True
    if re.match(r'^This book made available by the Internet Archive', first, re.IGNORECASE):
        return True
    return False

def clean_ocr_title(title: str) -> str:
    """Limpia errores OCR comunes en títulos de libros escaneados (Google Books, IA)."""
    # 1) Corregir primero los números romanos mal reconocidos
    title = re.sub(r'\bIH\b', 'III', title)       # IH → III
    title = re.sub(r'\bTill\b', 'VIII', title)     # Till → VIII (OCR de VIII)
    title = re.sub(r'\bVIIL\b', 'VIII', title)     # VIIL → VIII
    title = re.sub(r'\bVI1\b', 'VII', title)        # VI1 → VII
    # 2) Si el título contiene "DIRECTION/CHAPTER/SERMON", extraer solo esa parte
    m_dir = re.search(r'((?:DIRECTION|CHAPTER|SERMON|LECTURE)\s+[IVXLCDM]+\.?)', title, re.IGNORECASE)
    if m_dir:
        return m_dir.group(1).rstrip('.') + '.'
    # 3) Quitar basura inicial antes de la primera letra mayúscula real
    title = re.sub(r"^[^A-Za-z]+(?=[A-Z])", '', title)
    # 4) Limpiar puntuación doble/extra al final
    title = re.sub(r'[,\.]+$', '.', title)
    title = re.sub(r'\.\s*\.\s*\.', '', title)
    return title.strip()

def is_footnote_split(soup: BeautifulSoup, stripped: str) -> bool:
    return bool(FOOTNOTE_RE.search(stripped)) or bool(soup.find('dl', class_='footnote'))

def html_to_md(elem) -> str:
    """Convierte un elemento HTML a texto Markdown limpio."""
    result = []

    def process(node):
        if isinstance(node, NavigableString):
            result.append(str(node))
            return
        tag = node.name
        if tag == 'sup':
            a = node.find('a')
            if a:
                href = a.get('href', '')
                m = re.search(r'note_(\d+)', href)
                if m:
                    result.append(f'[^{m.group(1)}]')
                    return
            result.append(node.get_text())
            return
        elif tag in ('b', 'strong'):
            inner = node.get_text().strip()
            if inner:
                result.append(f'**{inner}**')
            return
        elif tag in ('i', 'em'):
            inner = node.get_text().strip()
            if inner:
                result.append(f'_{inner}_')
            return
        elif tag == 'a':
            result.append(node.get_text())
            return
        for child in node.children:
            process(child)

    for child in elem.children:
        process(child)

    return clean_text(''.join(result))


def parse_epub_book(epub_path: str) -> dict:
    """
    Parsea un epub de libro y devuelve:
    {
        'title': str,
        'author_raw': str,        # como está en el epub
        'author': str,            # normalizado
        'publisher': str,
        'year': str,
        'chapters': [
            {'title': str, 'paragraphs': [str], 'footnotes': {int: str}}
        ]
    }
    """
    book = epub.read_epub(epub_path)

    def meta(tag):
        vals = book.get_metadata('DC', tag)
        return vals[0][0].strip() if vals else ''

    title = Path(epub_path).stem
    # Limpiar caracteres especiales en el título del epub (el filename puede tener _)
    title = title.replace('_', ' ').replace('  ', ' ').strip()
    author_raw = meta('creator') or '?'
    author = AUTHOR_NORMALIZE.get(author_raw, author_raw)
    publisher = meta('publisher') or 'Chapel Library'
    date_raw = meta('date')
    year = date_raw[:4] if date_raw and date_raw[:4].isdigit() and date_raw[:4] != '0101' else ''

    # ── Leer todos los splits ──
    all_splits = {}
    for item in book.get_items_of_type(ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        all_splits[item.get_name()] = soup

    # ── Clasificar splits ──
    content_splits = []   # [(name, soup)]
    footnote_splits = []  # [(name, soup)]

    for name, soup in sorted(all_splits.items()):
        raw_text = soup.get_text()
        raw_lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
        stripped = clean_text(raw_text)

        if is_footnote_split(soup, stripped):
            footnote_splits.append((name, soup))
            continue
        if is_skip_split(name, soup, raw_lines, stripped):
            continue
        if raw_lines:
            content_splits.append((name, soup))

    # ── Parsear notas al pie ──
    all_footnotes = {}  # {note_num: {'text': str, 'source': str}}
    for fname, soup in footnote_splits:
        for dl in soup.find_all('dl', class_='footnote'):
            dt = dl.find('dt')
            if not dt:
                continue
            a_back = dt.find('a')
            if not a_back:
                continue
            back_href = a_back.get('href', '')
            source_file = back_href.split('#')[0] if '#' in back_href else ''
            note_num_m = re.search(r'(\d+)', a_back.get_text())
            if not note_num_m:
                continue
            note_num = int(note_num_m.group(1))
            dd = dl.find('dd')
            note_text = clean_text(dd.get_text()) if dd else ''
            note_text = re.sub(r'^\[←\d+\]\s*', '', note_text)
            all_footnotes[note_num] = {'text': note_text, 'source': source_file}

    # ── Parsear capítulos ──
    chapters = []

    for split_name, soup in content_splits:
        body = soup.find('body')
        if not body:
            continue
        elems = body.find_all(['p', 'h1', 'h2', 'h3', 'blockquote'])
        raw_lines_split = [l.strip() for l in soup.get_text().split('\n') if l.strip()]

        # Notas de este split
        chapter_footnotes = {
            num: data['text']
            for num, data in all_footnotes.items()
            if data['source'] == split_name
        }

        # Título del capítulo: primer elemento con texto (limpiar notas al pie pegadas)
        chapter_title = raw_lines_split[0] if raw_lines_split else ''
        chapter_title = re.sub(r'\d+$', '', chapter_title).strip()  # quitar número final (ref. de nota)
        chapter_title = clean_ocr_title(chapter_title)

        # Párrafos de contenido
        paragraphs = []
        first_done = False
        for elem in elems:
            text_md = html_to_md(elem)
            if not text_md:
                continue
            # Saltar el título (ya lo capturamos)
            if not first_done and text_md == chapter_title:
                first_done = True
                continue
            first_done = True
            paragraphs.append(text_md)

        if chapter_title or paragraphs:
            chapters.append({
                'title': chapter_title,
                'paragraphs': paragraphs,
                'footnotes': chapter_footnotes,
                'source_split': split_name,
            })

    return {
        'title': title,
        'author_raw': author_raw,
        'author': author,
        'publisher': publisher,
        'year': year,
        'chapters': chapters,
    }


# ─────────────────────────────────────────────────────────────
# RENDERIZADO MARKDOWN
# ─────────────────────────────────────────────────────────────

def render_frontmatter(data: dict, topics: list, is_chapter: bool = False,
                        chapter_title: str = '', book_title: str = '') -> list:
    """Genera el frontmatter YAML como lista de líneas."""
    lines = ['---']
    lines.append(f"type: {'chapter' if is_chapter else 'book'}")

    fm_title = chapter_title if is_chapter else data['title']
    lines.append(f'title: {yaml_str(fm_title)}')
    lines.append(f'author: "[[{data["author"]}]]"')

    if is_chapter:
        lines.append(f'parent: "[[{book_title}]]"')

    lines.append(f'publisher: "[[{data["publisher"]}]]"')
    if data.get('year'):
        lines.append(f'year: {data["year"]}')
    lines.append('tags:')
    lines.append('  - resources/Chapel')
    lines.append('link: https://www.chapellibrary.org/spanish')

    if topics:
        lines.append('related:')
        for t in topics:
            lines.append(f'  - {yaml_str(f"[[{t}]]")}')

    lines.append('---')
    return lines


def render_single_file(data: dict, topics: list) -> str:
    """Genera un único archivo .md para libros cortos."""
    lines = render_frontmatter(data, topics)
    lines.append('')
    lines.append(f'# {data["title"]}')
    lines.append('')
    lines.append(f'*{data["author"]}*')
    lines.append('')

    # Recopilar todas las notas al pie
    all_footnotes = {}
    for ch in data['chapters']:
        all_footnotes.update(ch['footnotes'])

    for ch in data['chapters']:
        if ch['title']:
            lines.append(f'## {ch["title"]}')
            lines.append('')
        for para in ch['paragraphs']:
            if para:
                lines.append(para)
                lines.append('')

    if all_footnotes:
        for num in sorted(all_footnotes.keys()):
            lines.append(f'[^{num}]: {all_footnotes[num]}')

    return '\n'.join(lines)


def render_index_file(data: dict, topics: list, chapter_titles: list) -> str:
    """Genera el archivo índice para libros largos."""
    lines = render_frontmatter(data, topics)
    lines.append('')
    lines.append('')

    folder = safe_filename(data['title'])
    for i, ch_title in enumerate(chapter_titles, 1):
        safe_ch = safe_filename(ch_title) if ch_title else f'Capítulo {i}'
        display = ch_title if ch_title else f'Capítulo {i}'
        lines.append(f'- [[{folder}/{safe_ch}|{display}]]')

    lines.append('')
    return '\n'.join(lines)


def render_chapter_file(data: dict, chapter: dict, chapter_topics: list, book_title: str) -> str:
    """Genera el archivo .md de un capítulo individual."""
    lines = render_frontmatter(data, chapter_topics, is_chapter=True,
                               chapter_title=chapter['title'], book_title=book_title)
    lines.append('')
    lines.append(chapter['title'])
    lines.append('')

    for para in chapter['paragraphs']:
        if para:
            lines.append(para)
            lines.append('')

    if chapter['footnotes']:
        for num in sorted(chapter['footnotes'].keys()):
            lines.append(f'[^{num}]: {chapter["footnotes"][num]}')

    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# CONVERSIÓN PRINCIPAL
# ─────────────────────────────────────────────────────────────

def convert_epub(epub_path: str, output_base: Path, known_authors: set,
                 topics_list: list, force: bool = False):
    """Convierte un epub de libro a notas Obsidian."""
    print(f"\n📖 {Path(epub_path).name}")

    data = parse_epub_book(epub_path)
    title = data['title']
    author = data['author']
    chapters = data['chapters']

    if not chapters:
        print(f"  ⚠️  Sin contenido detectado.")
        return

    folder_name = safe_filename(title)
    single_path = output_base / f'{folder_name}.md'
    folder_path = output_base / folder_name

    # Verificar si ya existe
    if not force:
        if single_path.exists() or folder_path.exists():
            print(f"  ⏩ Ya convertido. Usa --force para sobreescribir.")
            return

    # ── Autor: verificar / crear ──
    if author not in known_authors and author != '?':
        create_author_note(author)
        known_authors.add(author)  # evitar duplicar en misma sesión
    print(f"  ✍️  Autor: {author}")

    # ── Temas relacionados ──
    ch_titles = [ch['title'] for ch in chapters]
    matched = match_topics(title, ch_titles, topics_list, max_topics=4)
    print(f"  🏷️  Temas: {', '.join(matched) if matched else '(ninguno)'}")

    # ── Decidir formato ──
    is_long = len(chapters) > SINGLE_FILE_THRESHOLD
    print(f"  📐 Capítulos: {len(chapters)} → {'carpeta' if is_long else 'archivo único'}")

    output_base.mkdir(parents=True, exist_ok=True)

    if not is_long:
        # ── ARCHIVO ÚNICO ──
        content = render_single_file(data, matched)
        single_path.write_text(content, encoding='utf-8')
        print(f"  ✅ {folder_name}.md")

    else:
        # ── CARPETA + CAPÍTULOS ──
        folder_path.mkdir(parents=True, exist_ok=True)

        ch_titles_display = []
        for i, ch in enumerate(chapters, 1):
            ch_title = ch['title'] if ch['title'] else f'Capítulo {i}'
            ch_titles_display.append(ch_title)

        # Índice
        index_content = render_index_file(data, matched, ch_titles_display)
        index_path = output_base / f'{folder_name}.md'
        index_path.write_text(index_content, encoding='utf-8')
        print(f"  ✅ Índice: {folder_name}.md")

        # Capítulos
        for i, ch in enumerate(chapters, 1):
            ch_title = ch['title'] if ch['title'] else f'Capítulo {i}'
            ch_topics = match_topics(ch_title, [], topics_list, max_topics=3)
            ch_content = render_chapter_file(data, ch, ch_topics, title)
            ch_filename = safe_filename(ch_title) + '.md'
            ch_path = folder_path / ch_filename
            ch_path.write_text(ch_content, encoding='utf-8')
            print(f"     → {ch_filename}")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    force = '--force' in args
    args = [a for a in args if not a.startswith('--')]

    # Parsear --output
    output_dir = DEFAULT_OUTPUT
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_dir = Path(sys.argv[idx + 1])
    args = [a for a in args if a != sys.argv[sys.argv.index('--output') + 1] if '--output' in sys.argv] if '--output' in sys.argv else args

    target = args[0]
    target_path = Path(target)

    # Cargar datos del vault
    print("🔍 Cargando índices del vault...")
    known_authors = load_known_authors()
    topics_list = load_topics()
    print(f"   {len(known_authors)} autores conocidos | {len(topics_list)} temas bíblicos")

    if target_path.is_file() and target_path.suffix == '.epub':
        convert_epub(str(target_path), output_dir, known_authors, topics_list, force)

    elif target_path.is_dir():
        epubs = sorted(target_path.glob('*.epub'))
        if not epubs:
            print(f"No se encontraron .epub en {target_path}")
            sys.exit(1)
        print(f"📚 {len(epubs)} epubs encontrados → salida en: {output_dir}")
        for ep in epubs:
            convert_epub(str(ep), output_dir, known_authors, topics_list, force)
        print(f"\n✨ Conversión completada.")
    else:
        print(f"Error: {target} no es un epub o carpeta válida")
        sys.exit(1)


if __name__ == '__main__':
    main()
