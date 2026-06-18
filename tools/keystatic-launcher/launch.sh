#!/usr/bin/env bash
# Запуск локальной админки Keystatic + открытие её в браузере по умолчанию.
# Скрипт сам находит корень репозитория (лежит в tools/keystatic-launcher/).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

URL="http://localhost:4321/keystatic"

# Зависимости (на случай самого первого запуска)
if [ ! -d node_modules ]; then
  echo "Устанавливаю зависимости (первый запуск, это разово)…"
  npm install
fi

# Фоновая задача: дождаться, пока сервер поднимется, и открыть браузер
(
  for _ in $(seq 1 90); do
    if curl -fs -o /dev/null "$URL" 2>/dev/null; then break; fi
    sleep 1
  done
  if command -v open >/dev/null 2>&1; then open "$URL"
  elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$URL"
  else echo "Откройте вручную в браузере: $URL"
  fi
) &

echo "Запускаю Keystatic… ($URL)"
echo "Чтобы остановить — закройте это окно или нажмите Ctrl+C."
npm run cms
