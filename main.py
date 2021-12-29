# clean up verbose filenames - replace with simple ones with only pertinent info

# TODO: remove debugging print statements
# TODO: pack into .exe file

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
    "PR",
    "GU",
    "DC",
]

# TODO: Check last entries
doc_types = [
    "EDI Confirmation",
    "EDI Return",
    "Return Payment",
    "Return",
    "Confirmation",
]

# create list of years from 2020 - 2099
years = [str(x) for x in range(2020, 2100)]


def main():
    # TODO: ensure sufficient error handling

    udir = get_dir()

    print("=" * 30)

    try:
        # for each file in the directory
        for ufile in os.listdir(udir):
            # original all have ~ which is removed for all renames
            if "~" not in ufile:
                print(f"File '{ufile}' already renamed\n{'='*30}")
                continue

            # full path with original filename
            src = f"{udir}\\{ufile}"  # src = source (original file path)

            # full path with new filename
            new_name = change_name(ufile)
            dest = f"{udir}\\{new_name}"  # dest = destination (altered file path)

            # apply the rename, handles FileExistsError recursively
            actually_rename(src, dest)

            print(f"original = {ufile}")
            print(f"new_name = {new_name}")
            print("=" * 30)

    except FileNotFoundError:
        # TODO: prompt user for another attempt - call main() again
        return print("Specified directory not found")


def actually_rename(src, dest, n=0):
    """calls os.rename() and handles FileExistsError recursively

    Args:
        src (string): original file name (full path)
        dest (string): new file name (full path)
        n (int, optional): counter for end of duplicate names. Defaults to 0.
    """
    try:
        if n > 0:
            dest = dest.strip(".pdf")
            dest = f"{dest} ({n}).pdf"
            os.rename(src, dest)
        else:
            os.rename(src, dest)

    except FileExistsError:
        actually_rename(src, dest, n + 1)


def change_name(ufile):
    """change the name of ufile with specific criteria:
    <state&code>_<doc_type>_<date>
    strip everything else

    Args:
        ufile (str): name of file to rename
    Return:
        new_name (str): new name for file
    """

    # empty name list to be filled in with pertinent information
    new_name = []

    # remove .pdf, add back before return
    ufile_noext = ufile.strip(".pdf")
    # TODO: check for other delimiters
    ufile_split = ufile_noext.split("~")

    for item in ufile_split:
        # check states (state abbreviation will be first 2 characters of item)
        try:
            if ("".join(item[:2])) in state_abbreviations:
                state_code = item  # save item to put in new_name
        except IndexError:
            # not a state code, just pass
            pass

        # check if a dtype from doc_types is in the item
        for dtype in doc_types:
            if dtype in item:
                # remove all numbers/symbols around it,
                # only use doc_types entry, as requested
                document_type = dtype  # save document type to put in new_name

        # TODO: make sure this is specific enough for all file variations
        # check if all digits (may be a date)
        if item.isdigit():
            try:
                # check if first 4 digits are a valid year (range(2020, 2100))
                if ("".join(item[:4])) in years:
                    document_date = item  # save item to put in new_name
            except IndexError:
                # not a number from 2020 - 2099 (inclusive) so pass
                pass

    # add info to new_name in specified order
    new_name.append(state_code)
    new_name.append(document_type)
    new_name.append(document_date)

    # join and add back .pdf
    new_name = "_".join(new_name)
    new_name = f"{new_name}.pdf"
    return new_name


# TODO: make work with CLI or GUI. Remember try, except
def get_dir():
    """get directory to work on from user. Should use GUI."""
    # temp value for now
    return "C:\\Users\\jgeog\\Code\\PythonProjects\\filename_change\\test_dir copy"


if __name__ == "__main__":
    main()
