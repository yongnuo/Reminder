Installera python3
Hamnar i C:\Users\zacharias\AppData\Local\Programs\Python\Python310

Kolla version
py --version

Uppgradera pip
py -m pip install --user --upgrade pip 
(eller)
py -m pip install --upgrade pip

Skapa venv
py -m venv reminder

Aktivera venv
.\reminder\Scripts\activate.bat

Installera paket
py -m pip install pystray

Visa paket
py -m pip freeze

Kör ex tray
py .\tray.py

OBS! Bra att köra en ny prompt med Powershell Execution-Policy som bypass
powershell.exe -ExecutionPolicy Bypass

Deaktivera venv
exit (stänger av command prompt)

Öppna Startup-katalog
press Windows+R, then type shell:startup.

Skapa genväg med följande text
"C:\Program Files\PowerShell\7\pwsh.exe" -command "& C:\OwnProjects\Reminder\reminder\Scripts\pythonw.exe C:\OwnProjects\Reminder\production\reminder.py -s C:\OwnProjects\Reminder\production\exercise_settings.yaml"

