# Ярлык запуска Keystatic (локальная админка)

Один двойной клик по ярлыку на рабочем столе:

1. поднимает локальный сервер с админкой Keystatic (`npm run cms`);
2. ждёт, пока он стартует, и открывает `http://localhost:4321/keystatic` в браузере по умолчанию.

Скрипты сами находят корень репозитория, поэтому репозиторий можно держать в любой папке. При первом запуске, если нет `node_modules`, зависимости поставятся автоматически (`npm install`).

> Нужен установленный **Node.js** (вместе с ним идёт `npm`).

## Установка ярлыка

### Windows
Дважды кликните по **`install-shortcut.bat`** — на рабочем столе появится ярлык **«PlanPlace Keystatic»**.

### macOS
В терминале из корня репозитория:
```bash
bash tools/keystatic-launcher/install-shortcut.sh
```
На рабочем столе появится **«Запустить Keystatic.command»**. Первый запуск: правый клик → «Открыть» (чтобы обойти Gatekeeper).

### Linux
```bash
bash tools/keystatic-launcher/install-shortcut.sh
```
На рабочем столе появится **«PlanPlace · Keystatic»** (и пункт в меню приложений). Если система просит «разрешить запуск» — разрешите.

## Остановить
Закройте окно терминала/консоли, которое открылось при запуске (или `Ctrl+C` в нём).

## Без ярлыка
Можно запускать напрямую:
- Windows: `tools\keystatic-launcher\launch.bat`
- macOS/Linux: `bash tools/keystatic-launcher/launch.sh`
