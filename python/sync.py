from pathlib import Path
import logging
import subprocess
import shutil
import os
import argparse
import re
import xml.etree.ElementTree as ET



current_pid = os.getpid()
logging.basicConfig(filename = str(current_pid) + ".log", level=logging.INFO)

parser = argparse.ArgumentParser()
list_of_repos = ['']

parser.add_argument('-s', '--source_repo', choices=list_of_repos,help="Source repo name ", required=True)
parser.add_argument('-t', '--target_repo', choices=list_of_repos,help="Target repo name ", required=True)
parser.add_argument('-m', '--message', help="custom message for svn commit", required=False)
args = parser.parse_args()
message = args.message
target_repo = args.target_repo
source_repo = args.sorce_repo

if target_repo == source_repo:
    print("Error target_repo and source_repo arguments are identical")

home = str(Path.home())
target_path = home + "/"+target_repo+"/"
source_path = home + "/"+source_repo+"/"
svn_repos = {}




def get_resources():
    svn_repo_list = [target_repo, source_repo]
    for repo_name in svn_repo_list:
        print("Executing : " + repo_name + " svn checkout")
        logging.info("Executing : " + repo_name + " svn checkout")
        execute = subprocess.run("svn checkout " + repo_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if execute.returncode == 1:
            print("Error in  " + repo_name + " " + str(execute.stdout))
            print(str(execute.stderr))
            logging.info("Error in  : " + repo_name + " " + str(execute.stdout))
            exit()




def sync_all():
    #syncs all
    count = 0
    folders = ['Common', 'Win', 'Mac']
    for folder in folders:
        print("Copy: " + source_path + folder + " To: " + target_path + folder)
        if os.path.isdir(target_path + folder) == True:
            shutil.rmtree(target_path + folder)
            print("Removing" + target_path + folder)
            logging.info("Removing" + target_path + folder)
            shutil.copytree(source_path + folder, target_path + folder)
            logging.info("Copying :" + source_path + folder, target_path + folder)
         # copies premission also https://docs.python.org/3/library/shutil.html#shutil.copystat

        else:
            shutil.copytree(source_path + folder, target_path + folder)
            logging.info("Copying :" + source_path + folder, target_path + folder)

    print("Completed")
    logging.info("Completed")
    print("Copying & editing index file")
    logging.info("Copying & editing index file")
    shutil.copyfile(source_path + "/instl/index.yaml", target_path + "/instl/index.yaml")
    logging.info("Copying" + source_path + "/instl/index.yaml", target_path + "/instl/index.yaml")
    logging.info("reading index.yaml")
    print("reading index.yaml")
    with open(target_path + "/instl/index.yaml", 'r') as file:
        file_data = file.read()

    file_data = file_data.replace(svn_repos[source_repo], svn_repos[target_repo])

    with open(target_path + "/instl/index.yaml", 'w') as file:
        file.write(file_data)

def commit():
  global message
  current_repo_in_svn = subprocess.getoutput("svn info " + target_path)
  find_repo_rev_num = re.search(r'Revision: (\d+)', current_repo_in_svn)
  current_repo_rev_num = find_repo_rev_num.group(1)
  if not current_repo_rev_num:
      print("Error Cant find current repo rev number")
      exit()
  print("Current revision before commit: " + current_repo_rev_num)
  logging.info("Current revision before commit: " + current_repo_rev_num)
  print("Commit to svn " + target_repo)
  logging.info("Commit to svn " + target_repo)
  if message:
      print("Custom message for commit " + message )
      logging.info("Custom message for commit " + message )
  else:
      get_last_message = subprocess.run("svn log " + source_repo + " -l 1 --xml > log.xml ",shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      logging.info("Getting svn log for " + source_repo)
      if get_last_message.returncode == 1:
          print("Error getting svn log " + str(get_last_message))
          print(str(get_last_message.stderr))
          logging.info("Error getting svn log" + str(get_last_message))
          exit()
      tree = ET.parse("./log.xml")
      root = tree.getroot()
      for elem in root.iter():
          if elem.tag == "msg":
             message = "Deployed to " + target_repo +" automatically by Jenkins : " + elem.text
  svn_command = subprocess.run('svn commit -m ' + message, cwd=target_path,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  if svn_command.returncode == 1:
   print("Error " + str(svn_command.stdout))
   logging.info("Error " + str(svn_command.stdout))
   print(str(svn_command.stderr))
   exit()
  elif svn_command.returncode == 0:
      current_repo_rev_num = int(current_repo_rev_num)
      current_repo_rev_num += 1
      print("Commit end repo rev number after commit " + str(current_repo_rev_num))
      logging.info("Commit end repo rev number after commit " + str(current_repo_rev_num))

#get_resources()
#sync_all()
#commit()
#if the entire script doesnt work then, svn checkout $reponame , svn update -r <earlier_revision_number>, svn commit


