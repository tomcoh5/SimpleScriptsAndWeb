
from flask import Flask, url_for, render_template, request, redirect, session, request
from flask_sqlalchemy import SQLAlchemy
import subprocess
import urllib.request
dockercommand = list() 
ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

def deploycommand2(command):
    global bashcommand
    global process
    try:
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        return process
    except:
        return "Error"



def deploycommand():
    global bashcommand
    global process
    try:
        process = subprocess.Popen(bashcommand.split(), stdout=subprocess.PIPE)
        return "deployed.. "
    except:
        return "Error cant deploy"



class User(db.Model):
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/', methods=['GET', 'POST'])
def home():
    """ Session control"""
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        if request.method == 'POST':
            global username
            username = getname(request.form['username'])
            return render_template('my-form.html', data=getfollowedby(username), user = username)
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global name
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        try:
            data = User.query.filter_by(username=name, password=passw).first()
            if data is not None:
                session['logged_in'] = True
                return render_template('my-form.html')
            else:
                return render_template('errorlogin.html')
        except:
            return render_template('errorlogin.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    global username
    global password
    """Register Form"""
    if request.method == 'POST':
        new_user = User(
            username=request.form['username'],
            password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')
    return render_template('register.html')


@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))

@app.route('/options')
def options():
    return render_template('my-form.html') 
@app.route('/multi')
def multi():
    return render_template('multi.html')


@app.route('/multi', methods=['POST', 'GET'])
def multi_post():
    global network
    global bashcommand
    network = request.form['text']
    bashcommand = "docker network create  " + network
    process = subprocess.Popen(bashcommand.split(), stdout=subprocess.PIPE)
    return redirect("http://" + ip + ":5000/objects")


@app.route('/objects')
def objects():
    return render_template('objects.html')



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
            dockercommand.append(bashcommand)
            return redirect("http://" + ip + ":5000/objects")
        elif image == "grafana":
            bashcommand = "docker run -d -p 3000:3000 grafana/grafana"
            dockercommand.append(bashcommand)
            return redirect("http://" + ip + ":5000/objects")
        elif image == "postgresql" or image == "postgres":
            return redirect("http://" + ip + ":5000/passwordpost2")
        elif image == "mysql":
            return redirect("http://" + ip + ":5000/passwordmysql2")
        else:
            return redirect("http://" + ip + ":5000/deployment2")



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
        deploycommand()
        return redirect("http://" + ip + ":5000")
    elif image == "grafana":
        bashcommand = "docker run -d -p 3000:3000 " + image
        deploycommand()
        return redirect("http://" + ip + ":5000")
    elif image == "postgresql" or image == "postgres":
        return redirect("http://" + ip + ":5000/passwordpost")
    elif image == "mysql":
        return redirect("http://" + ip + ":5000/passwordmysql")
    else:
        return redirect("http://" + ip + ":5000/deployment")

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
def password5():
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
    bashcommand = "docker run --name " + name + " -e MYSQL_ROOT_PASSWORD=" + password + " -d mysql"
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
    bashcommand = "docker run --name " + name + " -e MYSQL_ROOT_PASSWORD=" + password + " -d mysql"
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


if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0')
    
