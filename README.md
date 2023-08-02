# filename_changes

Automate specific filename changes requested by Zack

Cleans up verbose filenames - replace with simple ones that only contain specified pertinent information

## Changes to filenames

Filename items in order after rename:  
\<State abbreviation\>\_\<document codes\>\_\<document type\>\_\<date\>

If the filename has a number at the end of the document codes, it is a prepayment. Prepayment filenames are given a slightly different format:  
\<State abbreviation\>\_\<Prepayment \#\>\_\<document type\>\_\<date\>

All numbers besides dates are removed in either case, with the exception of prepayment numbers and occasionally a lone number indicating a connection with another file. In this relatively rare case this lone number is tacked onto the end just before the file extension.

## How to use

Run FilenameChange.py or FilenameChange.exe, whichever is applicable. It will open a popup box asking for a directory. Provide the full path to a folder containing files that need their names trimmed down. Click the Rename Files button and it will do just that, then close. A log entry will be made each time listing the original filenames, the new names they were given, and any filenames that were not changed.
