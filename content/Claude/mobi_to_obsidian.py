#!/usr/bin/env python3
"""
mobi_to_obsidian.py
Convierte archivos .mobi a notas Obsidian.

Lógica:
  - Detecta capítulos por párrafos en negrita que sirven como títulos de sección
  - ≤ 5 capítulos → archivo único
  - > 5 capítulos → carpeta con índice + un .md por capítulo
  - Autor: se busca en el Índice de Autores; si no existe, se crea en Biblioteca/Autores/
  - Related: se mapea desde el Índice de Temas Bíblicos

Uso:
  python3 mobi_to_obsidian.py <archivo.mobi>  [--output <carpeta>]
  python3 mobi_to_obsidian.py <carpeta/>      [--output <carpeta>] [--force]
"""

import sys
import os
import re
import mobi as mobi_lib
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

# ─────────────────────────────────────────────────────────────
# RUTAS DEL VAULT
# ─────────────────────────────────────────────────────────────
VAULT          = Path("/sessions/pensive-sweet-turing/mnt/Obsidian")
AUTHORS_DIR    = VAULT / "Biblioteca" / "Autores"
AUTHOR_INDEX   = VAULT / "Claude" / "Indice de Autores.md"
TOPICS_INDEX   = VAULT / "Claude" / "Indice de temas biblicos.md"
DEFAULT_OUTPUT = VAULT / "Biblioteca" / "Libros"

SINGLE_FILE_THRESHOLD = 5

AUTHOR_NORMALIZE = {
    "Juan Bunyan":              "John Bunyan",
    "John Charles Ryle":        "J. C. Ryle",
    "Joel Beeke":               "Joel R. Beeke",
    "Benjamin Keach":           "Benjamín Keach",
    "Robert Murray McCheyne":   "Robert Murray M'Cheyne",
    "Vario":                    "Varios",
    "varios":                   "Varios",
}

# Patrones que marcan un capítulo principal (negrita corta y reconocible)
CHAPTER_HEADING_RE = re.compile(
    r'^('
    r'[IVXivx]+\.'              # Números romanos: I. II. III.
    r'|[IVXivx]+\.\s+\w'       # I. THE WORD / I. Preface etc.
    r'|PREFACE|INTRODUCTION|CONCLUSION|APPENDIX'
    r'|The\s+(First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth)\s+Principle'
    r'|The\s+(First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth)\s+Principle\s+Expounded'
    r'|The\s+Exposition'
    r'|SUMMARY'
    r')',
    re.IGNORECASE
)

# Patrones a ignorar como capítulos (portada, TOC, créditos, etc.)
SKIP_HEADING_RE = re.compile(
    r'^('
    r'CONTENTS|TABLE OF CONTENTS|INDEX'
    r'|Soli\s+Deo|To God alone'
    r')',
    re.IGNORECASE
)


# ─────────────────────────────────────────────────────────────
# UTILIDADES (copiadas del chapel script)
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
    if any(c in value for c in [':', '#', '[', ']', '{', '}', '&', '*', '|', '<', '>']):
        return f'"{value}"'
    return value


# ─────────────────────────────────────────────────────────────
# AUTORES Y TEMAS
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
# PARSER MOBI
# ─────────────────────────────────────────────────────────────

def is_chapter_heading(para) -> bool:
    """Devuelve True si este <p> es un título de capítulo (negrita + texto corto + patrón)."""
    if not (para.find('b') or para.find('strong')):
        return False
    text = clean_text(para.get_text())
    if not text or len(text) > 120:
        return False
    if SKIP_HEADING_RE.match(text):
        return False
    return bool(CHAPTER_HEADING_RE.match(text))

def para_to_md(para) -> str:
    """Convierte un <p> a texto Markdown."""
    result = []

    def process(node):
        if isinstance(node, NavigableString):
            result.append(str(node))
            return
        tag = node.name
        if tag in ('b', 'strong'):
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

    for child in para.children:
        process(child)

    return clean_text(''.join(result))


def parse_mobi_book(mobi_path: str) -> dict:
    """
    Extrae título, autor y capítulos de un archivo .mobi.
    Retorna dict compatible con las funciones de renderizado.
    """
    tempdir, _ = mobi_lib.extract(mobi_path)
    temp = Path(tempdir)

    # ── Metadatos desde content.opf ──
    opf_path = temp / "mobi7" / "content.opf"
    title = Path(mobi_path).stem
    author_raw = ''

    if opf_path.exists():
        try:
            tree = ET.parse(opf_path)
            ns = {
                'dc': 'http://purl.org/dc/elements/1.1/',
                'opf': 'http://www.idpf.org/2007/opf',
            }
            root = tree.getroot()
            t = root.find('.//dc:title', ns)
            c = root.find('.//dc:creator', ns)
            if t is not None and t.text:
                title = t.text.strip()
            if c is not None and c.text:
                author_raw = c.text.strip()
        except Exception:
            pass

    author = AUTHOR_NORMALIZE.get(author_raw, author_raw)

    # ── Parsear HTML ──
    html_path = temp / "mobi7" / "book.html"
    soup = BeautifulSoup(html_path.read_text(encoding='utf-8'), 'html.parser')
    paras = soup.find_all('p')

    # ── Detectar capítulos ──
    # Un capítulo = heading bold + todo el contenido hasta el siguiente heading
    chapters = []
    current_title = None
    current_paras = []
    preamble_done = False  # Saltar portada/índice al inicio

    for p in paras:
        text = clean_text(p.get_text())
        if not text:
            continue

        if is_chapter_heading(p):
            # Guardar capítulo anterior
            if current_title is not None and current_paras:
                chapters.append({'title': current_title, 'paragraphs': current_paras})
            elif current_paras and preamble_done:
                # Contenido sin título (preamble que llegó después del inicio)
                chapters.append({'title': '', 'paragraphs': current_paras})

            current_title = clean_text(p.get_text())
            current_paras = []
            preamble_done = True
        else:
            # Saltar portada y tabla de contenido (antes del primer capítulo)
            if not preamble_done:
                # Detectar si es la TOC (lista de capítulos)
                if re.match(r'^(CONTENTS|TABLE OF CONTENTS)', text, re.IGNORECASE):
                    continue
                # Saltar título del libro, nombre del autor, año de publicación
                if len(chapters) == 0 and current_title is None:
                    # Solo agregar si ya pasamos de la sección de portada
                    if re.match(r'^(PREFACE|INTRODUCTION|The\s+\w+\s+Principle)', text, re.IGNORECASE):
                        preamble_done = True
                    else:
                        continue

            if current_title is not None:
                md = para_to_md(p)
                if md:
                    current_paras.append(md)

    # Último capítulo
    if current_title is not None and current_paras:
        chapters.append({'title': current_title, 'paragraphs': current_paras})

    return {
        'title':      title,
        'author_raw': author_raw,
        'author':     author,
        'publisher':  'Banner of Truth',
        'year':       '',
        'chapters':   chapters,
    }


# ─────────────────────────────────────────────────────────────
# RENDERIZADO (reutiliza la misma lógica que chapel script)
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
    lines.append('  - resources/Puritans')
    if topics:
        lines.append('related:')
        for t in topics:
            lines.append(f'  - {yaml_str(f"[[{t}]]")}')
    lines.append('---')
    return lines

def render_single_file(data: dict, topics: list) -> str:
    lines = render_frontmatter(data, topics)
    lines += ['', f'# {data["title"]}', '', f'*{data["author"]}*', '']
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
    lines += ['', '']
    folder = safe_filename(data['title'])
    for i, ch_title in enumerate(chapter_titles, 1):
        safe_ch = safe_filename(ch_title) if ch_title else f'Capítulo {i}'
        display = ch_title if ch_title else f'Capítulo {i}'
        lines.append(f'- [[{folder}/{safe_ch}|{display}]]')
    lines.append('')
    return '\n'.join(lines)

def render_chapter_file(data: dict, chapter: dict, ch_topics: list, book_title: str) -> str:
    lines = render_frontmatter(data, ch_topics, is_chapter=True,
                               chapter_title=chapter['title'], book_title=book_title)
    lines += ['']
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

def convert_mobi(mobi_path: str, output_base: Path, known_authors: set,
                 topics_list: list, force: bool = False):
    print(f"\n📖 {Path(mobi_path).name}")

    data = parse_mobi_book(mobi_path)
    title    = data['title']
    author   = data['author']
    chapters = data['chapters']

    if not chapters:
        print(f"  ⚠️  Sin contenido detectado.")
        return

    folder_name = safe_filename(title)
    single_path = output_base / f'{folder_name}.md'
    folder_path = output_base / folder_name

    if not force and (single_path.exists() or folder_path.exists()):
        print(f"  ⏩ Ya convertido. Usa --force para sobreescribir.")
        return

    if author not in known_authors and author and author != '?':
        create_author_note(author)
        known_authors.add(author)
    print(f"  ✍️  Autor: {author}")

    ch_titles = [ch['title'] for ch in chapters]
    matched = match_topics(title, ch_titles, topics_list, max_topics=4)
    print(f"  🏷️  Temas: {', '.join(matched) if matched else '(ninguno)'}")

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
        index_path = output_base / f'{folder_name}.md'
        index_path.write_text(render_index_file(data, matched, ch_titles_display), encoding='utf-8')
        print(f"  ✅ Índice: {folder_name}.md")
        for i, ch in enumerate(chapters, 1):
            ch_title = ch['title'] if ch['title'] else f'Capítulo {i}'
            ch_topics = match_topics(ch_title, [], topics_list, max_topics=3)
            ch_filename = safe_filename(ch_title) + '.md'
            (folder_path / ch_filename).write_text(
                render_chapter_file(data, ch, ch_topics, title), encoding='utf-8')
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
    args = [a for a in args if a != '--force']

    output_dir = DEFAULT_OUTPUT
    if '--output' in args:
        idx = args.index('--output')
        if idx + 1 < len(args):
            output_dir = Path(args[idx + 1])
            args = args[:idx] + args[idx + 2:]
        else:
            args = args[:idx]

    target = Path(args[0])

    print("🔍 Cargando índices del vault...")
    known_authors = load_known_authors()
    topics_list   = load_topics()
    print(f"   {len(known_authors)} autores conocidos | {len(topics_list)} temas bíblicos")

    if target.is_file() and target.suffix == '.mobi':
        convert_mobi(str(target), output_dir, known_authors, topics_list, force)
    elif target.is_dir():
        mobis = sorted(set(target.glob('*.mobi')))
        # Deduplicar por nombre base (sin " (1)")
        seen_titles = {}
        for m in mobis:
            base = re.sub(r'\s*\(\d+\)$', '', m.stem).strip()
            if base not in seen_titles:
                seen_titles[base] = m
        unique_mobis = sorted(seen_titles.values())
        print(f"📚 {len(unique_mobis)} mobis únicos → salida en: {output_dir}")
        for m in unique_mobis:
            convert_mobi(str(m), output_dir, known_authors, topics_list, force)
        print(f"\n✨ Conversión completada.")
    else:
        print(f"Error: {target} no es un .mobi o carpeta válida")
        sys.exit(1)

if __name__ == '__main__':
    main()
