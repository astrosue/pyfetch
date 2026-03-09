from datetime import datetime
from itertools import zip_longest
import getpass
import psutil, socket
import time
import os
import subprocess

##mem
virt_mem = psutil.virtual_memory()

## vars
host = socket.gethostname()
user = getpass.getuser()
date = datetime.now()
ram_used = round(virt_mem.used / (1024**3), 1)
ram_total = round(virt_mem.total / (1024**3), 1)
ram_percent = virt_mem.percent
boot_time = psutil.boot_time()
uptime_seconds = time.time() - boot_time
hours = int(uptime_seconds // 3600)
minutes = int((uptime_seconds % 3600) // 60)

## strings
up_str = f"{hours}h {minutes}m"
##logoz
cachy_logo = [
    "  _____________    ",
    " /            /   ◯",
    "/    _______ /",
    "|    |          ⟋─⟍",
    "|    |          ⟍_⟋ ___",
    "\\    \\             /   \\",
    " \\    \\____________\\___/",
    "  \\                /",
    "   \\_____________ /"
]

arch_logo = [
r"      /\ ",
r"     /  \ ",
r"    /    \ ",
r"   /      \ ",
r"  /   ,,   \ ",
r" /   |  |   \ ",
r"/_-''    ''-_\ ",
]
fedora_logo = [
r"        ,'''''. ",
r"       |   ,.  | ",
r"       |  |  '_' ",
r"  ,....|  |.. ",
r".'  ,_;|   ..' ",
r"|  |   |  | ",
r"|  ',_,'  | ",
r" '.     ,' ",
r" ''''' "
]
gentoo_logo = [
r"  _-----_ ",
r" (       \ ",
r" \    0   \ ",
r"  \        )",
r" /      _/ ",
r" (     _- ",
r" \____- ",
]


default_logo = [
"ur distro dont get logo"
        ]

##defs
def get_os_name():
    if os.path.exists("/etc/os-release"):
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    return line.strip().split("=")[1].replace('"', '').replace("'", "")
    return("Linux kernel")


def get_distro_id():
    if os.path.exists("/etc/os-release"):
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("ID="):
                    return line.strip().split("=")[1].lower().replace('"', '').replace("'", "")
    return "unknown"


def get_logo(distro_id):
    logos = {
    "cachyos": cachy_logo,
    "arch": arch_logo,
    "fedora": fedora_logo,
    "gentoo": gentoo_logo
            }
    return logos.get(distro_id, default_logo)

def get_wm():
    session_type = os.environ.get("XDG_SESSION_TYPE", "unknown").lower()
    wm = os.environ.get("XDG_CURRENT_DESKTOP")

    if not wm:
        try:
            out = subprocess.check_output(['wmctrl', '-m'], text=True)
            for line in out.split('\n'):
                if line.startswith("Name:"):
                    wm = line.split(':')[1].strip()
                    break
        except:
            wm = "unknown wm"
    return f"{wm} ({session_type})"

def get_cpu():
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if "model name" in line:
                    return line.split(":")[1].strip()
    except: return "unknown cpu"

def get_gpu():
    try:
        gpu_info = subprocess.check_output("lspci | grep -Ei 'vga|3d|display'", shell=True, text=True)
        gpu_name = gpu_info.split(":")[-1].strip()
        return gpu_name
    except:
        return "unknown gpu"


##logo
def print_fetch():
    dist_id = get_distro_id()
    current_logo = get_logo(dist_id)
    print("")
    for logo_line, info_line in zip_longest(current_logo, info, fillvalue=""):
        print(f" {logo_line.ljust(25)} {info_line}")
    print("")


##sam fetch
info = [
f"\033[1;36m{user}\033[0m@\033[1;36m{host}\033[0m",
"----------------",
f"\033[1;32mOS:\033[0m {get_os_name()}",
f"\033[1;32mWM:\033[0m {get_wm()}",
f"\033[1;32mDate:\033[0m {date}",
f"\033[1;32mShell:\033[0m Python",
f"\033[1;32mCPU:\033[0m {get_cpu()}",
f"\033[1;32mGPU:\033[0m {get_gpu()}",
f"\033[1;32mRAM:\033[0m {ram_used}GB / {ram_total}GB ({ram_percent}%)",
f"\033[1;32mUptime:\033[0m {up_str}"
]
print_fetch()
