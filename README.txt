Please ensure your metadata variable name syntax matches the data variable names exactly.

Please ensure your metadata names variable names and descriptions as "var_name" and "var_label".

Please ensure encoding of csv is utf-8.

To include your own keywords in the metadata search, edit custom_varlabel_recogniser.py and add a new Pattern in the same format as the current code. It is case-insensitive so just name the pattern and put in the keyword within the regex line e.g.  regex =r"(?i)(?:^|\W)insert your keyword here(?:$|\W)"






