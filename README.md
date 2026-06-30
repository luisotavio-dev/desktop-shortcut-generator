# Desktop Shortcut Generator

A **Python** and **PyQt6** desktop app for creating `.desktop` shortcuts on Linux through a simple graphical interface with multi-language support.

Works on environments that follow the [FreeDesktop.org](https://specifications.freedesktop.org/) standard — **KDE Plasma**, **GNOME**, **XFCE**, **Cinnamon**, **MATE**, and derivatives (Fedora, Ubuntu, Bazzite, Arch, Linux Mint, etc.).

## Features

- Graphical interface for creating `.desktop` shortcuts
- Fields: name, executable, icon (with live preview), description, and *Run in Terminal*
- Path validation before saving
- Automatic desktop folder detection via **XDG** (`user-dirs.dirs`)
- Fallback to `~/.local/share/applications` when no desktop folder is available
- Trusted launcher support on **GNOME** (`metadata::trusted`)
- Internationalization: **Portuguese (Brazil)**, **English**, and **Spanish**
- System language detection with English fallback

## Requirements

| Requirement | Minimum version |
|-------------|-----------------|
| Python | 3.11+ |
| PyQt6 | 6.4+ |
| gettext (`msgfmt`) | only needed to compile translations |

### Install system dependencies

**Fedora / Bazzite / RHEL:**

```bash
sudo dnf install python3 python3-pip gettext
```

**Ubuntu / Debian / Mint:**

```bash
sudo apt install python3 python3-pip python3-venv gettext
```

**Arch Linux:**

```bash
sudo pacman -S python python-pip gettext
```

## How to run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USER/desktop-shortcut-generator.git
cd desktop-shortcut-generator
```

Replace `YOUR_USER` with the actual GitHub user or organization once the repository is published.

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Compile translations

```bash
python scripts/compile_translations.py
```

### 5. Run the application

```bash
python -m desktop_shortcut_generator.main
```

Fill in the form, select the executable and icon image, then click **Create Shortcut**. The `.desktop` file will be saved to your desktop (if available) or to the applications menu directory.

## Project structure

```text
desktop_shortcut_generator/
├── config/           # Global settings (name, version, languages)
├── domain/           # Pure business entities and rules
├── use_cases/        # Use cases (orchestration)
├── infrastructure/   # I/O: file writing, XDG paths, GNOME trust
├── presentation/     # PyQt6 user interface
├── i18n/             # gettext translations (.po / .mo)
└── main.py           # Entry point

scripts/
└── compile_translations.py
```

The project follows **Clean Architecture**: business logic does not depend on PyQt6.

## How to contribute

Contributions are welcome — bug fixes, improvements, translations, and documentation.

### 1. Fork and branch

```bash
git clone https://github.com/YOUR_USER/desktop-shortcut-generator.git
cd desktop-shortcut-generator
git checkout -b my-feature
```

### 2. Set up the development environment

Follow the steps in [How to run](#how-to-run).

### 3. Make your changes

- Follow **PEP 8** and use **type hints** in new code
- Keep layer separation (`domain` must not import PyQt6)
- Add docstrings to public classes and functions
- If you change UI strings, update **all** `.po` files under `i18n/locales/`

### 4. Compile translations (if needed)

```bash
python scripts/compile_translations.py
```

### 5. Test locally

```bash
python -m desktop_shortcut_generator.main
```

Verify that shortcuts are created correctly and the interface is properly translated.

### 6. Commit and open a Pull Request

```bash
git add .
git commit -m "feat: clear description of the change"
git push origin my-feature
```

Open a **Pull Request** on GitHub describing what you changed and how to test it.

### Contribution ideas

- New languages in `i18n/locales/`
- UI accessibility improvements
- Flatpak / Flathub packaging
- Automated tests
- Desktop environment compatibility fixes

## Adding a new language

1. Copy `desktop_shortcut_generator/i18n/locales/en/LC_MESSAGES/messages.po` to `locales/<code>/LC_MESSAGES/messages.po`
2. Translate all `msgstr` entries and set the `Language:` header
3. Register the language in `config/settings.py` → `SUPPORTED_LANGUAGES`
4. Run `python scripts/compile_translations.py`

## License

License not yet defined. Check the repository for updates.
