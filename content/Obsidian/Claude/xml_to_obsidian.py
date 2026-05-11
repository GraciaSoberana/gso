#!/usr/bin/env python3
"""
xml_to_obsidian.py
Convierte libros ThML (CCEL) en formato XML a notas Obsidian.

Reglas:
  - ≤ 5 capítulos  → un solo archivo .md
  - > 5 capítulos  → carpeta con índice + un .md por capítulo
  - Autor: se busca en el Índice de Autores; si no existe, se crea en Biblioteca/Autores/
  - Related: se mapea desde el Índice de Temas Bíblicos

Uso:
  python3 xml_to_obsidian.py <archivo.xml>  [--output <carpeta>]
  python3 xml_to_obsidian.py <carpeta/>     [--output <carpeta>] [--force]
"""

import sys
import os
import re
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# RUTAS DEL VAULT
# ─────────────────────────────────────────────────────────────
VAULT          = Path("/sessions/pensive-sweet-turing/mnt/Obsidian")
AUTHORS_DIR    = VAULT / "Biblioteca" / "Autores"
AUTHOR_INDEX   = VAULT / "Claude" / "Indice de Autores.md"
TOPICS_INDEX   = VAULT / "Claude" / "Indice de temas biblicos.md"
DEFAULT_OUTPUT = VAULT / "Biblioteca" / "Libros"

# Umbral: si el libro tiene MÁS de esto capítulos → carpeta; si no → archivo único
SINGLE_FILE_THRESHOLD = 5

# ─────────────────────────────────────────────────────────────
# NORMALIZACIÓN DE AUTORES
# ─────────────────────────────────────────────────────────────
AUTHOR_NORMALIZE = {
    "Juan Bunyan":               "John Bunyan",
    "John Charles Ryle":         "J. C. Ryle",
    "Joel Beeke":                "Joel R. Beeke",
    "Benjamin Keach":            "Benjamín Keach",
    "Robert Murray McCheyne":    "Robert Murray M'Cheyne",
    "Vario":                     "Varios",
    "varios":                    "Varios",
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
    if len(name) > max_len:
        name = name[:max_len].rsplit(' ', 1)[0].strip(" .'")
    return name

def yaml_str(value: str) -> str:
    """Envuelve en comillas si el valor contiene caracteres especiales YAML."""
    if any(c in value for c in [':', '#', '[', ']', '{', '}', '&', '*', '|', '<', '>']):
        return f'"{value}"'
    return value


# ─────────────────────────────────────────────────────────────
# ÍNDICE DE AUTORES
# ─────────────────────────────────────────────────────────────

def load_known_authors() -> set:
    known = set()
    if AUTHOR_INDEX.exists():
        for line in AUTHOR_INDEX.read_text(encoding='utf-8').splitlines():
            m = re.search(r'\[\[(.+?)\]\]', line)
            if m:
                known.add(m.group(1).strip())
    if AUTHORS_DIR.exists():
        for f in AUTHORS_DIR.glob('*.md'):
            known.add(f.stem)
    return known


def create_author_note(author_name: str):
    AUTHORS_DIR.mkdir(parents=True, exist_ok=True)
    path = AUTHORS_DIR / f"{safe_filename(author_name)}.md"
    if not path.exists():
        content = "---\ntype: author\ntags:\n  - Biblioteca/Autores\n---\n"
        path.write_text(content, encoding='utf-8')
        print(f"     ✨ Autor nuevo creado: Biblioteca/Autores/{path.name}")


# ─────────────────────────────────────────────────────────────
# ÍNDICE DE TEMAS
# ─────────────────────────────────────────────────────────────

def load_topics() -> list:
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
        exact_bonus = 10 if norm_topic == norm_title or norm_topic in norm_title else 0
        matched.append((exact_bonus + hits, topic))

    matched.sort(key=lambda x: -x[0])
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
# PARSER THML
# ─────────────────────────────────────────────────────────────

# Títulos de secciones que deben omitirse
SKIP_TITLES_RE = re.compile(
    r'^(title\s*page|indexes?|table\s+of\s+contents|contents|'
    r'index\s+of\s+scripture|title\s+pages?)$',
    re.IGNORECASE
)


def is_skip_div(title: str) -> bool:
    t = title.strip() if title else ''
    return bool(SKIP_TITLES_RE.match(t))


def elem_to_md(elem, in_chapter: bool = True) -> str:
    """
    Convierte recursivamente un elemento XML ThML a texto Markdown.
    Retorna el texto resultante (sin dobles saltos de línea, eso lo hace el caller).
    """
    tag = elem.tag.lower() if elem.tag else ''
    parts = []

    def collect_text(node) -> str:
        """Extrae texto recursivo simple (para inline)."""
        text = node.text or ''
        for child in node:
            child_tag = child.tag.lower() if child.tag else ''
            if child_tag == 'b' or child_tag == 'strong':
                inner = collect_text(child)
                text += f'**{inner}**'
            elif child_tag in ('i', 'em'):
                inner = collect_text(child)
                text += f'_{inner}_'
            elif child_tag == 'a':
                text += collect_text(child)
            elif child_tag == 'scripref':
                text += collect_text(child)
            else:
                text += collect_text(child)
            text += (child.tail or '')
        return text

    # ── Párrafos normales ──
    if tag == 'p':
        # scripCom dentro de p: es el pasaje base del sermón
        sc = elem.find('scripCom')
        if sc is not None:
            passage = sc.get('passage', '').strip()
            if passage:
                return f'*{passage}*'
            return ''

        text = clean_text(collect_text(elem))
        return text if text else ''

    # ── Encabezados ──
    if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
        level = int(tag[1])
        text = clean_text(collect_text(elem))
        if text:
            return '#' * level + ' ' + text
        return ''

    # ── scripCom standalone (self-closing) ──
    if tag == 'scripcom':
        passage = elem.get('passage', '').strip()
        if passage:
            return f'*{passage}*'
        return ''

    # ── scripRef standalone ──
    if tag == 'scripref':
        text = clean_text(collect_text(elem))
        return text

    # ── br ──
    if tag == 'br':
        return ''

    # ── div2 dentro de un div1 (subsección) ──
    if tag == 'div2':
        d2_title = elem.get('title', '').strip()
        lines = []
        if d2_title and not is_skip_div(d2_title):
            lines.append(f'## {d2_title}')
            lines.append('')
        for child in elem:
            child_md = elem_to_md(child, in_chapter=True)
            if child_md:
                lines.append(child_md)
                lines.append('')
        return '\n'.join(lines).strip()

    # ── Otros (div, span, etc.) → procesar hijos ──
    for child in elem:
        child_md = elem_to_md(child, in_chapter=in_chapter)
        if child_md:
            parts.append(child_md)
    return '\n\n'.join(p for p in parts if p)


def parse_div_content(div_elem) -> list:
    """
    Extrae párrafos de un div1 o div2, devuelve lista de strings (un elemento = un párrafo/bloque).
    El primer encabezado (h1) se considera el título y se omite aquí.
    """
    paragraphs = []
    title_skipped = False

    for child in div_elem:
        tag = child.tag.lower() if child.tag else ''

        # Saltar el primer h1 (es el título del capítulo)
        if tag == 'h1' and not title_skipped:
            title_skipped = True
            continue

        # Saltar div2 "Table of Contents" / "Indexes"
        if tag == 'div2':
            d2_title = child.get('title', '').strip()
            if is_skip_div(d2_title):
                continue

        md = elem_to_md(child)
        if md and md.strip():
            paragraphs.append(md.strip())

    return paragraphs


def extract_chapters(body_elem) -> list:
    """
    Extrae los capítulos del ThML.body.
    Cada capítulo = {'title': str, 'paragraphs': [str]}

    Lógica:
    - Los div1 de nivel superior son los capítulos (o contienen div2 que son los capítulos).
    - Se omiten Title Page, Indexes, y similares.
    - Si un div1 contiene div2 significativos, se usan como capítulos.
    """
    chapters = []

    for div1 in body_elem.findall('div1'):
        d1_title = div1.get('title', '').strip()

        # Saltar páginas de título e índices
        if is_skip_div(d1_title):
            continue

        # ¿Tiene div2 significativos?
        significant_div2 = [
            d2 for d2 in div1.findall('div2')
            if not is_skip_div(d2.get('title', ''))
        ]

        if significant_div2:
            # Usar div2 como capítulos
            for div2 in significant_div2:
                d2_title = div2.get('title', '').strip()
                # Normalizar título: quitar número romano inicial si lo tiene
                paras = parse_div2_as_chapter(div2)
                if d2_title or paras:
                    chapters.append({'title': d2_title, 'paragraphs': paras})
        else:
            # El div1 es el capítulo
            paras = parse_div_content(div1)
            if d1_title or paras:
                chapters.append({'title': d1_title, 'paragraphs': paras})

    return chapters


def parse_div2_as_chapter(div2_elem) -> list:
    """
    Extrae párrafos de un div2 (cuando se usa como capítulo).
    Omite el h1/h2 inicial (título ya capturado).
    """
    paragraphs = []
    title_skipped = False

    for child in div2_elem:
        tag = child.tag.lower() if child.tag else ''

        if tag in ('h1', 'h2') and not title_skipped:
            title_skipped = True
            continue

        # Ignorar sub-sub-secciones tipo Table of Contents dentro de div2
        if tag == 'div2':
            d_title = child.get('title', '').strip()
            if is_skip_div(d_title):
                continue

        md = elem_to_md(child)
        if md and md.strip():
            paragraphs.append(md.strip())

    return paragraphs


# ─────────────────────────────────────────────────────────────
# METADATA DEL XML
# ─────────────────────────────────────────────────────────────

def parse_xml_book(xml_path: str) -> dict:
    """
    Parsea un archivo ThML XML de CCEL y devuelve:
    {
        'title': str,
        'author_raw': str,
        'author': str,     # normalizado
        'publisher': str,
        'year': str,
        'chapters': [{'title': str, 'paragraphs': [str]}]
    }
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # ── Metadatos ──
    head = root.find('ThML.head')
    dc   = head.find('.//DC') if head is not None else None

    def dc_val(tag, scheme=None):
        if dc is None:
            return ''
        for child in dc:
            if child.tag == tag:
                if scheme is None or child.get('scheme') == scheme:
                    return (child.text or '').strip()
        return ''

    title = dc_val('DC.Title') or Path(xml_path).stem

    # Autor preferido:
    #   1) DC.Creator sub=Author sin scheme, y tiene espacio → "John Flavel" (pneum.xml)
    #   2) DC.Creator sub=Author scheme=short-form, y tiene espacio → "John Flavel" / "Jonathan Edwards"
    #   3) DC.Creator sub=Author scheme=file-as → parsear "Flavel, John (1630)" → "John Flavel"
    author_raw = ''
    if dc is not None:
        # Prioridad 1: sin scheme (atributo scheme ausente), nombre con espacio
        for child in dc:
            if child.tag == 'DC.Creator' and child.get('sub') == 'Author':
                if 'scheme' not in child.attrib:
                    text = (child.text or '').strip()
                    if text and ' ' in text:
                        author_raw = text
                        break
        # Prioridad 2: short-form con espacio (nombre legible)
        if not author_raw:
            for child in dc:
                if child.tag == 'DC.Creator' and child.get('sub') == 'Author':
                    if child.get('scheme') == 'short-form':
                        text = (child.text or '').strip()
                        if text and ' ' in text:
                            author_raw = text
                            break
        # Prioridad 3: file-as → parsear "Apellido, Nombre (años)"
        if not author_raw:
            fa = dc_val('DC.Creator', 'file-as')
            if fa:
                m = re.match(r'^([\w\s\'\-]+),\s*([\w\s\.]+?)(?:\s*\(.*\))?$', fa)
                if m:
                    author_raw = m.group(2).strip() + ' ' + m.group(1).strip()
                else:
                    author_raw = fa

    author = AUTHOR_NORMALIZE.get(author_raw, author_raw)

    publisher = (dc_val('DC.Publisher') or 'CCEL').split(':')[-1].strip()
    year_raw = dc_val('DC.Date')
    year = year_raw[:4] if year_raw and year_raw[:4].isdigit() else ''

    # ── Capítulos ──
    body = root.find('ThML.body')
    chapters = []
    if body is not None:
        chapters = extract_chapters(body)

    return {
        'title':      title,
        'author_raw': author_raw,
        'author':     author,
        'publisher':  publisher,
        'year':       year,
        'chapters':   chapters,
    }


# ─────────────────────────────────────────────────────────────
# RENDERIZADO MARKDOWN
# ─────────────────────────────────────────────────────────────

def render_frontmatter(data: dict, topics: list, is_chapter: bool = False,
                       chapter_title: str = '', book_title: str = '') -> list:
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
    lines.append('  - resources/CCEL')

    if topics:
        lines.append('related:')
        for t in topics:
            lines.append(f'  - {yaml_str(f"[[{t}]]")}')

    lines.append('---')
    return lines


def render_single_file(data: dict, topics: list) -> str:
    lines = render_frontmatter(data, topics)
    lines.append('')
    lines.append(f'# {data["title"]}')
    lines.append('')
    lines.append(f'*{data["author"]}*')
    lines.append('')

    for ch in data['chapters']:
        if ch['title']:
            lines.append(f'## {ch["title"]}')
            lines.append('')
        for para in ch['paragraphs']:
            if para:
                lines.append(para)
                lines.append('')

    return '\n'.join(lines)


def render_index_file(data: dict, topics: list, chapter_titles: list) -> str:
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


def render_chapter_file(data: dict, chapter: dict, chapter_topics: list,
                         book_title: str) -> str:
    lines = render_frontmatter(data, chapter_topics, is_chapter=True,
                               chapter_title=chapter['title'], book_title=book_title)
    lines.append('')
    if chapter['title']:
        lines.append(f'# {chapter["title"]}')
        lines.append('')

    for para in chapter['paragraphs']:
        if para:
            lines.append(para)
            lines.append('')

    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# CONVERSIÓN PRINCIPAL
# ─────────────────────────────────────────────────────────────

def convert_xml(xml_path: str, output_base: Path, known_authors: set,
                topics_list: list, force: bool = False):
    print(f"\n📖 {Path(xml_path).name}")

    data = parse_xml_book(xml_path)
    title    = data['title']
    author   = data['author']
    chapters = data['chapters']

    if not chapters:
        print(f"  ⚠️  Sin contenido detectado.")
        return

    folder_name = safe_filename(title)
    single_path = output_base / f'{folder_name}.md'
    folder_path = output_base / folder_name

    if not force:
        if single_path.exists() or folder_path.exists():
            print(f"  ⏩ Ya convertido. Usa --force para sobreescribir.")
            return

    # ── Autor ──
    if author not in known_authors and author and author != '?':
        create_author_note(author)
        known_authors.add(author)
    print(f"  ✍️  Autor: {author}")

    # ── Temas ──
    ch_titles = [ch['title'] for ch in chapters]
    matched = match_topics(title, ch_titles, topics_list, max_topics=4)
    print(f"  🏷️  Temas: {', '.join(matched) if matched else '(ninguno)'}")

    # ── Formato ──
    is_long = len(chapters) > SINGLE_FILE_THRESHOLD
    print(f"  📐 Capítulos: {len(chapters)} → {'carpeta' if is_long else 'archivo único'}")

    output_base.mkdir(parents=True, exist_ok=True)

    if not is_long:
        content = render_single_file(data, matched)
        single_path.write_text(content, encoding='utf-8')
        print(f"  ✅ {folder_name}.md")
    else:
        folder_path.mkdir(parents=True, exist_ok=True)

        ch_titles_display = [
            ch['title'] if ch['title'] else f'Capítulo {i}'
            for i, ch in enumerate(chapters, 1)
        ]

        index_content = render_index_file(data, matched, ch_titles_display)
        index_path = output_base / f'{folder_name}.md'
        index_path.write_text(index_content, encoding='utf-8')
        print(f"  ✅ Índice: {folder_name}.md")

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
    args = [a for a in args if not a.startswith('--force')]

    output_dir = DEFAULT_OUTPUT
    if '--output' in args:
        idx = args.index('--output')
        if idx + 1 < len(args):
            output_dir = Path(args[idx + 1])
            args = args[:idx] + args[idx + 2:]
        else:
            args = args[:idx]

    if not args:
        print("Error: falta ruta de entrada")
        sys.exit(1)

    target = args[0]
    target_path = Path(target)

    print("🔍 Cargando índices del vault...")
    known_authors = load_known_authors()
    topics_list   = load_topics()
    print(f"   {len(known_authors)} autores conocidos | {len(topics_list)} temas bíblicos")

    if target_path.is_file() and target_path.suffix == '.xml':
        convert_xml(str(target_path), output_dir, known_authors, topics_list, force)

    elif target_path.is_dir():
        xmls = sorted(target_path.glob('*.xml'))
        if not xmls:
            print(f"No se encontraron .xml en {target_path}")
            sys.exit(1)
        print(f"📚 {len(xmls)} XMLs encontrados → salida en: {output_dir}")
        for xf in xmls:
            convert_xml(str(xf), output_dir, known_authors, topics_list, force)
        print(f"\n✨ Conversión completada.")
    else:
        print(f"Error: {target} no es un .xml o carpeta válida")
        sys.exit(1)


if __name__ == '__main__':
    main()
