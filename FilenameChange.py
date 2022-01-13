# clean up verbose filenames - replace with simple ones with only pertinent info


from os import listdir, rename, path
from string import digits, punctuation
import tkinter as tk
from tkinter import messagebox
from sys import exit
import logging
from logging.handlers import RotatingFileHandler



def main():
    # TODO: ensure sufficient error handling
    root = tk.Tk()
    popup_window = RenameFiles(master=root)
    popup_window.mainloop()

    # abort if no directory is given
    try:
        if len(popup_window.udir) == 0:
            messagebox.showerror('Error', 'No directory entered.\nNo filenames changed.')
            exit()
    except TypeError:
        messagebox.showerror('TypeError', 'issue with len(popup_window.udir)')

    try:
        # for each file in the directory
        for ufile in listdir(popup_window.udir):
            # original all have ~ which is removed for all renames
            if "~" not in ufile:
                # add to list of unchanged filenames for output log
                popup_window.unchanged.append(ufile)
                continue

            # full path with original filename
            src = f"{popup_window.udir}\\{ufile}"  # src = source (original file path)

            # full path with new filename
            new_name = popup_window.make_new_name(ufile)
            dest = f"{popup_window.udir}\\{new_name}"  # dest = destination (altered file path)
            

            # apply the rename, handles FileExistsError recursively
            popup_window.actually_rename(src, dest)
            
        # logging
        rfh = RotatingFileHandler(filename="filenames.log",
                                mode='a',
                                maxBytes=32_768,
                                backupCount=2,
                                )
        
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s\n%(message)s\n',
                            datefmt='%m/%d/%Y %H:%M:%S',
                            handlers=[rfh],
                            )
        logger = logging.getLogger('FilenameChange')
        logger.info(popup_window.print_results())


        msg = f"Log file can be found at:\n{path.dirname(path.abspath(__file__))}"
        messagebox.showinfo("Results", msg)


    except FileNotFoundError:
        # TODO: prompt user for another attempt
        retry = messagebox.askretrycancel("Error", "Directory not found.\nDo you want to retry?")
        if retry:
            root.destroy()
            main()
        else:
            exit()
    


class RenameFiles(tk.Frame):
    """popup window to take directory information from user.
    User is to input abosolute path to folder containing files to be renamed into
    the text entry field, then press the "Rename Files" button.
    This assings RenameFiles.udir
    """

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.create_widgets()
        self.entry.focus()
        master.title("Batch Rename Files")
        master.geometry("520x120")
        master.bind("<Return>", lambda event: self.get_udir())
        master.bind("<Escape>", lambda event: self.quit())
        self.unchanged = []
        self.new_old = {}
        self.result_msg = ""
        self.udir = self.get_udir()
        # create list of years from 2020 - 2099
        self.years = [str(x) for x in range(2020, 2100)]
        self.state_abbreviations = [
                                    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
                                    "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
                                    "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
                                    "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
                                    "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY",
                                    "DC",
                                    # Territories
                                    "AS","GU","MP","PR","VI",
        ]
        # TODO: make sure "Return", "Return Payment", "EDI Return" don't conflict
        # TODO: make sure "Confirmation" and "EDI Confirmation" don't conflict
        self.doc_types = [
            "EDI Confirmation",
            "EDI Return",
            "Return Payment",
            "Return",
            "Confirmation",
        ]

    def create_widgets(self):
        self.prompt = tk.Label(
            self,
            text="Enter the directory with files to be renamed.\n"
            "All contents in this directory should need renaming.",
            font=("Arial", 12),
        )
        self.prompt.pack(side="top")

        self.entry = tk.Entry(
            self,
            width=55,
            font=("Arial", 12),
        )
        self.entry.pack(side="top", pady=5)

        self.b_confirm = tk.Button(
            self,
            text="Rename Files",
            command=self.get_udir,
            font=("Arial", 12),
        )
        self.b_confirm.pack(side="top", pady=10)
        
    def get_udir(self):
        self.udir = self.entry.get()
        self.quit()
        
    def print_results(self):
        """setup log file contents

        Returns:
            str: log message
        """
        for k,v in self.new_old.items():
            self.result_msg += f"Original name:\n{k}\nNew name:\n{v}\n\n"
        
        unchanged_list = '\n'.join(self.unchanged)
        if len(unchanged_list) > 0:
            self.result_msg += f"Filenames not changed:\n{unchanged_list}"
        return self.result_msg
        
    def make_new_name(self, ufile):
        """make a new name for ufile with specific criteria:
        <state&code>_<doc_type>_<date>
        strip everything else
        sometimes different format, noted in comments

        Args:
            ufile (str): name of file to rename
        Return:
            new_name (str): new name for file
        """

        # empty name list to be filled in with pertinent information
        new_name = []
        # special criteria for prepayments, may be changed in future
        is_prepayment = False
        is_repeat_doc = False

        # remove file extension, add back before return
        if "." in ufile:
            # keep extension to add later
            cut_point = ufile.index(".")
            extension = ufile[cut_point:]
            # remove extension
            ufile_noext = ufile[:cut_point]

        ufile_split = ufile_noext.split("~")

        for item in ufile_split:
            # check states (state abbreviation will be first 2 characters of item)
            try:
                if item[:2] in self.state_abbreviations:
                    if item[-1].isdigit():
                        # this indicates a prepayment - bool mark and keep number
                        is_prepayment = True
                        prepayment_num = item[-1]
                        # only save state abbrev for prepayments, remove the rest
                        state_code = item[:2]  # save item to put in new_name
                    else:
                        # save full state code for NON-prepayments only
                        state_code = item  # save item to put in new_name
            except IndexError:
                # not a state code, just pass
                pass

            # check if a dtype from doc_types is in the item
            for dtype in self.doc_types:
                if dtype in item:
                    # remove all digits and symbols around it,
                    # save item to put in new_name
                    document_type = item.strip(digits).strip(punctuation)

            # check if all digits (may be a date)
            if item.isdigit():
                try:
                    # check if first 4 digits are a valid year (range(2020, 2100))
                    if item[:4] in self.years:
                        document_date = item  # save item to put in new_name
                except IndexError:
                    # not a number from 2020 - 2099 (inclusive) so pass      
                    pass
            
            # check if lone digit, keep if >= 2
            if item.isdigit() and len(item) == 1:
                if int(item) >= 2:
                    is_repeat_doc = True
                    repeat_doc = item

        # add info to new_name in specified order
        # example if prepayment:
        # ND_Prepayment 1_EDI Return_202111
        # example if not prepayment:
        # ND_ST_SU_EDI Return_202111
        # NOTE: state_code includes codes other than state abbrev for NON-prepayments
        # NOTE: state_code is trimmed down to just the state abbrev ONLY for prepayments
        new_name.append(state_code)
        if is_prepayment:  # prepayments need extra tag
            new_name.append(f"Prepayment {prepayment_num}")
        new_name.append(document_type)
        new_name.append(document_date)
        if is_repeat_doc:
            new_name.append(repeat_doc)

        # join and add back file extension
        new_name = "_".join(new_name)
        new_name = f"{new_name}{extension}"
        return new_name

    def actually_rename(self, src, dest, n=0):
        """calls os.rename() and handles FileExistsError recursively

        Args:
            src (string): original file name (full path)
            dest (string): new file name (full path)
            n (int, optional): counter for end of duplicate names. Defaults to 0.
        """
        # FIXME: for multiple dupicates will put '(1) (2)' etc
        # TODO: should be fixed, make sure it is
        try:
            if n > 0:
                # check for file extension
                if "." in dest:
                    # find beginning of file extension, save it then cut from there to end
                    cut_point = dest.index(".")
                    extension = dest[cut_point:]
                    dest = dest[:cut_point].strip()
                # check for duplicate tag
                if "(" in dest:
                    # find beginning of dup tag, cut from there to end
                    cut_point = dest.index("(")
                    dest = dest[:cut_point].strip()

                # add dup tag and replace file extension then rename
                dest = f"{dest} ({n}){extension}"
                rename(src, dest)
            else:
                # first attempt to rename this file
                rename(src, dest)

        except FileExistsError:
            self.actually_rename(src, dest, n + 1)
        try:
            original_name = src[len(self.udir)+1:]
            final_name = dest[len(self.udir)+1:]
        except IndexError:
            messagebox.showerror('IndexError', 'Issue with original_name[] or '
                                 'final_name[] before adding to new_old{}')
            
        # don't overwrite values
        if original_name not in self.new_old.keys():
            self.new_old[original_name] = final_name
        

if __name__ == "__main__":
    main()
    