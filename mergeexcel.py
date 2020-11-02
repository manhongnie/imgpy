
import os
import xlrd
import xlsxwriter
import pandas as pd

# def getfiles(path):
#     rvale = []
#     exlist = os.listdir(path)
#     for file in exlist:
#         if os.path.splitext(file)[1] == '.xlsx':
#             f = xlrd.open_workbook(os.path.join(path, file))
#             table = f.sheets()[1]
#             numy = table.ncols
#             numx = table.nrows
#             print(numx)
#             for row in range(numx):
#                 rdata = table.row_values(row)
#                 rvale.append(rdata)
    #return rvale
                #print(rdata)

# def getfiles(path):
#     exlist = os.listdir(path)
#     gsm = []
#     mgsm = []
#     xmmc = []
#     for k, file in enumerate(exlist):
#         if os.path.splitext(file)[1] == '.xlsx':
#             data = pd.DataFrame(pd.read_excel(os.path.join(path, file), 1))
#             #print(data['公司名称'])
#             gsm.append(data['公司名称'].values)
#
#             for c in range(len(gsm[k])):
#                 mgsm.append(gsm[k][c])
#     mgsms = list(set(mgsm))
def mergexls(path):
    exlist = os.listdir(path)
    outfile = "outfile"
    outpath = os.path.join(path, outfile)
    isExists = os.path.exists(outpath)
    if not isExists:
        os.makedirs(outpath)
    else:
        print(path + ' 目录已存在')
    newname = "newfile.xlsx"
    newfilename = os.path.join(outpath, newname)
    newl = []
    for k, file in enumerate(exlist):
        if os.path.splitext(file)[1] == '.xlsx':
            dataframe = pd.read_excel(os.path.join(path, file), 1)
            data = pd.DataFrame(dataframe)
            newl.append(data)
    writer = pd.ExcelWriter(newfilename)
    pd.concat(newl).to_excel(writer, 'mm', index=False)
    writer.save()
    mergeend(newfilename)
def mergeend(file):
    gx = []
    gxs = []
    counts = []

    xm = []

    data = pd.DataFrame(pd.read_excel(file))
    dataf = pd.read_excel(file)
    print(dataf.columns)
    #print(dataf['项目名称'])
    gx.append(data['公司名称'].values)
    xm.append(data['项目名称'].values)
    for
    #mm = list(set(gx))
    #print(len(gx))
    for c in range(len(gx[0])):
        #print(len(gx[0]))
        #print(len(xm[0]))
        gxs.append(gx[0][c])
    mm = list(set(gxs))
    for k in range(len(mm)):
        first_pos = 0
        for i in range(gxs.count(mm[k])):
            gs = []
            #if int(gxs.count(mm[0])) > 1:
                #print(gxs.count(mm[0]))
            new_list = gxs[first_pos:]
            next_pos = new_list.index(mm[k]) + 1
            print("pos : ", first_pos + new_list.index(mm[k]))
            gs.append(first_pos + new_list.index(mm[k]))
            first_pos += next_pos

        counts.append(gs)

    #print(len(counts))
    #print(gxs.index(mm[0]))
    #print(sum(counts))
            #dataf.loc(mm[k])
            #print("11111111")
    #print(len(mm))
if __name__ == "__main__":
    path = 'D:/exhebing'
    #getfiles(path)
    mergexls(path)


