#!/bin/bash
cd $HOME
echo "Hey lets run terraform"
terraform init
if [ ! -f apache.sh ];then
    touch apache.sh
else
    echo "" > apache.sh
fi
touch apache.sh
/bin/cat << EOF > apache.sh
#!/bin/bash
sudo apt-get update -y 
sudo apt install apache2 -y 
sudo systemctl start apache2 
sudo systemctl enable apache2
echo "<h1>Deployed via Terraform</h1>" | sudo tee /var/www/html/index.html
EOF
EOF
if [ ! -f terraformfile ];then
    touch $terraformfile
else
    echo "" > $terraformfile
fi 
/bin/cat << EOM >$terraformfile
provider "aws" {
  region = "$region"
}
resource "aws_instance" "web" {
  ami           = $ami
  instance_type = "t2.micro"
  key_name= $key_pair_name
  user_data = "${file("apache.sh")}"


  tags = {
    Name = "$name"
  }
EOM
terraform apply
