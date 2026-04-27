#!/usr/bin/env python3
"""
timteam site admin v2.0 — Album-aware CMS utility
Run: python admin.py
Scans public/music/ subdirectories as albums, matches covers from public/covers/,
updates public/data/albums.json for the website.

Requirements (optional for duration reading):
  pip install mutagen
"""
import os, json, re, sys
from pathlib import Path

try:
    from mutagen import File as MutagenFile
    HAS_MUTAGEN = True
except ImportError:
    HAS_MUTAGEN = False

BASE      = Path(__file__).parent
PUBLIC    = BASE / "public"
MUSIC_DIR = PUBLIC / "music"
COVERS_DIR= PUBLIC / "covers"
DATA_DIR  = PUBLIC / "data"

for d in [MUSIC_DIR, COVERS_DIR, DATA_DIR]:
    d.mkdir(parents=True, exist_ok=True)

ALBUMS_JSON = DATA_DIR / "albums.json"
IMG_EXT  = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
AUDIO_EXT= {".mp3", ".ogg", ".wav", ".flac", ".m4a"}

# ── Album descriptions (RU/EN) — edit here or via admin ─────
ALBUM_DESCRIPTIONS = {
    "01Love": {
        "ru": "Лучшие треки по мнению автора — знак качества. Сборник самых любимых произведений из всех альбомов, отражающих вершину творчества.",
        "en": "The author's favorite tracks — a quality mark. A collection of the most beloved pieces from all albums, reflecting the peak of creativity."
    },
    "02Laboratory": {
        "ru": "Первый опыт в написании музыки. Саундтрек к короткометражному фильму про безумного учёного, конец 2021 — начало 2022.",
        "en": "First music experience. Soundtrack for a short film about a mad scientist, end of 2021 — beginning of 2022."
    },
    "03Despair": {
        "ru": "Кульминация депрессии на протяжении 2025 года — передаёт страдание тела и разума, как разрушали вредные привычки, и как сквозь тьму нашёлся выход.",
        "en": "The culmination of depression throughout 2025 — conveys the suffering of body and mind, how destructive habits took their toll, and how light was found through the darkness."
    },
    "04Noise": {
        "ru": "Четвёртый альбом, весна 2025. Об аварии на 80 км/ч — я выкарабкался и нашёл светлый путь.",
        "en": "Fourth album, spring 2025. About a crash at 80 km/h — survived and found a brighter path."
    },
    "05Hope": {
        "ru": "Третий альбом, начало 2025. Депрессия начала обретать форму — философия классических инструментов страдающего разума.",
        "en": "Third album, early 2025. Depression began taking shape — the philosophy of classical instruments of a suffering mind."
    },
    "06Lost in sound, found in the stars": {
        "ru": "Пятый альбом, середина 2025. Саундтрек к короткометражному фильму о космических войнах рас роботов.",
        "en": "Fifth album, mid 2025. Soundtrack for a short film about cosmic wars between robot races."
    },
    "07Slowed Up": {
        "ru": "Написан в лагере в 2024. Медленный и динамичный — ломает восприятие одной и той же музыки через замедленную и ускоренную версию.",
        "en": "Written at camp in 2024. Slow and dynamic — shatters the perception of the same music through slowed and sped-up versions."
    },
    "08dramatic": {
        "ru": "Второй альбом, конец 2023 — начало 2024. Написан в период тяжёлой депрессии и передаёт боль того времени.",
        "en": "Second album, end of 2023 — beginning of 2024. Written during severe depression, conveying the pain of that period."
    },
    "09Cassy": {
        "ru": "Альбом 2026 года, ещё не завершён. Посвящён игровому и аниме-проекту про эльфийку Кэсси — активно расширяется.",
        "en": "2026 album, not yet finished. Dedicated to the gaming and anime project about elf Cassy — actively expanding."
    },
    "10Ambients_01": {
        "ru": "Первые эмбиент-работы. Начало пути в жанре — атмосферные текстуры и медитативные звуковые ландшафты.",
        "en": "First ambient works. The beginning of the journey in the genre — atmospheric textures and meditative soundscapes."
    },
    "11Ambients_02": {
        "ru": "Более зрелые эмбиент-работы — второй этап. Глубже, богаче, тоньше.",
        "en": "More mature ambient works — second stage. Deeper, richer, more refined."
    },
    "12Dino game": {
        "ru": "Саундтрек к игре Dino на Python для школьного проекта, занявшего первое место по программированию.",
        "en": "Soundtrack for a Python Dino game for a school project that won first place in programming."
    },
    "13Not relised": {
        "ru": "Треки, которые хороши, но по разным причинам не вошли ни в один из альбомов. Демо, незаконченные идеи и скрытые жемчужины.",
        "en": "Tracks that are good but did not make it into any album. Demos, unfinished ideas and hidden gems."
    },
}

ALBUM_EMOJIS = {
    "01Love": "❤️", "02Laboratory": "🧪", "03Despair": "🌑",
    "04Noise": "💥", "05Hope": "🌅",
    "06Lost in sound, found in the stars": "🚀",
    "07Slowed Up": "⏱️", "08dramatic": "🎭", "09Cassy": "🧝",
    "10Ambients_01": "🌊", "11Ambients_02": "🌌",
    "12Dino game": "🦕", "13Not relised": "🎲",
}

ALBUM_TITLES = {
    "01Love":      {"ru": "Любимые",    "en": "Love"},
    "02Laboratory":{"ru": "Лаборатория","en": "Laboratory"},
    "03Despair":   {"ru": "Отчаяние",   "en": "Despair"},
    "04Noise":     {"ru": "Шум",        "en": "Noise"},
    "05Hope":      {"ru": "Надежда",    "en": "Hope"},
    "06Lost in sound, found in the stars": {"ru": "Потерян в звуке, найден в звёздах","en": "Lost in Sound, Found in the Stars"},
    "07Slowed Up": {"ru": "Замедлен и Ускорен","en": "Slowed Up"},
    "08dramatic":  {"ru": "Драматик",   "en": "Dramatic"},
    "09Cassy":     {"ru": "Кэсси",      "en": "Cassy"},
    "10Ambients_01":{"ru":"Эмбиенты 01","en": "Ambients 01"},
    "11Ambients_02":{"ru":"Эмбиенты 02","en": "Ambients 02"},
    "12Dino game": {"ru": "Дино Игра",  "en": "Dino Game"},
    "13Not relised":{"ru":"Без Релиза", "en": "Not Released"},
}

def strip_prefix(name: str) -> str:
    """Remove leading numeric index like '01', '02' etc."""
    cleaned = re.sub(r'^\d+\s*', '', name).strip()
    return cleaned if cleaned else name

def slug_to_id(folder: str) -> str:
    """Convert folder name to a clean ID for JSON."""
    no_num = re.sub(r'^\d+', '', folder).strip()
    return re.sub(r'[^a-z0-9]+', '_', no_num.lower()).strip('_') or 'album'

def get_audio_duration(path: Path) -> float | None:
    """Try to get duration of audio file in seconds."""
    if not HAS_MUTAGEN:
        return None
    try:
        f = MutagenFile(str(path))
        if f and hasattr(f, 'info') and hasattr(f.info, 'length'):
            return round(f.info.length, 2)
    except Exception:
        pass
    return None

def find_cover(folder_name: str) -> str | None:
    """Find cover image for an album by matching folder name exactly."""
    for ext in IMG_EXT:
        candidate = COVERS_DIR / (folder_name + ext)
        if candidate.exists():
            return f"/covers/{folder_name}{ext}"
    return None

def scan_albums() -> list[dict]:
    """Scan public/music/ for album subdirectories and build album data."""
    if not MUSIC_DIR.exists():
        print(f"  ⚠ music dir not found: {MUSIC_DIR}")
        return []

    # Get existing data for preserving manual edits
    existing = {}
    if ALBUMS_JSON.exists():
        try:
            old = json.loads(ALBUMS_JSON.read_text(encoding='utf-8'))
            for a in old.get('albums', []):
                existing[a['folder']] = a
        except Exception:
            pass

    album_dirs = sorted(
        [d for d in MUSIC_DIR.iterdir() if d.is_dir()],
        key=lambda d: d.name
    )

    albums = []
    total_tracks = 0
    total_duration = 0.0
    all_duration_known = True

    for album_dir in album_dirs:
        folder = album_dir.name
        album_id = slug_to_id(folder)
        display_name = strip_prefix(folder)

        # Tracks
        track_files = sorted(
            [f for f in album_dir.iterdir() if f.suffix.lower() in AUDIO_EXT],
            key=lambda f: f.name
        )

        prev_tracks = {t['file']: t for t in existing.get(folder, {}).get('tracks', [])}
        tracks = []
        album_total = 0.0
        album_dur_known = True

        for tf in track_files:
            filename = tf.name
            stem = tf.stem
            num_match = re.match(r'^(\d+)', stem)
            num = int(num_match.group(1)) if num_match else len(tracks) + 1
            title = strip_prefix(stem)
            # Capitalize first char if lowercase
            if title and title[0].islower() and not title.startswith('#'):
                title = title[0].upper() + title[1:]

            # Duration
            dur = None
            if filename in prev_tracks and prev_tracks[filename].get('duration'):
                dur = prev_tracks[filename]['duration']
            else:
                dur = get_audio_duration(tf)

            if dur:
                album_total += dur
            else:
                album_dur_known = False
                all_duration_known = False

            tracks.append({
                "num": num,
                "title": title,
                "file": filename,
                "duration": dur
            })

        total_tracks += len(tracks)
        if album_dur_known and album_total > 0:
            total_duration += album_total

        # Titles & descriptions
        title_obj = ALBUM_TITLES.get(folder, {"ru": display_name, "en": display_name})
        desc_obj  = existing.get(folder, {}).get('description') or ALBUM_DESCRIPTIONS.get(folder, {"ru": "", "en": ""})
        emoji     = existing.get(folder, {}).get('emoji') or ALBUM_EMOJIS.get(folder, '🎵')
        cover     = find_cover(folder)

        albums.append({
            "id":           album_id,
            "folder":       folder,
            "title":        title_obj,
            "emoji":        emoji,
            "cover":        cover,
            "description":  desc_obj,
            "totalDuration": round(album_total, 2) if album_dur_known and album_total > 0 else None,
            "tracks":       tracks
        })

        print(f"  📁 {folder:40s} {len(tracks):3d} tracks", end='')
        if album_dur_known and album_total > 0:
            print(f"  {int(album_total//60)}:{int(album_total%60):02d}")
        else:
            print()

    return albums, total_tracks, total_duration if all_duration_known else None

def save_json(path: Path, data: dict):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n  ✓ Saved: {path.relative_to(BASE)}")

def edit_album(albums: list[dict]) -> list[dict]:
    print("\n─── ALBUMS ──────────────────────────────────────")
    for i, a in enumerate(albums):
        print(f"  [{i:2d}] {a['folder']:40s} {len(a['tracks']):3d} tracks")
    print("\nOptions:")
    print("  e [num]  — edit album title / description")
    print("  t [num]  — edit tracks inside album")
    print("  s        — save and exit")

    while True:
        cmd = input("\n> ").strip().lower()
        if cmd == 's':
            break
        elif cmd.startswith('e '):
            try:
                idx = int(cmd[2:])
                a = albums[idx]
                print(f"\n  Editing: {a['folder']}")
                for lang in ['ru', 'en']:
                    v = input(f"  Title [{lang}] [{a['title'].get(lang,'')}]: ").strip()
                    if v: a['title'][lang] = v
                for lang in ['ru', 'en']:
                    v = input(f"  Description [{lang}] (blank = keep): ").strip()
                    if v: a['description'][lang] = v
                v = input(f"  Emoji [{a.get('emoji','🎵')}]: ").strip()
                if v: a['emoji'] = v
                print("  ✓ Updated")
            except (ValueError, IndexError):
                print("  ✗ Invalid index")

        elif cmd.startswith('t '):
            try:
                idx = int(cmd[2:])
                a = albums[idx]
                edit_tracks_in_album(a)
            except (ValueError, IndexError):
                print("  ✗ Invalid index")
    return albums

def edit_tracks_in_album(album: dict):
    tracks = album['tracks']
    print(f"\n  Tracks in {album['folder']}:")
    for i, t in enumerate(tracks):
        dur = f"{int(t['duration']//60)}:{int(t['duration']%60):02d}" if t.get('duration') else '—:——'
        print(f"    [{i:2d}] {t['num']:3d}. {t['title'][:40]:40s} {dur}")
    print("\n  e [num] — edit title | d [num] — remove | b — back")

    while True:
        cmd = input("  > ").strip().lower()
        if cmd == 'b': break
        elif cmd.startswith('e '):
            try:
                idx = int(cmd[2:])
                t = tracks[idx]
                v = input(f"    Title [{t['title']}]: ").strip()
                if v: t['title'] = v
                print("    ✓ Updated")
            except (ValueError, IndexError): print("    ✗ Invalid")
        elif cmd.startswith('d '):
            try:
                idx = int(cmd[2:])
                removed = tracks.pop(idx)
                print(f"    Removed: {removed['title']}")
            except (ValueError, IndexError): print("    ✗ Invalid")

def main():
    print("╔══════════════════════════════════════════╗")
    print("║   timteam site admin  v2.0 (albums)     ║")
    print("╚══════════════════════════════════════════╝\n")

    if not HAS_MUTAGEN:
        print("  ℹ  mutagen not installed — track durations won't be read.")
        print("     Install: pip install mutagen\n")

    print("Scanning albums...\n")
    albums, total_tracks, total_dur = scan_albums()
    print(f"\n  Found {len(albums)} albums, {total_tracks} tracks total")

    print("\nWhat to do?")
    print("  1 — Edit albums and tracks")
    print("  2 — Just scan and save")
    print("  q — Quit without saving")

    choice = input("\n> ").strip()

    if choice == '1':
        albums = edit_album(albums)
    elif choice == 'q':
        print("Quit without saving.")
        return

    # Build final JSON
    output = {
        "generated":     "auto by admin.py",
        "totalTracks":   total_tracks,
        "estimatedHours": round(total_dur / 3600, 1) if total_dur else None,
        "albums":        albums
    }
    save_json(ALBUMS_JSON, output)
    print("\n✓ Done! Restart `npm run dev` to apply changes.")

if __name__ == "__main__":
    main()
