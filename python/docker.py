import subprocess
running = True


def dockercontainer():
    global running
    global bashcommand
    image = input("Tell me what image you want for your docker container")
    name = input("and also write a name for your container ")
    if image == "quit":
        running = False
    else:
        if image == "apache" or image == "nginx" or image == "httpd":
            bashcommand = "docker run -d --name " + name + " -p 8080:8080 " + image
            deploycommand()
        elif image == "grafana":
            bashcommand = "docker run -d -p 3000:3000 " + image
            deploycommand()
        elif image == "postgresql" or image == "postgres":
            password = input("write down password for your database")
            bashcommand = "docker run --name " + name + " -e POSTGRES_PASSWORD=" + password + " -d postgres"
            deploycommand()
        elif image == "mysql":
            password = input("write down password for your database")
            bashcommand = "docker run --name " + name + " MYSQL_ROOT_PASSWORD=" + password + " -d mysql"
            deploycommand()
        else:
            tellme = input("Do you need port for your image?")
            if tellme == "quit":
                running = False
            elif tellme == "yes":
                port = input("Write Down the port")
                bashcommand = "docker run -d --name " + name + " -p " + port + "  " + image
                deploycommand()
            elif tellme == "no":
                print("Lets run your container")
                bashcommand = "docker run -d --name " + name + " " +  image
                deploycommand()
def deploycommand():
    global bashcommand
    try:
        process = subprocess.Popen(bashcommand.split(), stdout=subprocess.PIPE)
        print("deployed.. ")
    except:
        print("Error cant deploy")
        end()

def end():
    global running
    now= input("okay you want to keep deploying containers or exit ?")
    if now == "exit":
        running = False

def docker_compose():
    global running
    global bashcommand
    print("Lets start by adding images")
    images_number = input("how much containers do you want ? ")
    network = input("Creating network for your containers enter a name ")
    bashcommand = "docker network create " + network
    deploycommand()
    maxlengthlist = int(images_number)
    counter = 0
    while counter  < maxlengthlist:
        global network
        global name
        image = input("Tell me what image you want for your docker container")
        name = input("and also write a name for your container ")
        if image == "quit":
            running = False
        else:
            if image == "apache" or image == "nginx" or image == "httpd":
                bashcommand = "docker run -d --name " + name +  " --network " + network + " -p 8080:8080 " + image
                deploycommand()
            elif image == "grafana":
                bashcommand = "docker run -d -p 3000:3000 " + image
                deploycommand()
            elif image == "postgresql" or image == "postgres":
                password = input("write down password for your database")
                bashcommand = "docker run --name " + name + " --network " + network + " -e POSTGRES_PASSWORD=" + password + " -d postgres"
                deploycommand()
            elif image == "mysql":
                password = input("write down password for your database")
                bashcommand = "docker run --name " + name + " --network " + network + "MYSQL_ROOT_PASSWORD=" + password + " -d mysql"
                deploycommand()
            else:
                tellme = input("Do you need port for your image?")
                if tellme == "quit":
                    running = False
                elif tellme == "yes":
                    port = input("Write Down the port")
                    bashcommand = "docker run -d --name " + name + "--network " + network + " -p " + port + "  " + image
                    deploycommand()
                elif tellme == "no":
                    print("Lets run your container")
                    bashcommand = "docker run -d --name " + name + " " + "--netowrk " + network + + image
                    deploycommand()
        counter += 1
    end()

def dockerbuild ():
    global running
    global bashcommand
    path = input("Write down the path to your docker file")
    bashcommand = "cd " + path
    deploycommand()
    name = input("name for your docker image?")
    bashcommand = "docker build -t " + name + "."
    deploycommand()

while running:
    print("welcome, developer")
    choose= input("If you want do deploy only one container press 1 \n"
                  " if you want to deploy a lot of  containers (connected) press 2 \n"
                  "if you want to build your image and deploy it press 3")
    if choose == "1":
        dockercontainer()
    elif choose == "2":
        docker_compose()
    elif choose == "3":
        print("okay")

    elif choose == "quit":
        running = False

