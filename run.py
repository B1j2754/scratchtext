import os
import shutil
import scratch
from appUi import open_sb3_TW

# Read contents of code file - currently where the "text editor" is
with open('CODE.txt','r') as j:
    src = j.read()
    j.close()

# S1 is the sprite name for the code to be injected into
program = {"S1": scratch.parse(src)}
print(program)
shutil.copyfile('assets/start.sb3', 'projects/program.sb3')
input_path = r"projects/program.sb3"
output_path = os.path.normpath(input_path)

# Open specified project
project = scratch.ScratchProject(os.path.normpath(input_path))
project.add_program(program)
project.write(output_path)

# Open the project using TurboWarp offline editor
open_sb3_TW(output_path)