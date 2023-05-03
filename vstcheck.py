#!/usr/bin/env python
# lists all VSTs that are not arm64 compatible

import os, sys, subprocess, re

# you may want to add more directories to this list
vst_directories = [
    "/Library/Audio/Plug-Ins/VST",
    "/Library/Audio/Plug-Ins/VST3",
    "~/Library/Audio/Plug-Ins/VST",
    "~/Library/Audio/Plug-Ins/VST3",
]


def check_for_lipo():
    from shutil import which

    return which("lipo") is not None


def check_exec(plug_dir):
    result = {}
    plugs = []

    print(f"Scanning {plug_dir} ...")

    # get plugin names
    reg_compile = re.compile(".*\.vst")
    for dirpath, dirnames, filenames in os.walk(plug_dir):
        plugs = plugs + [
            f"{dirpath}/{dirname}" for dirname in dirnames if reg_compile.match(dirname)
        ]

    # read architecture of executables
    for plug in plugs:
        exe_file = [f for f in os.listdir(f"{plug}/Contents/MacOS")]
        exe_cmd = f'lipo -archs "{plug}/Contents/MacOS/{exe_file[0]}"'
        exe = subprocess.Popen(exe_cmd, shell=True, stdout=subprocess.PIPE)
        out = exe.stdout.read().strip().decode()
        if not out in result:
            result[out] = []
        result[out].append(plug)

    # remove already compatible plugins
    delete = [key for key in result if "arm64" in key]
    for key in delete:
        del result[key]
    return result


def print_results(res):
    for key in res:
        print(key)
        for val in res[key]:
            print(f"\t{val}")


if __name__ == "__main__":
    if not check_for_lipo():
        print("lipo executable not found in PATH")
        print("you may need to install xcode commandline tools by running:")
        print("\t xcode-select --install")
        sys.exit(1)

    result_list = [check_exec(d) for d in vst_directories]
    result_final = {}
    for result in result_list:
        for key in result.keys():
            if not key in result_final:
                result_final[key] = result[key]
            else:
                result_final[key] += result[key]
    print_results(result_final)
