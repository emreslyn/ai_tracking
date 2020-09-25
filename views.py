from flask import Flask, render_template, request, redirect, app, flash, url_for
import os
from script import Script
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from subprocess import Popen
import psutil
from os import listdir
from os.path import isfile, join
import platform
from datetime import datetime
from systemInfo import SystemInfo

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["FILE_UPLOADS"] = "uploads"
app.config["ALLOWED_FILE_EXTENSIONS"] = ["PY"]
app.secret_key = b'_5#y2L\n\xec]/'
files = {}
checkUploads = True
servers = ["Apache","Tomcat","localhost"]
def check_file(filename):
    if not "." in filename:
        return False
    extension = filename.rsplit(".",1)[1]
    if extension.upper() in app.config["ALLOWED_FILE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/")
def main_file():
    return render_template("public/main_file.html")

@app.route("/upload-file", methods=["GET","POST"])
def upload_file():
    error = None
    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            if file.filename == "":
                print("\nNo filename\n")
                error = "You should select file."
            elif check_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["FILE_UPLOADS"], filename))
                script = Script(file.filename,"localhost","Not Invoked")
                files[filename] = script
                print("\nFile Saved.\n")
                error = "You uploaded file successfully."
            else:
                print("\nFile extension is not allowed.\n")
                error = "File extension is not allowed."
    return render_template("public/upload_file.html", error=error)

@app.route("/monitor-results")
def monitor_results():
    global checkUploads
    if checkUploads == True:
        onlyfiles = [f for f in listdir("uploads") if isfile(join("uploads", f))]
        for filename in onlyfiles:
            script = Script(filename, "localhost", "Not Invoked")
            files[filename] = script
        checkUploads = False
    return render_template("public/monitor_results.html", files = files, servers = servers)

@app.route("/run/<filename>")
def run(filename):
    file = app.config["FILE_UPLOADS"] + "//" + filename
    Popen('python ' + file)
    files[filename].condition = "Invoked"
    uname = platform.uname()
    sys_name = uname.system
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    cpu_usage = psutil.cpu_percent()
    freq = psutil.cpu_freq()
    curr_freq = freq.current
    print("Current Frequency: {} Mhz".format(freq.current))
    sysInfo = SystemInfo(sys_name,bt,cpu_usage,curr_freq)
    files[filename].sysInfo = sysInfo
    return render_template("public/monitor_results.html",files = files, servers = servers)

@app.route("/monitor/<filename>")
def monitor(filename):
    print(filename)
    return render_template("public/monitor.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)