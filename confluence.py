import subprocess
import glob
import argparse
from atlassian import Confluence
import xml.etree.ElementTree as ET
from tabulate import tabulate
import os,time
import filecmp
from datetime import datetime
import requests
import json
import re
# pip3  install Atlassian-python-API
# apt install subversion
# pip3 install tabulate
# arparse , 6
# xml library


def execute_command():
    global command
    execute = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if execute.returncode == 1:
        print("Error " + str(execute.stdout))
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



list_of_dict = dict()

command = "svn log http://url "+ env + " --xml >  log.xml "
execute_command()

repo_command = "svn info http://url"+ env
output_repo_rev = subprocess.getoutput(repo_command)
l = re.search(r'Revision: (\d+)', output_repo_rev)
current_repo_rev = l.group(1)

html_content_latest  = "<p> Latest Repo Rev:" + current_repo_rev + " </p> "

confluence = Confluence(url="", username=username, password=password)
pageid = confluence.get_page_id('SWDO', env)


contentApiUrl = '/rest/api/content'
confluenceBaseUrl = ''
pageId = pageid

requestUrl = '{confluenceBaseUrl}{contentApiUrl}/{pageId}?expand=body.storage'.format(confluenceBaseUrl = confluenceBaseUrl, contentApiUrl = contentApiUrl, pageId = pageId)

requestResponse = requests.get(requestUrl, auth=(username, password))

respond = requestResponse.json()
respond_body = respond['body']
html_body = respond_body['storage']
html_content = html_body['value']
m = re.search(r'Latest Repo Rev:(\d*)', html_content)
if not m:
    latest_rev = 0
else:
    latest_rev = m.group(1)

if str(latest_rev) == current_repo_rev:
    print("No new revisions")
    exit()


final = [['Revision', 'Date', 'Description'],]


myDict = dict()

tree = ET.parse("./log.xml")
root = tree.getroot()


line_rev = {}
mylist = []
for elem in root.iter():
    if elem.tag == "logentry":
        if line_rev:
            mylist.append(line_rev)
            line_rev = {}
        revision = elem.attrib['revision']
        line_rev['revision'] = revision
    elif elem.tag == "date":
        datetime_object = datetime.strptime(elem.text, "%Y-%m-%dT%H:%M:%S.%fZ")
        datetime_change = datetime.strftime(datetime_object, "%Y-%m-%d %H:%M:%S")
        line_rev['date'] = str(datetime_change)
    elif elem.tag == "msg":
        line_rev['msg'] = elem.text




final_list = list()
for dict in mylist:
    final.append([dict['revision'],dict['date'],dict['msg']])







add = tabulate(final, tablefmt='html')

add = html_content_latest + add

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


