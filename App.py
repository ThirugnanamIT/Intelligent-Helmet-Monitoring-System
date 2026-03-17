from flask import Flask, render_template, flash, request, session
from flask import render_template, redirect, url_for, request
# from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
# from werkzeug.utils import secure_filename

import mysql.connector

import sys, fsdk, math, ctypes, time

app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/WorkerLogin")
def WorkerLogin():
    return render_template('WorkerLogin.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3workerdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/Report")
def Report():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3workerdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM atenttb")
    data = cur.fetchall()
    return render_template('Report.html', data=data)


@app.route("/ORemove")
def ORemove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3workerdb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from ownertb where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('Owner  info Remove Successfully!')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3workerdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb  ")
    data = cur.fetchall()
    return render_template('OwnerInfo.html', data=data)


@app.route("/NewWorker")
def NewWorker():
    import LiveRecognition as liv

    # del sys.modules["LiveRecognition"]
    return render_template('NewWorker.html')


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3workerdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb")
            data = cur.fetchall()
            return render_template('AdminHome.html', data=data)

        else:
            flash("UserName Or Password Incorrect!")
            return render_template('AdminHome.html')


@app.route("/newwork", methods=['GET', 'POST'])
def newwork():
    if request.method == 'POST':
        dname = request.form['name']

        UMobile = request.form['Mobile']
        UEmail = request.form['Email']
        Address = request.form['Address']
        Aadharno = request.form['Aadharno']
        uname = request.form['uname']
        password = request.form['password']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3workerdb')
        cursor = conn.cursor()
        cursor.execute(
            "insert into regtb values('','" + dname + "','" + UMobile + "','" + UEmail + "','" + Address + "','" + Aadharno + "','" +
            uname + "','" + password + "')")
        conn.commit()
        conn.close()

        flash("New User Info Saved!")
        return render_template("NewWorker.html")


@app.route("/WorkerInfo")
def WorkerInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3workerdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb")
    data = cur.fetchall()
    return render_template('WorkerInfo.html', data=data)


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3workerdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where UserName='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('WorkerLogin.html')

        else:
            session['mob'] = data[2]
            session['email'] = data[3]

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3workerdb')
            cursor = conn.cursor()
            cursor.execute("truncate table temptb")
            conn.commit()
            conn.close()
            import LiveRecognition1 as liv
            liv.att()
            del sys.modules["LiveRecognition1"]
            return driver()


def driver():
    uname = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3workerdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * from temptb where username='" + uname + "' ")
    data = cursor.fetchone()
    if data is None:
        flash('Face  is wrong')
        return render_template('WorkerLogin.html')


    else:
        import datetime
        date = datetime.datetime.now().strftime('%d-%b-%Y')

        import cv2
        import torch
        import numpy as np
        # Load the model
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp/weights/best.pt',
                               force_reload=True)
        model.conf = 0.7
        # Set webcam input
        cam = cv2.VideoCapture(0)
        dd1 = 0
        dd2 = 0
        dd3 = 0
        dd4 = 0
        while True:
            # Read frames
            ret, img = cam.read()
            dd2 += 1

            # Perform object detection
            results = model(img)
            # print(results)

            try:
                # Access the detection results
                class_names = ['head', 'helmet',
                               'person']  # List of class names in the order corresponding to the model's output

                # Assuming results contains bounding box coordinates and class indices
                bounding_boxes = results.xyxy[0]  # Assuming the first image in results
                class_indices = bounding_boxes[:, -1].int().tolist()  # Extracting class indices
                # Mapping class indices to class names
                prediction_names = [class_names[idx] for idx in class_indices]
                # Printing prediction names
                print(prediction_names[0])

                if prediction_names[0] == "helmet":
                    dd1 += 1
                    dd3 = 1




            except:
                pass

            if dd1 == 20:
                session['hel'] = 'Yes'

                cv2.waitKey(1)

                conn = mysql.connector.connect(user='root', password='', host='localhost', database='3workerdb')
                cursor = conn.cursor()
                cursor.execute(
                    "insert into atenttb values('','" + uname + "','" + date + "','Yes')")
                conn.commit()
                conn.close()

                conn = mysql.connector.connect(user='root', password='', host='localhost', database='3workerdb')
                cur = conn.cursor()
                cur.execute("SELECT * FROM atenttb where WorkerName='" + uname + "'")
                data = cur.fetchall()
                cam.release()
                cv2.destroyAllWindows()

                return render_template('WorkerHome.html', data=data)


            if dd2 == 50:
                session['hel'] = 'No'

                cv2.waitKey(1)

                conn = mysql.connector.connect(user='root', password='', host='localhost', database='3workerdb')
                cursor = conn.cursor()
                cursor.execute(
                    "insert into atenttb values('','" + uname + "','" + date + "','No')")
                conn.commit()
                conn.close()

                conn = mysql.connector.connect(user='root', password='', host='localhost', database='3workerdb')
                cur = conn.cursor()
                cur.execute("SELECT * FROM atenttb where WorkerName='" + uname + "'")
                data = cur.fetchall()
                cam.release()
                cv2.destroyAllWindows()
                import winsound

                filename = 'alert.wav'
                winsound.PlaySound(filename, winsound.SND_FILENAME)

                sendmail("thiruprasanaoo3@gmail.com","WorkerName " +  uname  +" Helmet Status: No")



                return render_template('WorkerHome.html', data=data)

            cv2.imshow("Output", np.squeeze(results.render()))

            # Press 'q' or 'Esc' to quit
            if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1) == 27):
                break

        # Close the camera
        cam.release()
        cv2.destroyAllWindows()


def sendmsg(targetno, message):
    import requests
    requests.post(
        "http://smsserver9.creativepoint.in/api.php?username=fantasy&password=596692&to=" + targetno + "&from=FSSMSS&message=Dear user  your msg is " + message + " Sent By FSMSG FSSMSS&PEID=1501563800000030506&templateid=1507162882948811640")

def sendmail(Mailid,message):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "projectmailm@gmail.com"
    toaddr = "thirugnanamrameshcs@gmail.com"

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = message

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "gzft jyol lctm titz")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
