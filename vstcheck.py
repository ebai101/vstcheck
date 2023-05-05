#!/usr/bin/env python
# lists all VSTs that are not arm64 compatible

from os import walk, listdir
from sys import stderr
from itertools import chain
from subprocess import Popen, PIPE
from concurrent.futures import ProcessPoolExecutor

# you may want to add more directories to this list
vst_directories = [
    "/Library/Audio/Plug-Ins/VST",
    "/Library/Audio/Plug-Ins/VST3",
    "~/Library/Audio/Plug-Ins/VST",
    "~/Library/Audio/Plug-Ins/VST3",
]


def get_arch_info(plug):
    exe_path = [f for f in listdir(f"{plug}/Contents/MacOS")]
    file_cmd = f'file "{plug}/Contents/MacOS/{exe_path[0]}"'
    cmd_out = Popen(file_cmd, shell=True, stdout=PIPE)
    return cmd_out.stdout.read().strip().decode()


def check_exec(plug_dir):
    print(f"Scanning {plug_dir} ...", file=stderr)

    # get plugin names
    plugs = []
    for dirpath, dirnames, filenames in walk(plug_dir):
        plugs += [f"{dirpath}/{dirname}" for dirname in dirnames if "vst" in dirname]

    # read architecture of executables
    result = []
    with ProcessPoolExecutor() as executor:
        for plug, arch_info in zip(plugs, executor.map(get_arch_info, plugs)):
            if not "arm64" in arch_info:
                result.append(plug)

    return result


if __name__ == "__main__":
    results = list(chain.from_iterable([check_exec(d) for d in vst_directories]))
    [print(vst) for vst in results]
