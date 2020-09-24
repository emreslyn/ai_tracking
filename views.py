from flask import Flask, render_template, request, redirect, app, flash, url_for
import os
from script import Script
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from subprocess import Popen
import psutil
from os import listdir
from os.path import isfile, join

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
                #return redirect(request.url, error=error)
            elif check_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["FILE_UPLOADS"], filename))
                script = Script(file.filename,"localhost","Not Invoked")
                files[filename] = script
                print("\nFile Saved.\n")
                error = "You uploaded file successfully."
                #return redirect(url_for("public/upload_file.html", error=error))
            else:
                print("\nFile extension is not allowed.\n")
                error = "File extension is not allowed."
                #return redirect(request.url, error=error)
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
    #
    """
    print("=" * 40, "CPU Info", "=" * 40)
    # number of cores
    print("Physical cores:", psutil.cpu_count(logical=False))
    print("Total cores:", psutil.cpu_count(logical=True))
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    # CPU usage
    print("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"Core {i}: {percentage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")
    """
    return render_template("public/monitor_results.html",files = files, servers = servers)

@app.route("/monitor/<filename>")
def monitor(filename):
    print(filename)
    return render_template("public/monitor.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)