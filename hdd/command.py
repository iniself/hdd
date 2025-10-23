#!/usr/bin/env python

import os, sys, argparse
from . import __version__
from pathlib import Path
from tomlkit import parse, dumps
from hdd.snippet import (
    load_json_file_if_not_exist_return_empty_dict,
    write_config_to_json_file,
    copyfile,
)

try:
    package_absolute_path = Path(__file__).absolute().parent
    project_absolute_path = Path.cwd()

    sys.path.append(str(project_absolute_path))
except:
    pass

hdd_template = package_absolute_path.joinpath("templates")

project_folder = ["bootstrap", "migrate", "pipeline", "config", "services", "provider"]


def main(**kwargs):
    parser = argparse.ArgumentParser(
        prog="hdd",
        usage="%(prog)s [OPTION]",
        description="%(prog)s is a tools package",
        add_help=True,
    )
    subparsers = parser.add_subparsers(dest="command")
    parser.add_argument(
        "-V", "--version", help="show %(prog)s version", action="store_true"
    )
    init_parser = subparsers.add_parser("init", help="init your %(prog)s project")
    init_parser.add_argument("--name", help="Project name")

    args = parser.parse_args()

    if args.version:
        print(f"hdd version is: {__version__}")

    if args.command == "init":
        try:
            project_name = input("Project Name: ").strip() or args.name or "hdd_project"
            version = input("Version(default 0.1.0): ").strip() or "0.1.0"
            description = input("description: ").strip() or "one hdd project"
            author = input("Author: ").strip() or "Anonymous"
        except KeyboardInterrupt:
            print("\n❌ 取消操作。")
            sys.exit(0)

        try:
            package_name = make_project_dir(project_name)
        except Exception:
            raise IOError(
                "There was an error creating the folder. Please check your execution permissions. Alternatively, you can creating by manually: bootstrap | migrate | pipeline | config | provider"
            )

        try:
            copy_template(f"pyproject.toml", f"{project_name}/pyproject.toml")
            copy_template(
                f"config/core_config.json", f"{package_name}/config/core_config.json"
            )
            copy_template(
                f"config/project_config.json",
                f"{package_name}/config/project_config.json",
            )
        except Exception:
            raise IOError(
                "Copying config template files failed. You can manually create them: config/core_config.json"
            )

        try:
            for folder in project_folder:
                copy_template(
                    f"bootstrap/__init__.py", f"{package_name}/{folder}/__init__.py"
                )

            copy_template(f"bootstrap/main.py", f"{package_name}/main.py")
        except Exception:
            print("Copying boot template files failed. You can manually create them")

        with open(f"{project_name}/pyproject.toml", "r", encoding="utf-8") as f:
            pyproject = parse(f.read())

        pyproject["tool"]["setuptools"]["packages"] = project_name
        pyproject["project"]["name"] = project_name
        pyproject["project"]["version"] = version
        pyproject["project"]["authors"] = [{"name": author}]
        pyproject["project"]["description"] = description

        with open(f"{project_name}/pyproject.toml", "w", encoding="utf-8") as f:
            f.write(dumps(pyproject))

        print(f"Init {parser.prog} project, Done", end="\n\n")


def make_project_dir(project_name):
    package_name = f"{project_name}/{project_name}"
    for folder in project_folder:
        os.makedirs(f"{package_name}/{folder}", exist_ok=True)
    return package_name


def copy_template(src, dst):
    dst_absolute_path = project_absolute_path.joinpath(dst)
    if not check_file_exist(dst_absolute_path):
        copyfile(hdd_template.joinpath(src), dst_absolute_path)


def read_template(file_name):
    return load_json_file_if_not_exist_return_empty_dict(
        hdd_template.joinpath(file_name)
    )


def write_config(file_name, json):
    write_config_to_json_file(project_absolute_path.joinpath(file_name), json)


def check_dir_exist(dir):
    path = Path(dir)
    return path.exists() and path.is_dir()


def check_file_exist(file):
    file = Path(file)
    return file.exists() and file.is_file()


if __name__ == "__main__":
    main()
