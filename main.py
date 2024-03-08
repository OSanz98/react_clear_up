# This is a Python project used to clear up node_modules folders in existing react applications
import os
import argparse
import shutil


def is_react_app(directory):
    package_json_path = os.path.join(directory, 'package.json')
    return os.path.exists(package_json_path)

def remove_node_modules(directory):
    node_modules_path = os.path.join(directory, 'node_modules')
    if os.path.exists(node_modules_path):
        shutil.rmtree(node_modules_path)
        print(f"removed node_modules from {directory}")


def scan_and_clean(root_dir):
    for root, dirs, files in os.walk(root_dir):
        if is_react_app(root):
            remove_node_modules(root)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Clean up React applications")
    parser.add_argument('directory', type=str, help='Root directory to scan')
    args = parser.parse_args()

    scan_and_clean(args.directory)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
