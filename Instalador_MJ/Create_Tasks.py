import subprocess

def create_scheduled_task(task_name, executable_path, delay="00:00"):
    # Flags para suprimir janelas
    flags = subprocess.CREATE_NO_WINDOW

    # Verifica se a tarefa já existe
    check_cmd = ['schtasks', '/Query', '/TN', task_name]
    task_exists = subprocess.run(check_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=flags).returncode == 0

    # Remove se já existir
    if task_exists:
        delete_cmd = ['schtasks', '/Delete', '/TN', task_name, '/F']
        subprocess.run(delete_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=flags)

    # Cria a nova tarefa com atraso após o logon
    create_cmd = [
        'schtasks', '/Create',
        '/SC', 'ONLOGON',
        '/RL', 'HIGHEST',
        '/TN', task_name,
        '/TR', f'"{executable_path}"',
        '/RU', 'SYSTEM',
        '/DELAY', delay,
        '/F'
    ]
    subprocess.run(create_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=flags)

    # Ajusta para executar com bateria via PowerShell
    ps_script = f'''
    $task = Get-ScheduledTask -TaskName "{task_name}"
    $task.Settings.DisallowStartIfOnBatteries = $false
    $task.Settings.StopIfGoingOnBatteries = $false
    Set-ScheduledTask -TaskName "{task_name}" -Settings $task.Settings
    '''
    subprocess.run(['powershell', '-Command', ps_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=flags)
