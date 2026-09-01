#!/usr/bin/env bash
set -eo pipefail

cd "$(dirname "$0")"
PROJECT_ROOT="$(pwd)"

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "HATA: macOS .app paketi bir Mac üzerinde oluşturulmalıdır."
  exit 1
fi

PYTHON_BIN="${PYTHON_BIN:-python3}"
"$PYTHON_BIN" -m pip install --upgrade pip
"$PYTHON_BIN" -m pip install -r requirements.txt
"$PYTHON_BIN" -m pip install pyinstaller

rm -rf build/macos "dist/GermanCourseAI.app"
mkdir -p build/macos

ICON_ARGS=()
if command -v sips >/dev/null && command -v iconutil >/dev/null && [[ -f assets/app-final.png ]]; then
  ICONSET="build/macos/GermanCourseAI.iconset"
  mkdir -p "$ICONSET"
  for size in 16 32 128 256 512; do
    sips -z "$size" "$size" assets/app-final.png --out "$ICONSET/icon_${size}x${size}.png" >/dev/null
    double=$((size * 2))
    sips -z "$double" "$double" assets/app-final.png --out "$ICONSET/icon_${size}x${size}@2x.png" >/dev/null
  done
  iconutil -c icns "$ICONSET" -o build/macos/GermanCourseAI.icns
  ICON_ARGS=(--icon "$PROJECT_ROOT/build/macos/GermanCourseAI.icns")
fi

DATA_ARGS=()
for dir in assets Resources grammar; do
  [[ -d "$dir" ]] && DATA_ARGS+=(--add-data "$PROJECT_ROOT/$dir:$dir")
done

"$PYTHON_BIN" -m PyInstaller --noconfirm --clean --onedir --windowed \
  --workpath build/macos/pyinstaller --specpath build/macos \
  --name "GermanCourseAI" \
  --osx-bundle-identifier "com.germancourseai.desktop" \
  "${ICON_ARGS[@]}" "${DATA_ARGS[@]}" \
  --hidden-import pypdf \
  "$PROJECT_ROOT/German_Course_AI.pyw"

APP_PATH="dist/GermanCourseAI.app"
[[ -d "$APP_PATH" ]] || { echo "HATA: $APP_PATH oluşturulamadı."; exit 1; }

ditto -c -k --keepParent "$APP_PATH" "dist/GermanCourseAI-macOS.zip"
echo "Tamamlandı: $APP_PATH"
echo "Dağıtım ZIP'i: dist/GermanCourseAI-macOS.zip"
