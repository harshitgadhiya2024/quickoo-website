from operations.mongo_operation import mongoOperation
from operations.common_operations import commonOperation
from utils.constant import constant_dict
import os, json
from flask import (Flask, render_template, request, session, send_file, flash, redirect)
from flask_cors import CORS
from datetime import datetime, date
# from operations.mail_sending import emailOperation
# from utils.html_format import htmlOperation
import uuid

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = constant_dict.get("secreat_key")
UPLOAD_FOLDER = 'static/uploads/'

client = mongoOperation().mongo_connect(get_mongourl=constant_dict.get("mongo_url"))

@app.route("/", methods=["GET", "POST"])
def home():
    try:
        return render_template("index.html")

    except Exception as e:
        response_data = commonOperation().get_error_msg("Please try again..")
        print(f"{datetime.utcnow()}: Error in register user data route: {str(e)}")
        return response_data
    
@app.route("/about", methods=["GET", "POST"])
def about():
    try:
        return render_template("about.html")

    except Exception as e:
        response_data = commonOperation().get_error_msg("Please try again..")
        print(f"{datetime.utcnow()}: Error in register user data route: {str(e)}")
        return response_data
    
@app.route("/contact", methods=["GET", "POST"])
def contact():
    try:
        if request.method=="POST":
            name = request.form.get("name")
            email = request.form.get("email")
            phone = request.form.get("phone")
            subject = request.form.get("subject")
            message = request.form.get("message")
            mongoOperation().insert_data_from_coll(client, "quickoo", "contact_us", {"name": name, "email": email, "phone": phone, 
                                                                                     "subject": subject, "message": message, "inserted_on": datetime.utcnow()})
            flash("Our administrative contact will you soon!")
            return redirect("/contact")
        else:
            return render_template("contact.html")

    except Exception as e:
        response_data = commonOperation().get_error_msg("Please try again..")
        print(f"{datetime.utcnow()}: Error in register user data route: {str(e)}")
        return response_data
    
@app.route("/newletters", methods=["GET", "POST"])
def newletters():
    try:
        email = request.form.get("email")
        mongoOperation().insert_data_from_coll(client, "quickoo", "newsletters", {"email": email})
        flash("Newsletter submit successfully...")
        return redirect("/")
    
    except Exception as e:
        response_data = commonOperation().get_error_msg("Please try again..")
        print(f"{datetime.utcnow()}: Error in register user data route: {str(e)}")
        return response_data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7070, debug=True)
