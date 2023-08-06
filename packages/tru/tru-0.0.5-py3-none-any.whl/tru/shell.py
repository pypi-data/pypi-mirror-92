import subprocess
from sys import platform
import os
import stat
from .global_vars import CACHE


def execute_shell_and_return_result(cmd):

    process = subprocess.Popen(
        cmd,
        shell=True,
        encoding="ascii",
        executable="/bin/bash",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = process.communicate()
    process.wait()
    if err != "":
        raise Exception(err)
    return out


def execute_in_terminal(cmd, dry_run=False):
    if isinstance(cmd, list):
        cmd_list = cmd
    else:
        cmd_list = [cmd]

    execute_strings_in_terminal(cmd_list, dry_run=dry_run)


def execute_strings_in_terminal(strings, dry_run=False):
    if not isinstance(strings, list):
        raise TypeError("Argument must be a list of strings")
    if not all(isinstance(x, str) for x in strings):
        raise TypeError("Argument must be a list of strings")
    if not os.path.isdir(CACHE):
        os.makedirs(CACHE, exist_ok=True)

    file_name = os.path.join(CACHE, "tru_temp_file.sh")
    with open(file_name, "w") as f:
        f.write("set -eu -o pipefail\n")
        f.writelines(f"{s}\n" for s in strings)

    # Make executable: chmod +x
    st = os.stat(file_name)
    os.chmod(file_name, st.st_mode | stat.S_IEXEC)

    if platform == "linux" or platform == "linux2":
        cmd = f"gnome-terminal -e '/bin/bash -c \"{file_name}; /bin/bash\" '"
    elif platform == "darwin":
        cmd = f'osascript -e \'tell app "Terminal" to do script "{file_name}"\''
    elif platform == "win32":
        raise EnvironmentError("Win32 shell is not supported")
    else:
        raise EnvironmentError("Unknown OS")

    if dry_run:
        execute_shell_and_return_result(f"cat {file_name}")
    else:
        print(cmd)
        os.system(cmd)
