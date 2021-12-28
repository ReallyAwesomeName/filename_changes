# clean up verbose filenames - replace with simple ones with only pertinent info

import os


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

codes = ["TT", "KB", "FB", "GG"]


def main():
    udir = get_dir()

    # for each file in the directory
    for ufile in os.listdir(udir):
        # full path with original filename
        src = f"{udir}\\{ufile}"

        # full path with new filename
        new_name = change_name(ufile)
        dest = f"{udir}\\{new_name}"

        os.rename(src, dest)

        # TODO: remove after testing
        print(f"original = {ufile}")
        print(f"new_name = {new_name}")
        print("=" * 15)


def change_name(ufile):
    """change the name of ufile with specific criteria

    Args:
        ufile (str): name of file to rename
    """
    new_name = []

    # remove .pdf, add back before return
    ufile_noext = ufile.strip(".pdf")
    # TODO: check for other delimiters
    ufile_split = ufile_noext.split("_")

    for item in ufile_split:
        # check states
        if item in state_abbreviations:
            new_name.append(item)
        # check codes
        if item in codes:
            new_name.append(item)

        # TODO: make sure this is specific enough for all file variations
        # check if all digits (dates)
        if item.isdigit():
            new_name.append(item)

        else:
            continue

    # join and add back .pdf
    new_name = "_".join(new_name)
    new_name = f"{new_name}.pdf"
    return new_name


# TODO: make work with CLI or GUI
def get_dir():
    """get directory to work on from user. Should use GUI."""
    # temp value for now
    return "C:\\Users\\jgeog\\Code\\PythonProjects\\filename_change\\test_dir"


if __name__ == "__main__":
    main()
