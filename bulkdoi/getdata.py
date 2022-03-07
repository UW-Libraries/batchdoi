import openpyxl

wb = openpyxl.load_workbook(filename = 'doitest.xlsx')
sh = wb.active
#print(sheet['A1'].value)

data = []
revised_headers = ['url', 'creators', 'title', 'publisher', 'pubyear', 'restype', 'description']
expected_headers = ['URL', 'Creators', 'Title', 'Publisher', 'Publication Year', 'Resource Type', 'Description']
headers = []
for i in range(1, sh.max_column+1):
    cell_obj = sh.cell(row=1, column=i)
    if cell_obj.value is None: break
    headers.append(cell_obj.value)
numcols = len(headers)

for row in sh.iter_rows(min_row=2):
    rowdata = []
    if row[0].value:
        for idx in range(numcols):
            cellval = row[idx].value
            if cellval is None:
                rowdata.append('')
            else:
                rowdata.append(row[idx].value)
    if rowdata:
        data.append(dict(zip(headers, rowdata)))

print(data)
