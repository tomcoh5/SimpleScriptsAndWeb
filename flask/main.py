from flask import Flask, request, render_template, redirect, url_for
import subprocess
app = Flask(__name__)

def deploycommand():
    global bashcommand
    global process
    try:
        process = subprocess.Popen(bashcommand.split(), stdout=subprocess.PIPE)
        return "deployed.. "
    except:
        return "Error cant deploy"



@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    if text =="1":
        return redirect("http://localhost:5000/container")
    else:
        return "Error 404"


@app.route('/container')
def plz():
    return render_template('container.html')

@app.route('/container', methods=['POST'])
def plz_post():
    global define
    global image
    global name
    global bashcommand
    define = request.form['text']
    arrange = define.split()
    image = arrange[0]
    name = arrange[1]
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
            bashcommand = "docker run -d --name " + name + " " + image
            deploycommand()

    return redirect("http://localhost:5000/deployment")


@app.route('/deployment', methods=['POST'])
def ports():
    return render_template()

if __name__ == "__main__":
    app.run(debug=True)



#some functions to make it easy



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
