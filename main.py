# Clean up verbose filenames - replace with simple ones with only pertinent info

import os
import shutil
import tkinter


state_abbreviations = [
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DE",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY",
]


def main():
    udir = get_dir()
    for ufile in os.listdir(udir):
        # copy_dir(udir)
        src = f"{udir}\\{ufile}"
        dest = f"{udir}\\{str(change_name(ufile))}"
        os.rename(src, dest)
        print(f"udir = {udir}")
        print(f"ufile = {ufile}")

    pass


def change_name(ufile):
    """change the name of ufile with specific criteria

    Args:
        ufile (str): name of file to rename
    """
    new_name = []
    
    #TODO: Change to .pdf
    ufile_noext = ufile.translate(str.maketrans("", "", ".txt"))
    #TODO: Check for other delimiters
    ufile_split = ufile_noext.split("_")
    
    for state in state_abbreviations:
        if state in ufile_split:
            new_name.append(state)
        
        else:  # Temporary for easier testing
            continue
        
    #TODO: Change to .pdf
    new_name.append(".txt")
    new_name = '_'.join(new_name)
    return new_name


def copy_dir(udir):
    udir_edit = udir.split("\\")
    udir_edit.pop()
    udir_edit = "\\".join(udir_edit)
    dest = f"{udir_edit}\\backup\\"
    print(f"udir_edit = {udir_edit} --- dest = {dest}")
    shutil.copy(udir, dest)


def get_dir():
    """get directory to work on from user. Should use GUI."""
    # Temp value for now
    return "C:\\Users\\jgeog\\Code\\PythonProjects\\filename_change\\test_dir"


if __name__ == "__main__":
    main()
