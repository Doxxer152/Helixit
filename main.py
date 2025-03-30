import os
import subprocess
import sys

LIB_PATH = "/data/data/com.termux/files/usr/lib"
TARGET_LIB = f"{LIB_PATH}/libpython3.12.so.0.1"
SOURCE_LIB = f"{LIB_PATH}/libpython3.12.so.1.0"
BASHRC_PATH = os.path.expanduser("~/.bashrc")
EXPORT_CMD = f"export LD_LIBRARY_PATH={LIB_PATH}:$LD_LIBRARY_PATH"

if os.path.exists(SOURCE_LIB) and not os.path.exists(TARGET_LIB):
    subprocess.run(["ln", "-s", SOURCE_LIB, TARGET_LIB], check=True)

os.environ["LD_LIBRARY_PATH"] = f"{LIB_PATH}:" + os.environ.get("LD_LIBRARY_PATH", "")

with open(BASHRC_PATH, "r") as bashrc:
    lines = bashrc.readlines()

if EXPORT_CMD not in "".join(lines): 
    with open(BASHRC_PATH, "a") as bashrc:
        bashrc.write("\n" + EXPORT_CMD + "\n")

protected_script = os.path.join(os.path.dirname(__file__), "protected.py")

if not os.path.exists(protected_script):
    print("Ошибка: защищённый файл protected.py не найден!")
    sys.exit(1)

subprocess.run([sys.executable, protected_script])
