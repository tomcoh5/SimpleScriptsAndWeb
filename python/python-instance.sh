#!/bin/bash
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
pip install boto3
python <<END_OF_PYTHON
import boto3
ec2 = boto3.resource('ec2')

outfile = open('ec2-keypair.pem','w')
key_pair = ec2.create_key_pair(KeyName='ec2-keypair')

KeyPairOut = str(key_pair.key_material)
print(KeyPairOut)
outfile.write(KeyPairOut)
END_OF_PYTHON
chmod 400 ec2-key_pair.pem

python << END_OF_PY
import boto3
ec2 = boto3.resource('ec2')

# create a new EC2 instance
instances = ec2.create_instances(
     ImageId='ami-00b6a8a2bd28daf19',
     MinCount=1,
     MaxCount=2,
     InstanceType='t2.micro',
     KeyName='ec2-keypair'
 )

 END_OF_PY
