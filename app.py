from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages
from database import validate_user, add_record, update_record, search_record, get_all_records, delete_record
import hashlib

app = Flask(__name__)
app.secret_key = "39cm85yu234m98"
upload_folder = "static/images"
app.config["UPLOAD_FOLDER"] = upload_folder

@app.route("/upload", methods=['POST', 'GET'])
def upload():
    if request.method == "POST":
        try:
            file = request.files['webcam']
            idno = request.args.get("idno")
            lastname = request.args.get("lastname")
            firstname = request.args.get("firstname")
            course = request.args.get("course")
            level = request.args.get("level")
            imagename = upload_folder + "/" + idno + ".jpg"
            studentField = ['idno', 'lastname', 'firstname', 'course', 'level', 'images']
            studentData = [idno, lastname, firstname, course, level, imagename]
            file.save(imagename)
            okey = add_record('tblstudent', studentField, studentData)
            if okey:
                flash("Student added.", 'success')
                return redirect(url_for("student_list"))
            else:
                flash("Something went wrong while uploading.", 'error')
                return redirect(url_for("student_list"))
        except Exception as e:
            flash(f"Error: {str(e)}", 'error')
            return redirect(url_for("student_list"))
    

@app.route("/add_student", methods=["POST"])
def add_student():
    try:
        idno: str = request.form["idno"]
        lastname: str = request.form["lastname"]
        firstname: str = request.form["firstname"]
        course: str = request.form["course"]
        level: str = request.form["level"]
        images = upload_folder+"/"+"default"+".jpg"
        rows = database.searchrecord('tblstudent','idno',idno)
        studentField:list=['idno','lastname','firstname','course','level','images']
        studentData:list=[idno, lastname, firstname, course, level, images]
        if rows ==None:
            okey: bool = add_record('tblstudent', studentField, studentData)			
            if okey:	
                flash("New Student Added",'success')
                return redirect(url_for("student_list"))
            else:
                okey: bool = update_record('tblstudent',studentField, studentData,'idno',idno)		
                if okey==False:
                    flash("Something went wrong!, updating",'error')
                    return redirect(url_for("student_list"))
                #SUCCESS
                flash("Student Updated!",'success')
                return redirect(url_for("student_list"))
        flash("Something went wrong.",'error')
        return redirect(url_for("student_list"))
    except Exception as e:
        flash(f"Error: {str(e)}", 'error')
        return redirect(url_for("student_list"))

@app.route("/delete_student", methods=["GET"])
def delete_student(): 
    try:
        # Retrieving the ID parameter from the request
        student_id = request.args.get('id')

        # Checking if the student exists
        if not search_record('tblstudent', 'id', student_id):
            flash("Student doesn't exist!", 'error')
        else:
            # Deleting the student record
            if delete_record('tblstudent', 'id', int(student_id)):
                flash("Student deleted.", 'success')
            else:
                flash("Something went wrong while deleting!", 'error')
        
        return redirect(url_for("student_list"))
    except Exception:
        flash("Something went wrong", 'error')
        return redirect(url_for("student_list"))


@app.route("/home")
def student_list():
    if "username" in session:
        headers = ['#', 'Id No.', 'Last Name', 'First Name', 'Course', 'Level', 'Image', 'Actions']
        student_list = get_all_records('tblstudent')
        flashed_messages = get_flashed_messages()
        return render_template("home.html", title="Home", student_list=student_list, page_header=headers, flashed_messages=flashed_messages)
    else:
        return redirect(url_for("index"))

@app.route("/")
def index():
    flashed_messages = get_flashed_messages()
    return render_template("signin.html", title="Sign In", flashed_messages=flashed_messages)

@app.route("/signup")
def signup():
    return render_template("signup.html", title="Sign Up")
    
#SIGN-IN USER    
@app.route("/signin", methods=["POST"])
def signin():
    username = request.form["username"].strip()
    password = request.form["password"].strip()
    password = hashlib.md5(password.encode()).hexdigest()

    if username and password:
        if validate_user(username, password):
            session['username'] = username
            return redirect(url_for("student_list"))
        else:
            flash("Invalid username or password, please try again.", 'error')
            return redirect(url_for("index"))
    else:
        flash("Invalid username or password, please try again.", 'error')
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index", message="Your account has been signed out"))

@app.after_request
def after_request(response):
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
