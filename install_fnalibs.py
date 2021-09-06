"""
   Copyright 2021 Lucy Beda

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import subprocess
import os
import os.path as path
import argparse
import shutil
import sys

class LibraryDescriptor:
    def __init__(self, name: str, remote: str):
        self.name = name
        self.remote = remote
    def clone(self, fnalibs_dir: str):
        repo_path = path.join(fnalibs_dir, self.name)
        if path.isdir(repo_path):
            shutil.rmtree(repo_path)
        elif path.exists(repo_path):
            os.unlink(repo_path)
        args = [
            "git",
            "clone",
            "--recursive",
            self.remote,
            repo_path
        ]
        return subprocess.call(args) == 0
def determine_target_directory():
    if sys.platform.lower().startswith("darwin"):
        return path.join(os.getcwd(), "osx")
    elif sys.platform.lower().startswith("win32"):
        return os.getcwd()
    else:
        return "no path"
LIBS = [
    LibraryDescriptor("SDL2", "https://github.com/libsdl-org/SDL.git"),
    LibraryDescriptor("FNA3D", "https://github.com/FNA-XNA/FNA3D.git"),
    LibraryDescriptor("FAudio", "https://github.com/FNA-XNA/FAudio.git")
]
SCRIPT_DIR = path.dirname(path.abspath(__file__))
FNALIBS_DIR = path.join(SCRIPT_DIR, "fnalibs")
BUILD_DIR=path.join(SCRIPT_DIR, "build")
CONFIGURE_OPTIONS = {
    "SDL_SHARED": "ON",
    "SDL_STATIC": "OFF",
    "BUILD_SHARED_LIBS": "ON",
    "FNALIBS_TARGET_DIRECTORY": determine_target_directory()
}
def configure(cmake="cmake"):
    args = [
        cmake,
        FNALIBS_DIR,
        "-B",
        BUILD_DIR
    ]
    for option in CONFIGURE_OPTIONS.keys():
        args.append(f"-D{option}={CONFIGURE_OPTIONS[option]}")
    return subprocess.call(args) == 0
def build(cmake="cmake"):
    args = [
        cmake,
        "--build",
        BUILD_DIR,
        "-j",
        "8"
    ]
    return subprocess.call(args) == 0
def install(cmake="cmake"):
    args = [
        "sudo",
        cmake,
        "--install",
        BUILD_DIR
    ]
    return subprocess.call(args) == 0
def main(options):
    for lib in LIBS:
        print(f"Cloning {lib.name}...")
        if not lib.clone(FNALIBS_DIR):
            print(f"Could not clone {lib.name}!")
            exit(1)
        else:
            print(f"Successfully cloned {lib.name}!")
    print(f"Configuring {FNALIBS_DIR}...")
    if not configure(cmake=options.cmake):
        print(f"Could not configure {FNALIBS_DIR}!")
        exit(1)
    else:
        print(f"Successfully configured {FNALIBS_DIR}!")
    print(f"Building {BUILD_DIR}")
    if not build(cmake=options.cmake):
        print(f"Could not build {BUILD_DIR}!")
        exit(1)
    else:
        print(f"Successfully built {BUILD_DIR}!")
    if sys.platform.lower().startswith("linux"):
        print(f"Installing FNA libs...")
        if not install(cmake=options.cmake):
            print(f"Could not install FNA libs!")
            exit(1)
        else:
            print("Successfully installed FNA libs!")
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cmake", help="Select the CMake command to use", type=str, default="cmake")
    main(parser.parse_args())
