#!/bin/bash
echo "Please make sure you got your keypair in your host instance"
access_key_id= #put your key here
secret_access_key= #put your key here 
region='eu-central-1'
key_pair= #put your keypair here
if [ $(id -u) -ne 0 ]; then echo "Please run as root" ; exit 1 ; fi
aws --version
if [ $? -eq 0 ];then
	echo "aws cli installed"
else
	echo "installing  aws cli"
	curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
	unzip awscliv2.zip
	./aws/install
fi
cd $HOME
awsdir=".aws"
if [ ! -d $awsdir ];then
	mkdir $awsdir
fi
configfile=".aws/config"
if [ ! -f $configfile ];then
	touch $configfile
else
	echo "" > $configfile
fi
chmod 666 $configfile
/bin/cat << EOM >$configfile
[default]
region = $region
output = json
EOM

crenfile=".aws/credentials"
if [ ! -f $crenfile ];then
	touch $crenfile
else
	echo "" > $crenfile
fi
chmod 666 $crenfile
/bin/cat << EOM>$crenfile
[default]
aws_access_key_id = $access_key_id
aws_secret_access_key = $secret_access_key
EOM
echo "aws is now configured"
num_of_instances=2
image_id='ami-08c148bb835696b45'
aws ec2 run-instances --image-id $image_id  --count $num_of_instances  --instance-type t2.micro --key-name $key_pair  --security-group-ids default --user-data file:///root/apache.sh
