import csv
import os

def format_table(text, **options):
    """
    source: https://stackoverflow.com/questions/20025235/how-to-pretty-print-a-csv-file-in-python

    @summary:
        Reads a CSV file and prints visually the data as table to a new file.
    @param filename:
        is the path to the given CSV file.
    @param **options:
        the union of Python's Standard Library csv module Dialects and Formatting Parameters and the following list:
    @param new_delimiter:
        the new column separator (default " | ")
    @param bdr:
        boolean value if you want to print the bdr of the table (default True)
    @param bdr_vertical_left:
        the left bdr of the table (default "| ")
    @param bdr_vertical_right:
        the right bdr of the table (default " |")
    @param bdr_horizontal:
        the top and bottom bdr of the table (default "-")
    @param bdr_corner_tl:
        the top-left corner of the table (default "+ ")
    @param bdr_corner_tr:
        the top-right corner of the table (default " +")
    @param bdr_corner_bl:
        the bottom-left corner of the table (default same as bdr_corner_tl)
    @param bdr_corner_br:
        the bottom-right corner of the table (default same as bdr_corner_tr)
    @param header:
        boolean value if the first row is a table header (default True)
    @param bdr_header_separator:
        the bdr between the header and the table (default same as bdr_horizontal)
    @param bdr_header_left:
        the left bdr of the table header (default same as bdr_corner_tl)
    @param bdr_header_right:
        the right bdr of the table header (default same as bdr_corner_tr)
    @param newline:
        defines how the rows of the table will be separated (default "\n")
    @param new_filename:
        the new file's filename (*default* "/new_" + filename)
    """

    #function specific options
    new_delimiter           = options.pop("new_delimiter", " | ")
    bdr                  = options.pop("bdr", True)
    bdr_vertical_left    = options.pop("bdr_vertical_left", "| ")
    bdr_vertical_right   = options.pop("bdr_vertical_right", " |")
    bdr_horizontal       = options.pop("bdr_horizontal", "-")
    bdr_corner_tl        = options.pop("bdr_corner_tl", "+ ")
    bdr_corner_tr        = options.pop("bdr_corner_tr", " +")
    bdr_corner_bl        = options.pop("bdr_corner_bl", bdr_corner_tl)
    bdr_corner_br        = options.pop("bdr_corner_br", bdr_corner_tr)
    header                  = options.pop("header", True)
    bdr_header_separator = options.pop("bdr_header_separator", bdr_horizontal)
    bdr_header_left      = options.pop("bdr_header_left", bdr_corner_tl)
    bdr_header_right     = options.pop("bdr_header_right", bdr_corner_tr)
    newline                 = options.pop("newline", "\n")

    # file_path = filename.split(os.sep)
    # old_filename = file_path[-1]
    # new_filename            = options.pop("new_filename", "new_" + old_filename)

    column_max_width = {} #key:column number, the max width of each column
    num_rows = 0 #the number of rows

    # with open(filename, "rb") as input: #parse the file and determine the width of each column
    reader=csv.reader(text, **options)
    for row in reader:
        num_rows += 1
        for col_number, column in enumerate(row):
            width = len(column)
            try:
                if width > column_max_width[col_number]:
                    column_max_width[col_number] = width
            except KeyError:
                column_max_width[col_number] = width

    max_columns = max(column_max_width.keys()) + 1 #the max number of columns (having rows with different number of columns is no problem)

    if max_columns > 1:
        total_length = sum(column_max_width.values()) + len(new_delimiter) * (max_columns - 1)
        left = bdr_vertical_left if bdr is True else ""
        right = bdr_vertical_right if bdr is True else ""
        left_header = bdr_header_left if bdr is True else ""
        right_header = bdr_header_right if bdr is True else ""

        # with open(filename, "rb") as input:
        reader=csv.reader(text, **options)
        output = ""
        # with open(new_filename, "w") as output:
        for row_number, row in enumerate(reader):
            max_index = len(row) - 1
            for index in range(max_columns):
                if index > max_index:
                    row.append(' ' * column_max_width[index]) #append empty columns
                else:
                    diff = column_max_width[index] - len(row[index])
                    row[index] = row[index] + ' ' * diff #append spaces to fit the max width

            if row_number==0 and bdr is True: #draw top bdr
                "".join((output,bdr_corner_tl + bdr_horizontal * total_length + bdr_corner_tr + newline))

            "".join((output,
                left + new_delimiter.join(row) + right + newline)) #print the new row

            if row_number==0 and header is True: #draw header's separator
                "".join((output,
                    left_header + bdr_header_separator * total_length + right_header + newline))

            if row_number==num_rows-1 and bdr is True: #draw bottom bdr
                "".join((output,
                    bdr_corner_bl + bdr_horizontal * total_length + bdr_corner_br))

