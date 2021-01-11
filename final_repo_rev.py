import subprocess
import glob
import argparse
from atlassian import Confluence
import xml.etree.ElementTree as ET
from datetime import datetime
from tabulate import tabulate
import os,time
from datetime import date
import filecmp
# pip3  install Atlassian-python-API
# apt install subversion
# pip3 install tabulate
# arparse , 6
# xml library


def execute_command():
    global command
    execute = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if execute.returncode == 1:
        print("Error")
        exit()



list_of_env = ['V12_beta','V11_beta','V10_beta','V12_prod','V11_prod','V12_test','V11_test']
parser = argparse.ArgumentParser()
parser.add_argument('-e', '--env', choices=list_of_env ,help="svn repo name", required=True)
parser.add_argument('-u', '--C_USER', help="user for confluence", required=True)
parser.add_argument('-p', '--C_PASS', help="password for confluence", required=True)
args = parser.parse_args()
username = args.C_USER
password = args.C_PASS

env = args.env
#env = "V12_beta"




now = datetime.now()

dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")




list_of_dict = dict()
all_files = glob.glob("./*.xml")
command = "svn log http://lachouffe/svn/"+ env + " --xml > log_"+dt_string+".xml"
execute_command()
new_file = command.split(">")[1]
new_file = new_file.replace(" ","")
new_file = "./" + new_file

#if rm command fails then take recent file
if len(all_files) > 1:
    for file in all_files:
        creation = time.ctime(os.path.getmtime(file))
        datetime_file = datetime.strptime(creation, "%a %b %d %H:%M:%S %Y")
        duration  = now - datetime_file
        list_of_dict[duration] = file

    shortest_duration = sorted(list_of_dict.keys())[0]
    file_to_cmp = list_of_dict[shortest_duration]
    comp = filecmp.cmp(file_to_cmp,new_file, shallow=False)
    if comp == True:
        print("There's been no change in reporev, exiting code")
        command = "rm -fr " + file_to_cmp
        execute_command()
        exit()



    elif comp == False:
        print("There's been change in reporev, proceeding code")
        command = "rm -fr " + file_to_cmp
        execute_command()


# suppose to swap one file everytime
elif len(all_files) == 1:
    file_to_cmp = all_files
    file_to_cmp = ''.join(file_to_cmp)
    comp = filecmp.cmp(file_to_cmp,new_file, shallow=False)
    if comp == True:
        print("There's been no change in reporev, exiting code")
        command = "rm -fr " + file_to_cmp
        execute_command()
        exit()



    elif comp == False:
        print("There's been change in reporev, proceeding code")
        command = "rm -fr " + file_to_cmp
        execute_command()



# first run
elif len(all_files) == 0:
    print("No files detected,proceeding to update the code")





confluence = Confluence(url="https://confluence.waves.com:8443", username=username, password=password)
pageid = confluence.get_page_id('SWDO', env)


final = [['Revision', 'Date', 'Description'],]

mylist = list()

myDict = dict()


tree = ET.parse(new_file)
root = tree.getroot()
for elem in root.iter():
    if elem.tag == "logentry":
        revision = elem.attrib['revision']
        myDict['revision']  = revision
    elif elem.tag == "date":
        date = elem.text
        datetime_object = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        myDict['date'] = str(datetime_object)
    elif elem.tag == "msg":
        msg = elem.text
        myDict['msg'] = msg
    if len(myDict.values()) == 3:
        mylist = list(myDict.values())
        final.append(mylist)
        myDict = dict()


add = tabulate(final, tablefmt='html')

print("Trying to update page...")

status = confluence.update_page(
    parent_id=66945868,
    page_id=pageid,
    title=env,
    body=add,
)

if status:
    print("Completed")
else:
    print("Error")


