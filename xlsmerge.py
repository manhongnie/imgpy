
import os
import pandas as pd
import xlrd
import xlsxwriter
from texttable import Texttable

def getfiles(path):
    exlist = os.listdir(path)
    df = []
    outfile = "outfile"
    outpath = os.path.join(path, outfile)
    isExists = os.path.exists(outpath)
    if not isExists:
        os.makedirs(outpath)
    else:
        print(path + ' 目录已存在')
    newname = "newfile.xlsx"

    newfilename = os.path.join(outpath, newname)
    for k, file in enumerate(exlist):
        if os.path.splitext(file)[1] == '.xlsx':
            #dataframe = pd.read_excel(os.path.join(path, file), 1)
            data = pd.DataFrame(pd.read_excel(os.path.join(path, file), 1))
            df.append(data)
    res = pd.merge(df[0], df[1])
    tb = Texttable()
    tb.set_cols_align(['l', 'r', 'r'])
    tb.set_cols_dtype(['t', 'i', 'i'])
    tb.header(df.columns.get_values())
    tb.add_rows(df.values, header=False)
    print(tb.draw())
    pd.display(res.head())
    #writer = pd.ExcelWriter(newfilename)
    #pd.concat(newl).to_excel(writer, 'mm', index=False)

if __name__ == "__main__":
    path = 'D:/exhebing'
    getfiles(path)


