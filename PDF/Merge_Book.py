from PyPDF2 import PdfFileMerger, PdfFileReader

filenames = []
filenames +=["Ch_00"]
filenames +=["Ch_01"]
filenames +=["Ch_02"]
filenames +=["Ch_03"]
filenames +=["Ch_04"]
filenames +=["Ch_05"]
filenames +=["Ch_06"]
filenames +=["Ch_07"]
filenames +=["Ch_08"]
filenames +=["Ch_09"]
filenames +=["Ch_10"]
filenames +=["Ch_11"]
filenames +=["Ch_12"]
filenames +=["Ch_13"]
filenames +=["Ch_14"]
filenames +=["Ch_15"]
filenames +=["Ch_16"]
filenames +=["Ch_17"]
filenames +=["Ch_18"]
filenames +=["Ch_19"]
filenames +=["Ch_20"]
filenames +=["Ch_99"]

merger = PdfFileMerger()
for filename in filenames:
    merger.append(PdfFileReader(filename + '.pdf'))

merger.write("M_Yakimov_Limits_To_Limits.pdf")
