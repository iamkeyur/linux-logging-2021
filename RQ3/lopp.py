import os

with open("OutDone", "r") as f:
    cc = f.readlines()

import subprocess
from pathlib import Path

def run(command: str, cwd=None) -> str:
    working_dir = cwd
    if cwd is not None:
        p = Path(cwd)
        if p.is_file():
            working_dir = p.parent

    return subprocess.run(command, shell=True, cwd=working_dir, stdout=subprocess.PIPE).stdout.decode('utf-8')

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
cnt = 1
for c in cc:
    c = c.rstrip()
    dd = c.split(",")
    with cd("/home/keyur/Desktop/LinuxWorkingGit/linux"):
        with open("/home/keyur/Desktop/KernelHeuristic/FinalFolder/RQ3/Commits/" + str(cnt) + "___" +  str(dd[0]) + ".txt", "w") as f:
            f.write(str(dd) + "\n")
            f.write(run("git show " + dd[0]))
        f.close()
    cnt = cnt + 1