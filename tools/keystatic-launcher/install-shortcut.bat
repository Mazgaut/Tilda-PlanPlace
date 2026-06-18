@echo off
chcp 65001 >nul
rem Создаёт ярлык на рабочем столе (Windows), который запускает Keystatic.
rem Запустить один раз двойным кликом по этому файлу.
setlocal
set "TARGET=%~dp0launch.bat"
set "WORKDIR=%~dp0..\.."
set "LNK=%USERPROFILE%\Desktop\PlanPlace Keystatic.lnk"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$s=(New-Object -ComObject WScript.Shell).CreateShortcut('%LNK%'); $s.TargetPath='%TARGET%'; $s.WorkingDirectory=(Resolve-Path '%WORKDIR%').Path; $s.IconLocation='%SystemRoot%\System32\shell32.dll,13'; $s.Description='Запуск локальной админки Keystatic'; $s.Save()"

echo Готово. Ярлык на рабочем столе: "%LNK%"
echo Дважды кликните по нему - поднимется Keystatic и откроется браузер.
pause
