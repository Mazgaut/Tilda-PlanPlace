' Запуск Keystatic без видимого окна консоли (тихий режим).
' Можно сделать ярлык на рабочем столе именно на этот файл — тогда при
' двойном клике ничего не мелькнёт, просто откроется браузер с админкой.
' Чтобы остановить сервер в этом режиме — завершите процесс node.exe
' в Диспетчере задач (или используйте обычный launch.bat, где есть окно).
Dim fso, sh, dir
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh  = CreateObject("WScript.Shell")
dir = fso.GetParentFolderName(WScript.ScriptFullName)
sh.CurrentDirectory = dir
sh.Run """" & dir & "\launch.bat""", 0, False
