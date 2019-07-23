from os import listdir, remove
from os.path import isfile, join, exists
import sys
import shutil

def GetNames(Source_Folder):
    return [f for f in listdir(Source_Folder) if isfile(join(Source_Folder, f))]

def DeleteInFolder(Name, Folder):
    dest_name = join(Folder, Name)
    if not exists(dest_name): return
    remove( dest_name)
    print("Deleted: {:s}".format(dest_name))

def DeleteInAllChapters( Name):
    if Name is None: return
    for chapterNumber in range(1,100):
        dest_name = "./Chapter {:02d}/".format(chapterNumber)
        if not exists(dest_name): continue
        DeleteInFolder(Name, dest_name)
        DeleteInFolder(Name, dest_name + "/Data/")

Names = GetNames( "./Global Data/")
for n in Names:
    DeleteInAllChapters(n)
