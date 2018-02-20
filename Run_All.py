import os
import subprocess

#
# Calls a chapter executable
#
def RunChapterExample( program_name):
    print( "Running " + program_name)
    runpath = os.path.realpath(program_name)
    rundir = os.path.dirname(runpath)
    subprocess.call(runpath, shell=True, cwd=rundir)

f = open( "file_list.txt")
for i in range( 1000):
    s = f.readline()
    if len( s) <= 0: break
    s = s.strip()
    if s.startswith("#"): continue 
    RunChapterExample( s)

