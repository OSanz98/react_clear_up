# This is a Python project used to clear up node_modules folders in existing react applications
import os
import shutil
import errno
import logging
from tqdm import tqdm
from tkinter import filedialog, messagebox
import tkinter as tk

# global variable to keep track of total space cleared
total_space_cleared = 0
# store array of errors that we may encounter
errors = []
# store global list of root directories
root_directories = []
skip_directories = []

# use object instance of TK for tkfilebrowser
root_tk = tk.Tk()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')


def get_directory_size(directory):
    """
    Calculates the total size of a directory by recursively walking through its files.
    :param directory: (str) The path to the directory.
    :return: Total size of the directory in bytes.
    """
    total_size = 0
    for directoryPath, directoryNames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(directoryPath, f)
            total_size += os.path.getsize(fp)
    return total_size


def is_react_app(directory):
    """
    Checks if a given directory is a React application by looking for the 'package.json' file.
    :param directory: (str) Path to directory.
    :return: bool - True if directory is a React application, False otherwise.
    """
    package_json_path = os.path.join(directory, 'package.json')
    return os.path.exists(package_json_path)


def remove_node_modules(directory):
    """
    Removes 'node_modules' folder from a given directory and updates the total space cleared.
    :param directory: (str) Path to directory.
    """
    global total_space_cleared  # access global variable
    node_modules_path = os.path.join(directory, 'node_modules')  # store path to the node_modules folder
    if os.path.exists(node_modules_path):  # if exists then remove folder
        try:
            node_modules_size = get_directory_size(node_modules_path)
            shutil.rmtree(node_modules_path)  # remove node_modules folder
            total_space_cleared += node_modules_size  # update total_space_cleared
            logging.info(f"Removed node_modules from {directory}")  # log path to react app
        except PermissionError:
            # log error if script doesn't have permission to remove files from directory
            errors.append(f"Error: Permission denied to remove node_modules from {directory}")


def scan_and_clean():
    """
    Recursively scans the root directory and its subdirectories for React applications,
    skipping the directories specified in the 'skip_directories' list, and removes their node_modules folders.
    :param skip_dir: (str[]) Array of paths to skip in clean up
    :param root_dirs: (str) Path to root directory.
    """
    react_apps_found = []  # create array to store paths to react applications
    for root_dir in root_directories:
        for root, dirs, files in os.walk(root_dir):
            # returns true if both pathname arguments refer to the same file or directory
            if any(os.path.samefile(root, os.path.abspath(skip_dir)) for skip_dir in skip_directories):
                # loops through each file/directory specified in skip directories array to compare against
                continue
            if is_react_app(root):
                react_apps_found.append(root)  # append path to react_apps_found for removal later

    # create initial progress bar which updates based on number of paths to remove node_modules folders from
    progress_bar = tqdm(total=len(react_apps_found), unit='app', desc='Cleaning React apps')
    # for each path in react applications found array, call function remove_node_modules to remove it
    for app_path in react_apps_found:
        remove_node_modules(app_path)
        # update progress bar to show completion
        progress_bar.update(1)
    # close the progress bar to show all node_modules have been removed
    progress_bar.close()


# Allow user to select root directories to choose for cleaning
def select_root_directories():
    global root_directories  # access global list
    directory = filedialog.askdirectory(title="Select A Root Directory")
    if directory:
        directory = os.path.abspath(directory)
        if directory not in root_directories:
            root_directories.append(directory)
            root_directories_listbox.insert(tk.END, directory)


# Allow user to select directories to skip from the cleanup script
def select_skip_directories():
    global skip_directories  # access global list
    directory = filedialog.askdirectory(title="Select A Directory To Skip")
    if directory:
        directory = os.path.abspath(directory)
        if directory not in skip_directories:
            skip_directories.append(directory)
            skip_directories_listbox.insert(tk.END, directory)


# Function runs cleanup script and gets user to select root folders to choose from
def run_cleanup():
    scan_and_clean()  # run cleanup on chosen directories

    logging.info(f"\nTotal space cleared: {total_space_cleared} bytes")

    if errors:
        logging.info("\nErrors encountered:")
        for error in errors:
            logging.error(error)

    messagebox.showinfo("Cleanup Completed", f"Total space cleared: {total_space_cleared} bytes")


root_tk.title("React Application Cleanup")

root_directories_frame = tk.Frame(root_tk)
root_directories_frame.pack(pady=10)

root_directories_label = tk.Label(root_directories_frame, text="Root Directories:")
root_directories_label.pack(side=tk.LEFT)

select_root_directory_button = tk.Button(root_directories_frame, text="Select", command=select_root_directories)
select_root_directory_button.pack(side=tk.LEFT, padx=5)

root_directories_listbox = tk.Listbox(root_directories_frame, width=50)
root_directories_listbox.pack(side=tk.LEFT, padx=5)

# Directories to Skip
skip_directories_frame = tk.Frame(root_tk)
skip_directories_frame.pack(pady=10)

skip_directories_label = tk.Label(skip_directories_frame, text="Directories to Skip:")
skip_directories_label.pack(side=tk.LEFT)

select_skip_directory_button = tk.Button(skip_directories_frame, text="Select", command=select_skip_directories)
select_skip_directory_button.pack(side=tk.LEFT, padx=5)

skip_directories_listbox = tk.Listbox(skip_directories_frame, width=50)
skip_directories_listbox.pack(side=tk.LEFT, padx=5)

run_cleanup_button = tk.Button(root_tk, text="Run Cleanup", command=run_cleanup)
run_cleanup_button.pack(pady=10)

root_tk.mainloop()