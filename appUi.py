"""
Script for openning an SB3 project using the offline turbowarp editor
"""
from secret_manager import get_key
import subprocess
import os
import time     

def open_sb3_TW(sb3_file_path):
    # Update path according to location of TurboWarp.exe
    turbowarp_executable_path = os.path.normpath(get_key('Program'))

    if not os.path.isfile(sb3_file_path):
        raise FileNotFoundError(f"The file {sb3_file_path} does not exist.")

    # Run TurboWarp with the specified .sb3 file
    turbowarp_process = subprocess.Popen([turbowarp_executable_path, sb3_file_path])

    # Allow some time for the window to open
    #time.sleep(2)

    # # Use PowerShell to arrange windows
    # powershell_script = f"""
    # $Shell = New-Object -ComObject shell.application
    # $Shell.TileVertically()
    # """
    # subprocess.run(["powershell", "-Command", powershell_script], check=True)

    return turbowarp_process