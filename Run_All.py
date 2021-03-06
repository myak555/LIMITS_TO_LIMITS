import os
import sys
import subprocess


def RunChapterExample(program_name, report_file):
    """
    Calls a chapter executable
    """
    runpath = os.path.realpath(program_name)
    rundir = os.path.dirname(runpath)
    progname = os.path.basename(runpath)
    print("Running " + program_name)
    report_file.write("#\n".encode("cp1252"))
    report_file.write("# Executing {:s}\n".
                      format(program_name).
                      encode("cp1252"))
    report_file.write("#\n".encode("cp1252"))
    if sys.platform.lower().startswith('win'):
        command = ['{:s}'.format(progname), '-t']
    else:
        command = ['python3 "{:s}" -t'.format(progname)]
    p = subprocess.Popen(
        command,
        shell=True,
        cwd=rundir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    output, err = p.communicate()
    i = p.returncode
    if i != 0:
        print("Returned error: {:d}".format(i))
        report_file.write(err)
        return True
    report_file.write(output)
    return False


File_Mask = None
if len(sys.argv) >= 2:
    File_Mask = sys.argv[1]

f1 = open("file_list.txt")
f2 = open("test_report.txt", "wb")
failCount = 0
totalCount = 0
for i in range(1000):
    s = f1.readline()
    if len(s) <= 0:
        break
    s = s.strip()
    if s.startswith("#"):
        continue
    if File_Mask is not None and File_Mask not in s:
        continue
    if RunChapterExample(s, f2):
        failCount += 1
    totalCount += 1
f1.close()
f2.close()
if failCount == 0:
    print("Executed {:d}, no failures.".format(totalCount))
else:
    print("Executed {:d}, failed {:d}.".format(totalCount, failCount))
