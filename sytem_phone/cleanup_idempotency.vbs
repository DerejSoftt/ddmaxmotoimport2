Set WshShell = CreateObject("WScript.Shell")

' Configurar rutas
Dim projectPath, pythonExe, command
projectPath = "c:\Users\USER\Desktop\PROYECTOS\ddmaxmotoimport2\sytem_phone"
pythonExe = projectPath & "\venv\Scripts\python.exe"
command = pythonExe & " " & projectPath & "\manage.py cleanup_idempotency"

' Ejecutar en segundo plano (0 = ventana oculta, True = esperar a que termine)
WshShell.Run "cmd /c cd /d " & projectPath & " && " & command, 0, True

Set WshShell = Nothing
