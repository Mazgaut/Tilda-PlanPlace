#!/usr/bin/env bash
# Создаёт ярлык на рабочем столе (macOS или Linux), который запускает Keystatic.
# Запустить один раз: bash tools/keystatic-launcher/install-shortcut.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
LAUNCH="$SCRIPT_DIR/launch.sh"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
chmod +x "$LAUNCH"

# Папка рабочего стола (учитываем локализованные имена через xdg-user-dir)
DESKTOP="$(xdg-user-dir DESKTOP 2>/dev/null || true)"
[ -n "${DESKTOP:-}" ] && [ -d "$DESKTOP" ] || DESKTOP="$HOME/Desktop"
mkdir -p "$DESKTOP"

case "$(uname -s)" in
  Darwin)
    SHORTCUT="$DESKTOP/Запустить Keystatic.command"
    cat > "$SHORTCUT" <<EOF
#!/usr/bin/env bash
exec "$LAUNCH"
EOF
    chmod +x "$SHORTCUT"
    ;;
  *)
    SHORTCUT="$DESKTOP/planplace-keystatic.desktop"
    cat > "$SHORTCUT" <<EOF
[Desktop Entry]
Type=Application
Name=PlanPlace · Keystatic
Comment=Запустить локальную админку Keystatic и открыть в браузере
Exec=bash "$LAUNCH"
Path=$REPO_ROOT
Terminal=true
Icon=text-editor
Categories=Development;
EOF
    chmod +x "$SHORTCUT"
    gio set "$SHORTCUT" metadata::trusted true 2>/dev/null || true
    # Дублируем в меню приложений
    APPS="$HOME/.local/share/applications"
    mkdir -p "$APPS" && cp "$SHORTCUT" "$APPS/planplace-keystatic.desktop" 2>/dev/null || true
    ;;
esac

echo "Готово. Ярлык на рабочем столе: \"$SHORTCUT\""
echo "Дважды кликните по нему — поднимется Keystatic и откроется браузер."
