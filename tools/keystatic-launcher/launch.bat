@echo off
chcp 65001 >nul
rem Запуск локальной админки Keystatic + открытие её в браузере по умолчанию.
rem Скрипт сам переходит в корень репозитория (лежит в tools\keystatic-launcher\).
setlocal
cd /d "%~dp0..\.."
set "URL=http://localhost:4321/keystatic"

if not exist node_modules (
  echo Устанавливаю зависимости (первый запуск, это разово)...
  call npm install
)

rem Отдельное окно: ждём, пока сервер ответит, и открываем браузер
start "" /min powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$u='%URL%'; for($i=0;$i -lt 90;$i++){ try{ Invoke-WebRequest -UseBasicParsing $u -TimeoutSec 2 ^| Out-Null; break } catch { Start-Sleep 1 } }; Start-Process $u"

echo Запускаю Keystatic... (%URL%)
echo Чтобы остановить - закройте это окно или нажмите Ctrl+C.
call npm run cms
