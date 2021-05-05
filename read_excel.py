import xlrd
from datetime import datetime


# function reads in information in an excel file
def read_excel(file_path, sheet_name):
    # excel file path
    myFile = xlrd.open_workbook(file_path)
    # add sheet path
    sheet2 = myFile.sheet_by_name(sheet_name)

    # start reading file:
    i = 1
    all_rows = []  # all_rows store all info in the excel file

    while i < sheet2.nrows:
        # read line by line
        one_row = sheet2.row_values(i)

        # convert numbers to float
        one_row[0] = float(one_row[0])
        one_row[2] = float(one_row[2])
        one_row[3] = float(one_row[3])

        # add each row to all_rows
        all_rows.append(one_row)
        i += 1

    return all_rows


# function computes the difference between two time stamp
def cal_time(time1, time2):
    time1 = datetime.strptime(time1, "%Y/%m/%d %H:%M")  # :%S")
    time2 = datetime.strptime(time2, "%Y/%m/%d %H:%M")  # :%S")
    return (time2-time1).seconds


"""
if __name__ == "__main__":
    print(read_excel("test_update.xlsx", "test")[0], read_excel("test_update.xlsx", "test")[1])
    print(cal_time(read_excel("test_update.xlsx", "test")[1][1], read_excel("test_update.xlsx", "test")[0][1]))
"""