from flask import Flask, redirect, render_template, url_for, request
import pymssql
app = Flask(__name__)

# get SQL Server credentials. 
credential_file = open('credentials.txt', 'r')
server = credential_file.readline().strip()
username = credential_file.readline().strip()
password = credential_file.readline().strip()
dbname = credential_file.readline().strip()
print server, dbname

# connect to the Micosoft SQL server
conn = pymssql.connect(server, username, password, dbname)
cursor = conn.cursor(as_dict=True)
#conn.close() # maybe we should close the connection at some point

@app.route("/")
def index():
    return redirect("/login")


@app.route("/login", methods=['GET', 'POST'])
def login_user():
    if(request.method == 'POST'):
        # check db to see if it's valid
        username = request.form['username']
        password = request.form['password']
        print username, password
        # cursor.execute("EXEC AttemptLogin @username = " + username + ", @password = " + password)
        # results = cursor.fetchall()
        # print "login results:", results
        # if results == []:
        return redirect("/attendance")
    else:
        return render_template("login.html")
    


@app.route("/attendance")
def attendance_page():
    cursor.execute("EXEC GetTodaysAttendance")
    results = cursor.fetchall()
    return render_template("attendance.html", attendance=results)

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/contact")
def contact_page():
    return render_template("contact.html")

@app.route("/schedule")
def schedule_page():
    return render_template("schedule.html")

@app.route("/settings")
def settings_page():
    return render_template("settings.html")

@app.route("/upload")
def upload_page():
    if request.method == 'POST':
        upload_file = request.files['file']
        if upload_file and allowed_file(upload_file.filename):
            print "we got a file!  what type is it?", type(upload_file), "and can we open it?", open(upload_file, 'r')
            
            return "file uploaded successfully :)" # a message for the javascript callback
    else: # it is a get request, return the webpage after rendering it
        return render_template("upload.html")




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] == 'csv'

if __name__ == "__main__":
    app.debug = True # TODO: remove for production
    app.run(threaded=True)