# timteam portfolio — SETUP GUIDE v2

## Быстрый старт (если проект уже создан)

Скопируй все файлы из этого архива поверх существующих, сохраняя структуру папок.

---

## Структура проекта

```
C:\WORKS\Portfol_Site\
├── public\
│   ├── global.css              ← СЮДА (не в src/styles!)
│   ├── data\
│   │   └── albums.json         ← генерируется admin.py
│   ├── covers\                 ← обложки альбомов
│   │   ├── 02Laboratory.jpg    ← имя = точное название папки альбома
│   │   ├── 03Despair.jpg
│   │   ├── 04Noise.jpg
│   │   ├── 05Hope.jpg
│   │   ├── 06Lost in sound, found in the stars.jpg
│   │   ├── 07Slowed Up.jpg
│   │   ├── 08dramatic.jpg
│   │   ├── 09Cassy.jpg
│   │   ├── 10Ambients_01.jpg
│   │   ├── 11Ambients_02.jpg
│   │   ├── 12Dino game.jpg
│   │   └── 13Not relised.jpg
│   └── music\
│       ├── 02Laboratory\
│       │   ├── 01Trailer.mp3
│       │   ├── 02Storm.mp3
│       │   └── ...
│       ├── 03Despair\
│       │   ├── 01music solo.mp3
│       │   └── ...
│       ├── 04Noise\
│       ├── 05Hope\
│       ├── 06Lost in sound, found in the stars\
│       ├── 07Slowed Up\
│       ├── 08dramatic\
│       ├── 09Cassy\
│       ├── 10Ambients_01\
│       ├── 11Ambients_02\
│       ├── 12Dino game\
│       └── 13Not relised\
│
├── src\
│   ├── layouts\
│   │   └── Layout.astro
│   ├── components\
│   │   └── MiniPlayer.astro
│   ├── styles\
│   │   └── global.css          ← ДУБЛИРУЙ сюда тоже (для Astro import)
│   └── pages\
│       ├── index.astro
│       ├── music.astro
│       ├── 3d.astro
│       ├── video.astro
│       ├── games.astro
│       ├── services.astro
│       └── about.astro
│
├── admin.py                    ← запускать из корня проекта
├── astro.config.mjs
├── package.json
└── tsconfig.json
```

---

## Важные правила именования файлов

### Обложки альбомов
- Хранятся в `public\covers\`
- Имя файла = **точное название папки альбома** (с числовым префиксом, без расширения)
- Поддерживаемые форматы: `.jpg`, `.jpeg`, `.png`, `.webp`
- Примеры:
  - `02Laboratory.jpg` ✓
  - `06Lost in sound, found in the stars.jpg` ✓
  - `laboratory.jpg` ✗ (не найдётся)

### Треки
- Хранятся в `public\music\{папка альбома}\`
- Имена файлов должны совпадать с тем, что указано в `albums.json`
- Числовой префикс **сохраняется** в имени файла (01, 02...)
- Примеры:
  - `01Trailer.mp3` ✓
  - `01#Cassy - HaruNeko.mp3` ✓ (символ # нормально обрабатывается)

---

## Как добавить новые треки / альбомы

```bash
# 1. Скопируй mp3 в нужную папку альбома
# 2. Скопируй обложку в public\covers\ (если новый альбом)
# 3. Запусти admin.py из корня проекта:

python admin.py

# 4. Выбери "2 — Just scan and save"
# 5. Перезапусти dev сервер:

npm run dev
```

---

## Как включить чтение длительностей треков (опционально)

```bash
pip install mutagen
# После этого admin.py будет читать длительность каждого mp3
# и сохранять её в albums.json для отображения на сайте
```

---

## Запуск

```bash
cd C:\WORKS\Portfol_Site
npm run dev
# Открыть: http://localhost:4321
```

## Деплой на GitHub Pages

```bash
# В astro.config.mjs добавь:
# site: 'https://timteam.github.io'

npm run build
# Загрузи папку dist/ на GitHub Pages
```

---

## Порядок альбомов на сайте

| # на сайте | Папка | Название | Треков |
|---|---|---|---|
| 1 | 02Laboratory | Laboratory | 9 |
| 2 | 03Despair | Despair | 9 |
| 3 | 05Hope | Hope | 8 |
| 4 | 04Noise | Noise | 4 |
| 5 | 06Lost in sound, found in the stars | Lost in Sound... | 5 |
| 6 | 07Slowed Up | Slowed Up | 6 |
| 7 | 08dramatic | Dramatic | 3 |
| 8 | 09Cassy | Cassy | 5 |
| 9 | 10Ambients_01 | Ambients 01 | 5 |
| 10 | 11Ambients_02 | Ambients 02 | 2 |
| 11 | 12Dino game | Dino Game | 3 |
| 12 | 13Not relised | Not Released | 41 |

**Итого: 12 альбомов · 100 треков · ~6 часов**

> Папка 01Love существует на диске, но на сайте не отображается (по желанию)

---

## Смена языка

Кнопка **RU | EN** в навигации переключает весь интерфейс.
Описания альбомов автоматически переключаются между русским и английским.

---

*Создано с помощью Claude Sonnet 4.6 · timteam portfolio v2*
