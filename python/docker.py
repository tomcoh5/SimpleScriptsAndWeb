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
            print("port for your dockerfile -is ")
            bashcommand = "docker run -d -p 8080:8080 " + image
            deployforcontainer()
        elif image == "grafana":
            bashcommand = "docker run -d -p 3000:3000 " + image
            deployforcontainer()
        elif image == "postgresql" or image == "postgres":
            password = input("write down password for your database")
            bashcommand = "docker run --name " + name + " -e POSTGRES_PASSWORD=" + password + " -d postgres"
            deployforcontainer()
        elif image == "mysql":
            password = input("write down password for your database")
            bashcommand = "docker run --name " + name + " MYSQL_ROOT_PASSWORD=" + password + " -d mysql"
            deployforcontainer()
        else:
            tellme = input("Do you need port for your image?")
            if tellme == "quit":
                running = False
            elif tellme == "yes":
                port = input("Write Down the port")
                bashcommand = "docker run -d -p " + port + "  " + image
                deployforcontainer()
            elif tellme == "no":
                print("Lets run your container")
                bashcommand = "docker run -d " + image
                deployforcontainer()

def deployforcontainer():
    global bashcommand
    try:
        process = subprocess.Popen(bashcommand.split(), stdout=subprocess.PIPE)
        print("deployed.. ")

def docker_compose():
    global running
    images = input("Okay write down all of your images")
    image_list = list()
    for image in images:
        image_list.append(image)
    print("Done proecessing....")
    print(image_list)



while running:
    print("welcome, developer")
    choose= input("If you want do deploy only one container press 1, if you want to deploy more then one container press 2")
    if choose == "1":
        dockercontainer()
    elif choose == "2":
        docker_compose()

