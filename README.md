# Desktop Shortcut Generator

<p align="center">
  <img src="desktop_shortcut_generator/assets/app-icon-readme.png" alt="Desktop Shortcut Generator logo" width="128" height="128">
</p>

[![Built with AI](https://img.shields.io/badge/Built%20with-AI-8B5CF6?style=for-the-badge&logo=openai&logoColor=white)](https://github.com/luisotavio-dev/desktop-shortcut-generator)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.4+-41CD52?style=flat-square&logo=qt&logoColor=white)](https://www.riverbankcomputing.com/software/pyqt/)
[![Platform](https://img.shields.io/badge/Platform-Linux-FCC624?style=flat-square&logo=linux&logoColor=black)](https://www.kernel.org/)
[![FreeDesktop](https://img.shields.io/badge/Standard-FreeDesktop.org-0069DA?style=flat-square)](https://specifications.freedesktop.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

A **Python** + **PyQt6** desktop application for creating `.desktop` shortcuts on Linux through a simple graphical interface with multi-language support.

Compatible with **KDE Plasma**, **GNOME**, **XFCE**, **Cinnamon**, **MATE**, and other FreeDesktop-compliant environments (Fedora, Ubuntu, Bazzite, Arch, Linux Mint, and more).

> [!WARNING]
> **This project is no longer actively maintained.**
>
> After evaluating similar tools, [Launcher Studio](https://github.com/MrArnaudMichel/launcher_studio) already covers this use case more completely (create/edit `.desktop` files, validation, icon picker, Flathub packaging, and more). Development effort has moved to **contributing there** instead of continuing this repository.
>
> This codebase remains available for reference and learning. For a maintained alternative, use [Launcher Studio on Flathub](https://flathub.org/apps/fr.arnaudmichel.launcherstudio) or its [GitHub repository](https://github.com/MrArnaudMichel/launcher_studio).

---

## AI disclosure

> **This project was built with the assistance of AI (Large Language Models).**
>
> The initial architecture, codebase, documentation, and several iterations of features were generated and refined through AI-assisted development (e.g. Cursor / Claude). Human review and manual testing were applied along the way, but **contributors should treat the codebase accordingly**:
>
> - Review logic, security, and edge cases carefully before merging changes
> - Prefer tests for non-trivial behavior when adding features
> - Report or fix anything that looks auto-generated but incorrect
> - Improvements, refactors, and human-written replacements are encouraged

If you contribute, you do **not** need to use AI — but please be aware of the project's origins.

---

## Table of contents

- [Features](#features)
- [Requirements](#requirements)
- [Quick start](#quick-start)
- [Usage](#usage)
- [Project structure](#project-structure)
- [Contributing](#contributing)
- [Adding a new language](#adding-a-new-language)
- [License](#license)

---

## Features

| Feature | Description |
|---------|-------------|
| **GUI shortcut builder** | Create `.desktop` files without editing them by hand |
| **Form fields** | App name, executable, icon (with preview), description, *Run in Terminal* |
| **Validation** | Checks that executable and icon paths exist before saving |
| **XDG desktop detection** | Reads `~/.config/user-dirs.dirs` for the correct Desktop folder |
| **Smart fallback** | Saves to `~/.local/share/applications` when no Desktop exists |
| **GNOME trust** | Marks desktop shortcuts as trusted via `gio` when applicable |
| **i18n** | Portuguese (Brazil), English, and Spanish |
| **Locale detection** | Uses the system language with English fallback |

---

## Requirements

| Requirement | Minimum |
|-------------|---------|
| Python | 3.11+ |
| PyQt6 | 6.4+ |
| gettext (`msgfmt`) | Only for compiling translations |

<details>
<summary><strong>Install system packages by distribution</strong></summary>

**Fedora / Bazzite / RHEL**

```bash
sudo dnf install python3 python3-pip gettext
```

**Ubuntu / Debian / Mint**

```bash
sudo apt install python3 python3-pip python3-venv gettext
```

**Arch Linux**

```bash
sudo pacman -S python python-pip gettext
```

</details>

---

## Quick start

```bash
# 1. Clone
git clone https://github.com/luisotavio-dev/desktop-shortcut-generator.git
cd desktop-shortcut-generator

# 2. Virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# 3. Dependencies
pip install -r requirements.txt

# 4. Compile translations
python scripts/compile_translations.py

# 5. Run
python -m desktop_shortcut_generator.main
```

---

## Usage

1. Launch the application.
2. Fill in the **application name**, **executable path**, **shortcut icon path**, and optional **description**.
3. Enable **Run in Terminal** if the program must run inside a terminal.
4. Click **Create Shortcut**.

The `.desktop` file is saved to:

1. Your XDG desktop folder (e.g. `~/Desktop`, `~/Área de Trabalho`)
2. Or `~/.local/share/applications` if no desktop folder is found

---

## Project structure

```text
desktop_shortcut_generator/
├── config/           # App name, version, supported languages
├── domain/           # Entities, validation rules (no PyQt6)
├── use_cases/        # Application workflows
├── infrastructure/   # File I/O, XDG paths, GNOME trust
├── presentation/     # PyQt6 UI
├── i18n/             # gettext .po / .mo files
└── main.py           # Entry point & dependency injection

scripts/
└── compile_translations.py
```

The codebase follows **Clean Architecture** — business rules are decoupled from the UI layer.

---

## Contributing

Contributions are welcome. Feel free to open issues, suggest improvements, or submit pull requests.

### Workflow

1. **Fork** the repository on GitHub
2. **Clone** your fork and create a branch:
   ```bash
   git clone https://github.com/<your-user>/desktop-shortcut-generator.git
   cd desktop-shortcut-generator
   git checkout -b my-feature
   ```
3. **Set up** the dev environment ([Quick start](#quick-start))
4. **Make changes** following the guidelines below
5. **Test** locally:
   ```bash
   python -m desktop_shortcut_generator.main
   ```
6. **Commit** with a clear message and open a **Pull Request**

### Guidelines

- Follow **PEP 8** and use **type hints**
- Keep layers separated — `domain` must not import PyQt6
- Add docstrings to public classes and functions
- Update **all** `.po` files when changing UI strings
- Run `python scripts/compile_translations.py` after editing translations
- Mention in your PR if you used AI assistance for that change

### Ideas for contributors

- [ ] New language translations
- [ ] Automated tests
- [ ] UI accessibility improvements
- [ ] Desktop environment compatibility fixes
- [ ] Replace or harden AI-generated sections where needed

---

## Adding a new language

1. Copy `desktop_shortcut_generator/i18n/locales/en/LC_MESSAGES/messages.po` to `locales/<code>/LC_MESSAGES/messages.po`
2. Translate every `msgstr` and update the `Language:` header
3. Register the locale in `config/settings.py` → `SUPPORTED_LANGUAGES`
4. Compile: `python scripts/compile_translations.py`

---

## CI/CD (GitHub Actions)

Pushes to `main` trigger [`.github/workflows/release.yml`](.github/workflows/release.yml), which:

1. **Reads `APP_VERSION`** from `desktop_shortcut_generator/config/settings.py`
2. **Creates a GitHub release** only when the tag `v<APP_VERSION>` does not exist yet

> **Important:** A new release is **not** created on every commit — only when you **bump `APP_VERSION`** (for example from `1.0.0` to `1.0.1`) and push to `main`.

### Publish a new release

```bash
# 1. Bump the version
#    desktop_shortcut_generator/config/settings.py  -> APP_VERSION
#    desktop_shortcut_generator/__init__.py       -> __version__

git add desktop_shortcut_generator/config/settings.py desktop_shortcut_generator/__init__.py
git commit -m "chore: bump version to 1.0.1"
git push origin main
```

GitHub Actions will create the tag and publish the release on GitHub.

### Manual release trigger

You can also run the workflow manually from the GitHub **Actions** tab (`workflow_dispatch`).

---

## License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  <sub>Built with AI-assisted development · Maintainers and contributors welcome</sub>
</p>
