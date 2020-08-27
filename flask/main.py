from flask import Flask, request, render_template, redirect, url_for
import subprocess
import urllib.request

ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')

app = Flask(__name__)


def deploycommand2(command):
    global bashcommand
    global process
    try:
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        return "deployed.. "
    except:
        return "Error cant deploy"



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
    if text == "1":
        return redirect("http://" + ip + ":5000/container")
    elif text == "2":
        return redirect("http://" + ip + ":5000/multi")
    else:
        return "Error 404"


@app.route('/multi')
def multi():
    return render_template('multi.html')


@app.route('/multi', methods=['POST', 'GET'])
def multi_post():
    global network
    global bashcommand
    network = request.form['text']
    bashcommand = "docker create network " + network
    deploycommand()
    return redirect("http://" + ip + ":5000/objects")


@app.route('/objects')
def objects():
    return render_template('objects.html')

def test():
    global password
    password_post()
    return redirect("http://" + ip + ":5000/objects")



@app.route('/objects', methods=['POST', 'GET'])
def objects_post():
    global image
    global name
    global bashcommand
    global network
    global password
    define = request.form['text']
    while True:
        arrange = define.split()
        image = arrange[0]
        name = arrange[1]
        if image == "apache" or image == "nginx" or image == "httpd":
            bashcommand = "docker run -d --name " + name + " -p 8080:8080 " + image
            deploycommand()
            return redirect("http://" + ip + ":5000/objects")
        elif image == "grafana":
            bashcommand = "docker run -d -p 3000:3000 " + image
            deploycommand()
            return redirect("http://" + ip + ":5000/objects")
        elif image == "postgresql" or image == "postgres":
            return redirect("http://" + ip + ":5000/passwordpost2")
        elif image == "mysql":
            bashcommand = "docker run --name " + name + " MYSQL_ROOT_PASSWORD=" + password + " -d mysql"
            return redirect("http://" + ip + ":5000/passwordmysql")
        else:
            return redirect("http://" + ip + ":5000/deployment")



@app.route('/container')
def plz():
    return render_template('container.html')


@app.route('/container', methods=['POST', 'GET'])
def plz_post():
    global image
    global name
    global bashcommand
    global dockercommand
    define = request.form['text']
    arrange = define.split()
    image = arrange[0]
    name = arrange[1]
    dockercommand = list()
    if image == "apache" or image == "nginx" or image == "httpd":
        bashcommand = "docker run -d --name " + name + " -p 8080:8080 " + image
        dockercommand.append(bashcommand)
        return redirect("http://" + ip + ":5000")
    elif image == "grafana":
        bashcommand = "docker run -d -p 3000:3000 " + image
        dockercommand.append(bashcommand)
        return redirect("http://" + ip + ":5000")
    elif image == "postgresql" or image == "postgres":
        return redirect("http://" + ip + ":5000/passwordpost")
    elif image == "mysql":
        bashcommand = "docker run --name " + name + " MYSQL_ROOT_PASSWORD=" + password + " -d mysql"
        return redirect("http://" + ip + ":5000/passwordmysql2")
    else:
        return redirect("http://" + ip + ":5000/deployment2")

@app.route('/display')
def display():
    dockercommand_dis= "\n".join(dockercommand)
    return render_template('display.html', command =dockercommand_dis)

@app.route('/display', methods=['GET', 'POST'])
def display_post():
    choose = request.form['text']
    if choose == "no":
        return redirect("http://" + ip + ":5000")
    else:
        for command in dockercommand:
            deploycommand2(command)



@app.route('/passwordpost')
def password():
    return render_template('password.html')


@app.route('/passwordpost', methods=['POST', 'GET'])
def password_post():
    global bashcommand
    password = request.form['text']
    bashcommand = "docker run --name " + name + " -e POSTGRES_PASSWORD=" + password + " -d postgres"
    deploycommand()
    return redirect("http://" + ip + ":5000")


@app.route('/passwordpost2')
def password2():
    return render_template('password2.html')


@app.route('/passwordpost2', methods=['POST', 'GET'])
def password_post2():
    global bashcommand
    password = request.form['text']
    bashcommand = "docker run --name " + name + " -e POSTGRES_PASSWORD=" + password + " -d postgres"
    dockercommand.append(bashcommand)
    return redirect("http://" + ip + ":5000/objects")


@app.route('/passwordmysql2')
def passwordsql2():
    return render_template('passwordsql2.html')


@app.route('/passwordmysql2', methods=['POST', 'GET'])
def passwordsql_post2():
    global bashcommand
    password = request.form['text']
    bashcommand = "docker run --name " + name + " MYSQL_ROOT_PASSWORD=" + password + " -d mysql"
    dockercommand.append(bashcommand)
    return redirect("http://" + ip + ":5000/objects")


@app.route('/deployment2')
def deployment2():
    return render_template('deployment2.html')


@app.route('/deployment2', methods=['POST', 'GET'])
def deployment_post2():
    global bashcommand
    port = request.form['text']
    if port == "no":
        bashcommand = "docker run -d --name " + name + " " + image
        dockercommand.append(bashcommand)
        return redirect("http://" + ip + ":5000/objects")
    else:
        bashcommand = "docker run -d --name " + name + " -p " + port + "  " + image
        dockercommand.append(bashcommand)
        return redirect("http://" + ip + ":5000")










@app.route('/passwordmysql')
def passwordsql():
    return render_template('passwordsql.html')


@app.route('/passwordmysql', methods=['POST', 'GET'])
def passwordsql_post():
    global bashcommand
    password = request.form['text']
    bashcommand = "docker run --name " + name + " MYSQL_ROOT_PASSWORD=" + password + " -d mysql"
    deploycommand()
    return redirect("http://" + ip + ":5000")


@app.route('/deployment')
def deployment():
    return render_template('deployment.html')


@app.route('/deployment', methods=['POST', 'GET'])
def deployment_post():
    global bashcommand
    port = request.form['text']
    if port == "no":
        bashcommand = "docker run -d --name " + name + " " + image
        deploycommand()
        return redirect("http://" + ip + ":5000")
    else:
        bashcommand = "docker run -d --name " + name + " -p " + port + "  " + image
        deploycommand()
        return redirect("http://" + ip + ":5000")


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")


