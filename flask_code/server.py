from flask import Flask, redirect, render_template, url_for
import pymssql
app = Flask(__name__)

# get SQL Server credentials. 
credential_file = open('credentials.txt', 'r')
server = credential_file.readline().strip()
username = credential_file.readline().strip()
password = credential_file.readline().strip()
dbname = credential_file.readline().strip()
print server, username, password, dbname

# connect to the Micosoft SQL server
conn = pymssql.connect(server, username, password, dbname)
cursor = conn.cursor(as_dict=True)
#conn.close() # maybe we should close the connection at some point

@app.route("/")
def index():
    print "get index"
    return redirect("/login")


@app.route("/login")
def login_user():
    print "get login"
    return render_template("login.html")


@app.route("/attendance")
def attendance_page():
    cursor.execute("EXEC GetTodaysAttendance")
    results = cursor.fetchall()
    return render_template("attendance.html", attendance=results)


if __name__ == "__main__":
    app.debug = True # TODO: remove for production
    app.run(threaded=True)