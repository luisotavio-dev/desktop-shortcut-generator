#!/usr/bin/env bash
# Build a Linux x86_64 release tarball with PyInstaller.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"

VERSION="$(grep '^APP_VERSION' desktop_shortcut_generator/config/settings.py | sed -E 's/.*"([^"]+)".*/\1/')"
ARCHIVE="desktop-shortcut-generator-${VERSION}-linux-x86_64.tar.gz"

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt pyinstaller

python3 scripts/compile_translations.py
pyinstaller packaging/pyinstaller.spec --noconfirm --clean

rm -f "${ARCHIVE}"
tar -C dist -czf "${ARCHIVE}" desktop-shortcut-generator

echo "Built ${ROOT}/${ARCHIVE}"
