import os
import sys
import shutil


def GetSource():
    if len( sys.argv) <= 2:
        print("Usage:")
        print("Propagate <source_folder> <file_name> [start_folder]")
        return None, None, 3
    Source_Folder = sys.argv[1]
    Source_File = sys.argv[2]
    Start_Folder = 3
    if len(sys.argv) >= 4:
        try:
            Start_Folder = int( sys.argv[3])
        except:
            print("[start_folder] must be a number")
            return None, None, 3
    if not '.' in Source_File: Source_File += ".py" 
    try:
        n = int(Source_Folder)
        Full_Name = "./Chapter {:02d}/{:s}".format(n, Source_File)
    except:
        Full_Name = "./{:s}/{:s}".format(Source_Folder, Source_File)
    if not os.path.exists(Full_Name):
        print("File not found: {:s}".format(Full_Name))
        return None, None, 3
    print("Propagating {:s}:".format(Full_Name))
    return Full_Name, Source_File, Start_Folder


def CopyToAllFolders(Source_Name, Destination_Name, Start_Folder):
    if Source_Name is None: return
    if Destination_Name is None: return
    for chapterNumber in range(Start_Folder,100):
        dest_name = "./Chapter {:02d}/".format(chapterNumber)
        if not os.path.exists(dest_name): continue
        dest_name += Destination_Name
        if dest_name == Source_Name: continue 
        if not os.path.exists(dest_name):
            print(" * {:s} - not at destination".format(dest_name))
            continue
        try:
            shutil.copy( Source_Name, dest_name)
            print("   {:s}".format(dest_name))
        except:
            print(" * {:s} - failed to copy".format(dest_name))


a, b, n = GetSource()
CopyToAllFolders( a, b, n)
