# clean up verbose filenames - replace with simple ones with only pertinent info

"""
Instructions:

- Write a program to convert the returns from the format in the first picture, to the 
format of the second picture.
- Some returns will have indications as to what their tax jurisdiction is like the 
NJ returns below in the second picture, in this case, I need to manually look at 
the PDF and confirm the jurisdiction. (I will include further instruction on this).

What I need to keep:

-State abbreviation most important
-What the PDF is (EDI Confirmation, Return, Return Payment)
-The year and month (202111) Keep in mind this will change month to month.
-Keep all the letters and put them in the front. Example: The first PDF in picture 1.
Should code to: "NC_ST_SU_EDI Confirmation_202111"
- There are going to be returns that have multiple returns for its state. If you see 
in the first picture, there are a few from Ohio (OH). To combat this issue, look at 
the beginning numbers in picture 1. There are 5 PDFs with 4860802, that means it's 
all one return. For states with multiple returns, including keeping all the letters, 
please link those together. What do I mean by link together? For those same 5 pdf 
examples, do like the above format and add "(1)." In this case, this return has 
two confirmations, you can do "1a" & "1b".
-If you can't program some of the above tasks, it's okay. Whatever you can do is
amazing.

What I need to delete:

- All the numbers and special characters.
- Match it as best you can to picture 2 but keep the ST_SU as well because it'll make 
both our lives easier and in future if anything you or I could edit the code down 
the road.
"""

import os


codes = ["TT", "KB", "FB", "GG"]


class filename:
    """filename object with attributes: identifier (4860802), sub_identifier ((1)),
    type (EDI Confirmation, Return, Return Payment), date (202111),
    state_code (NC_ST_SU),
    """

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
    ufile_split = ufile_noext.split("~")

    for item in ufile_split:
        # check states
        if item in filename.state_abbreviations:
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
