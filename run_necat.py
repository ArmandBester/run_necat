#! /usr/bin/env python3

import os
from glob import glob
from subprocess import PIPE, Popen

# point to the project directory
folder = 'necat_in_test'


folders_w_data = []
jobList = []

# discover
for root, dirs, files in os.walk(folder):
    for f in files:
        #print(root)
        absPath = os.path.join(os.getcwd(), root)
        if absPath not in folders_w_data:
            folders_w_data.append(absPath)

# readlists
for d in folders_w_data:
    name = os.path.split(d)[-1]
    name = name + "_readList.txt"
    outF = os.path.join(d, name)

    with open(outF, 'w') as readList:
        dataList = glob(f'{d}/*fa*')
        for fastq in dataList:
            readList.write(f'{fastq}\n')

# configs
for d in folders_w_data:
    sample = open('sample_config.txt', 'r').read()
    name = os.path.split(d)[-1]
    fileName = name + "_config.txt"
    outF = os.path.join(d, fileName)
    jobList.append(outF)
    with open(outF, 'w') as conf:
        newConf = sample.replace("PROJECT=", f'PROJECT={name}')
        newConf = newConf.replace("ONT_READ_LIST=", f'ONT_READ_LIST={outF.replace("_config.txt", "_readList.txt")}')

        conf.write(newConf)

# run the jobs
for job in jobList:
    print(f'Running necat {job}')
    necatCmd = f'necat.pl bridge {job}'  ## define the necat command
    process = Popen(necatCmd, shell=True ,stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    ## look for Abort in the stdout
    if "Abort" in stdout.decode("utf-8"):
        print("X------> Seems something went wrong\n")
    else:
        print("OK\n")
