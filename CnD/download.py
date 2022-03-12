import urllib.request
import xlrd
loc = ("./Filename.xlsx") #Enter the file name of the .xlsx extension file for download

defectList=[]
errorList=[]

def download_file(download_url, filename):
    try:
        response = urllib.request.urlopen(download_url)
    except HTTPError as e:
        if e.code == 403:
            defectList.append(download_url)
            break
        else:

    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)

n=1

for i in range(sheet.nrows):
    pdf_path = sheet.cell_value(i,0)
    print(sheet.cell_value(i, 0))
    download_file(pdf_path,str(n))
    n+=1

with open("defectList3.txt","w") as file1:
    file1.write("Defect List \n")
    file1.write(defectList)
    file1.write("\n \n \n Errored List \n")
    file1.write(errorList)
