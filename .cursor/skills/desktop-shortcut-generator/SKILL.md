---
name: desktop-shortcut-generator
description: >-
  Develop and maintain the Desktop Shortcut Generator Python/PyQt6 app for
  creating Linux .desktop shortcuts. Use when working on this project,
  adding features, fixing bugs, extending i18n, or modifying Clean Architecture
  layers (domain, use_cases, infrastructure, presentation).
---

# Desktop Shortcut Generator

Specialist guidance for the **Desktop Shortcut Generator** project — a PyQt6 desktop app that creates FreeDesktop.org `.desktop` shortcuts on Linux.

## Architecture (mandatory)

Follow **Clean Architecture** with strict layer separation. Business logic must never import PyQt6.

```
desktop_shortcut_generator/
├── i18n/              # gettext translations (pt_BR, en, es)
├── config/settings.py # APP_NAME, APP_VERSION, DEFAULT_ICON, paths
├── domain/            # entities.py, exceptions.py — pure Python
├── use_cases/         # create_shortcut.py — orchestration
├── infrastructure/    # file_writer.py — disk I/O, chmod
├── presentation/      # main_window.py, components.py — PyQt6 only
└── main.py            # composition root / dependency injection
```

### Layer rules

| Layer | May depend on | Must NOT depend on |
|-------|---------------|-------------------|
| `domain` | stdlib only | PyQt6, infrastructure, presentation |
| `use_cases` | domain | PyQt6, presentation |
| `infrastructure` | domain, config | PyQt6, presentation |
| `presentation` | use_cases, domain, i18n, config | — (UI only) |
| `main.py` | all layers | — (wires dependencies) |

## Key behaviors

- **Shortcut entity** (`domain/entities.py`): validates name, executable path (must exist, be a file), icon path (must exist, be a file).
- **`.desktop` output**: FreeDesktop.org format with `[Desktop Entry]`, `Type=Application`, `Name`, `Comment`, `Exec`, `Icon`, `Terminal`, `Categories`.
- **Save location priority**: `XDG_DESKTOP_DIR` from `~/.config/user-dirs.dirs` → common localized desktop folder names → `$XDG_DATA_HOME/applications` (default `~/.local/share/applications`).
- **Permissions**: `chmod +x` applied after write (`infrastructure/file_writer.py`).
- **GNOME trust**: when saving to the desktop, runs `gio set … metadata::trusted true` if `gio` is available (`infrastructure/desktop_trust.py`).
- **i18n**: gettext with English msgids; locales in `i18n/locales/{pt_BR,en,es}/LC_MESSAGES/`. UI strings use `_()` from `desktop_shortcut_generator.i18n`.

## Development workflow

### Run the app

```bash
cd /var/home/lpereira/Developer/OtherProjects/desktop-shortcut-generator
pip install -r requirements.txt
python scripts/compile_translations.py   # after editing .po files
python -m desktop_shortcut_generator.main
```

### Add a new language

1. Copy `i18n/locales/en/LC_MESSAGES/messages.po` to `i18n/locales/<code>/LC_MESSAGES/messages.po`.
2. Translate all `msgstr` entries; set `Language:` header.
3. Register in `config/settings.py` → `SUPPORTED_LANGUAGES`.
4. Run `python scripts/compile_translations.py`.
5. Add translatable strings to all locale `.po` files when adding new UI text.

### Add a new UI string

1. Use English as msgid: `_("My new label")` in presentation layer.
2. Add `msgid`/`msgstr` to **all** `.po` files (en, pt_BR, es).
3. Recompile translations.
4. Call `retranslate_ui()` if the string is set outside the existing retranslate flow.

### Add a feature

1. Domain changes first (entity validation, new exceptions).
2. Use case orchestrates domain + infrastructure.
3. Infrastructure handles I/O only.
4. Presentation collects input and displays errors via `QMessageBox`.
5. Wire new dependencies in `main.py`.

## Code standards

- Python **3.11+**, full **type hints**, **PEP 8**, Google-style **docstrings** on public classes/methods.
- Validation errors: raise `ValidationError(field, message)` with English message keys translatable in `main_window.py`.
- File errors: raise `FileWriteError` from infrastructure; show user-friendly message in UI.
- Config: read `APP_NAME`, `APP_VERSION`, `DEFAULT_ICON` from `config/settings.py`.

## Flatpak considerations

- Keep paths relative to `BASE_DIR` in settings.
- App icon at `desktop_shortcut_generator/assets/app-icon.png` (referenced by `DEFAULT_ICON`).
- No hardcoded user paths outside `Path.home()` for shortcut output.
- Translations ship as compiled `.mo` files inside the package.

## Common tasks

| Task | Files to touch |
|------|----------------|
| New form field | `entities.py`, `main_window.py`, all `.po` files |
| Change save logic | `file_writer.py`, `config/settings.py` |
| New validation rule | `entities.py`, `exceptions.py`, `.po` error messages |
| Language switcher | `i18n/translator.py`, `main_window._on_language_changed` |

## Additional resources

- For full original requirements, see [reference.md](reference.md)
