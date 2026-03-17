
import numpy as np

from tkinter import *
import os
from tkinter import filedialog
import cv2
import time
from matplotlib import pyplot as plt
from tkinter import messagebox
def endprogram():
	print ("\nProgram terminated!")











def testing():
    import cv2
    import torch
    import numpy as np
    # Load the model
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp10/weights/best.pt', force_reload=True)
    model.conf = 0.15
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
            bounding_boxes = results.xyxy[0]
            class_indices = bounding_boxes[:, -1].int().tolist()
            prediction_names = [class_names[idx] for idx in class_indices]
            
            # This prints exactly what the AI sees to your terminal
            print(f"AI sees: {prediction_names}") 

            # If the AI sees 'helmet' but you aren't wearing one, 
            # we trigger the email based on that detection.
            if len(prediction_names) > 0:
                dd1 += 1
                print(f"Detection confirmed! Counter: {dd1}")

        except Exception as e:
            print(f"Error in detection: {e}")

        if dd1 == 50:
            dd1 = 0
            # 1. Resize first
            img_small = cv2.resize(img, (640, 480))
            
            # 2. Save the SMALLER version (Corrected variable name here)
            cv2.imwrite("alert.jpg", img_small) 
            
            import winsound
            filename = 'alert.wav'
            winsound.PlaySound(filename, winsound.SND_FILENAME | winsound.SND_ASYNC)
            
            import threading
            threading.Thread(target=sendmail).start()

        cv2.imshow("Output", np.squeeze(results.render()))

        # Press 'q' or 'Esc' to quit
        if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1) == 27):
            break

    # Close the camera
    cam.release()
    cv2.destroyAllWindows()


def sendmail():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "thiruprasana003@gmail.com"
    toaddr = "thirugnanamrameshcs@gmail.com" 

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "HELMET ALERT"
    msg.attach(MIMEText("No helmet detected!", 'plain'))

    try:
        # Attach the photo
        with open("alert.jpg", "rb") as attachment:
            p = MIMEBase('application', 'octet-stream')
            p.set_payload(attachment.read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= alert.jpg")
            msg.attach(p)

        # Connect to Gmail (This is FREE and bypasses SendGrid)
        s = smtplib.SMTP('smtp.gmail.com', 587, timeout=30)
        s.starttls()
        s.login(fromaddr, "pezg cdqu dshg acos") 
        s.sendmail(fromaddr, toaddr, msg.as_string())
        s.quit()
        print(">>> SUCCESS: Gmail Sent! Check your inbox.")
    except Exception as e:
        print(f">>> GMAIL ERROR: {e}")

def main_account_screen():
    global main_screen
    main_screen = Tk()
    width = 600
    height = 600
    screen_width = main_screen.winfo_screenwidth()
    screen_height = main_screen.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    main_screen.geometry("%dx%d+%d+%d" % (width, height, x, y))
    main_screen.resizable(0, 0)
    # main_screen.geometry("300x250")
    main_screen.configure()
    main_screen.title(" Worker Helmet  Detection")

    Label(text="Worker Helmet  Detection", width="300", height="5", font=("Calibri", 16)).pack()

    Label(text="").pack()
    Button(text="Prediction", font=(
        'Verdana', 15), height="2", width="30", command=testing).pack(side=TOP)

    Label(text="").pack()

    main_screen.mainloop()


main_account_screen()

