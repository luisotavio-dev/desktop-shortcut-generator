# Project Reference

Condensed requirements from the project specification.

## Functional requirements

1. **i18n**: Portuguese (Brazil), English, Spanish via gettext.
2. **GUI (PyQt6)**: Application Name, Executable Path (file picker), Icon Path (image picker), Description, Run in Terminal checkbox, Language selector.
3. **Shortcut generation**: field validation, FreeDesktop.org `.desktop` content, smart save to Desktop/Área de Trabalho/applications, `chmod +x`.
4. **Config**: centralized `config/settings.py` with app name, version, default icon.

## Technical requirements

- Type hints everywhere
- PEP 8
- Docstrings (Google/Sphinx style)
- Robust exception handling in infrastructure
- Executable path existence validated in domain entity

## .desktop format example

```ini
[Desktop Entry]
Type=Application
Name=My Application
Comment=A helpful description
Exec=/usr/bin/my-app
Icon=/usr/share/icons/my-app.png
Terminal=false
Categories=Utility;
```

## Dependencies

- PyQt6 >= 6.4.0
- gettext (stdlib) + gettext tools (`msgfmt`) for compiling translations
