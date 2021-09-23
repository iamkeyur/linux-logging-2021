def get_subsystem(filepath):
    core_files = ["init", "block", "ipc", "kernel", "lib", "mm", "virt"]
    fs_files = ["fs"]
    driver_files = ["crypto", "drivers", "sound", "security"]
    net_files = ["net"]
    arch_files = ["arch"]
    misc_files = ["Documentation", "scripts", "samples", "usr", "MAINTAINERS", "CREDITS", "README",
                  ".gitignore", "Kbuild", "Makefile", "REPORTING-BUGS", ".mailmap", "COPYING", "tools",
                  "Kconfig", "LICENSES", "certs", ".clang-format"]
    firmware_files = ["firmware"]

    folder = filepath.split("/")[0]

    if folder in core_files:
        return "core"
    if folder in fs_files:
        return "fs"
    if folder in driver_files:
        return "driver"
    if folder in net_files:
        return "net"
    if folder in arch_files:
        return "arch"
    if folder in misc_files:
        return "misc"
    if folder in firmware_files:
        return "firmware"

    return ""


with open("upd_final.csv", "r") as f:
    lines = f.readlines()

subsystems = ["core", "driver", "fs", "net", "arch", "misc", "firmware"]

for line in lines:
    line = line.rstrip()
    data = line.split("|||||")

    if "||||||||||" in line:
        continue
    if len(data) == 5:
        subsystem = get_subsystem(data[2])
        old_function = data[3].split(" ")[0]
        new_function = data[4].split(" ")[0]

        if "70@@" not in old_function or "70@@" not in new_function:
            continue
        if subsystem != "" and subsystem in subsystems:
            print(str(subsystem), str.replace(str(old_function), "70@@", ""), str.replace(str(new_function), "70@@", "") , line, sep='|||||')