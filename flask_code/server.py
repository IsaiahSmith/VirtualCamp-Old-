from flask import Flask, redirect, render_template, url_for, request
import pymssql
import csv
import datetime;
app = Flask(__name__)

# get SQL Server credentials. 
credential_file = open('credentials.txt', 'r')
server = credential_file.readline().strip()
username = credential_file.readline().strip()
password = credential_file.readline().strip()
dbname = credential_file.readline().strip()
print "db server:", server
print "db name:", dbname

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
        query = "EXEC AttemptLogin @username='"+username+"',@password='"+password+"'"
        cursor.execute(query)
        results = cursor.fetchall()
        print "login results:", results
        if len(results) > 1:
            print "ERROR: we have two users with the same username.  this should not happen ever since username is a primary key"
            return render_template("login.html", message="internal server error")
        elif results == [] or results[0]['password'] != password:
            return render_template("login.html", message="invalid username or password")
        else:
            # TODO: set the session variable however that works.
            return redirect("/attendance")
    else:
        return render_template("login.html")
    


@app.route("/attendance", methods=['GET', 'POST'])
def attendance_page():
    if request.method == 'POST':
        camper = request.form['string']
        camperArr = camper.split(", ")
        nameArr = camperArr[0].split(" ")
        fname = nameArr[0]
        lname = nameArr[1]
        tribe = camperArr[1]
        id = camperArr[2]
        date = datetime.datetime.today();
        cursor.execute("EXEC InsertAttending @date ='"+str(date)+"', @fname ='"+fname+"', @lname ='"+lname+"', @id ='"+id+"'")
        conn.commit();
        return fname + " " +lname + ", " + tribe
    else:
        cursor.execute("EXEC GetTodaysAttendance")
        results = cursor.fetchall();
        cursor.execute("EXEC GetAllCampers");
        answer = cursor.fetchall();
        for camper in answer:
            for here in results:
                if camper["ID"] == here["ID"]:
                    answer.remove(camper);
        number = len(results);
        return render_template("attendance.html", attendance=results, notHereYet=answer, count=number)

@app.route("/setAttendance", methods=['GET', 'POST'])
def setAttendance_page():
    if request.method == 'POST':
        list = request.form['list']
        print list
    cursor.execute("EXEC GetAllCampers");
    results = cursor.fetchall();
    return render_template("setAttendance.html", list=results)

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/contact")
def contact_page():
    return render_template("contact.html")

@app.route("/setSchedule")
def setSchedule_page():
    return render_template("setSchedule.html")

@app.route("/schedule", methods=['GET', 'POST'])
def schedule_page():
    date = datetime.datetime.today();
    if(date.weekday() != 0):
        if(date.weekday() <= 4):
            date -= datetime.timedelta(days=date.weekday());
        if(date.weekday() == 5):
            date += datetime.timedelta(days=2);
        if(date.weekday() == 6):
            date += datetime.timedelta(days=1);
    print date
#     query = "EXEC GetWeeksSchedule";
#     query += "@date="+datetime.today();
#     cursor.execute(query);
#     results = cursor.fetchall();
    return render_template("schedule.html")

@app.route("/settings")
def settings_page():
    return render_template("settings.html")

@app.route("/upload", methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        upload_file = request.files.get('file', default=None)
        if upload_file and allowed_file(upload_file.filename):
            print "we got a file!", dir(upload_file)
            for row in upload_file:
                row = row.split(',')
                fname = row[0]
                lname = row[1]
                tribe = row[2]
                print fname, lname, tribe
                query = "EXEC InsertCampers @Fname='"+fname+"',@Lname='"+lname+"',@Tribe='"+tribe+"'"
                print query
                cursor.execute(query)
            print "all done, committing"
            conn.commit()
            return "File uploaded successfully!" # a message for the javascript callback
        return "Oops! Something went wrong :( Try again"
    else: # it is a get request, return the webpage after rendering it
        return render_template("upload.html")




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] == 'csv'

if __name__ == "__main__":
    app.debug = True # TODO: remove for production
    app.run(threaded=True)