# filename_change_zack

Automate specific filename changes requested by Zack

Cleans up verbose filenames - replace with simple ones that only contain specified pertinent information

## Changes to filenames

Filename items in order after rename:  
\<State abbreviation\>\_\<document codes\>\_\<document type\>\_\<date\>

If the filename has a number at the end of the document codes, it is a prepayment. Prepayment filenames are given a different format:  
\<State abbreviation\>\_\<Prepayment \#\>\_\<document type\>\_\<date\>

All numbers besides dates are removed in either case, with the exception of prepayment numbers.

## How to use

Run main. It will open a popup box asking for a directory. Provide the full path to a folder containing files that need their names trimmed down. Click the Rename Files button and it will do just that, then close.

## Disclaimer

This is made for a very specific use case and will not work for filenames that do not follow the pattern specified by the client. I do not take responsibility for lost data or otherwise unexpected behavior. Run at your own risk.
