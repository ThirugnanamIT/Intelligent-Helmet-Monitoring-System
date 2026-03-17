### **Intelligent Helmet Monitoring System (IHMS)**

**Project Description:**

The Intelligent Helmet Monitoring System (IHMS) is a real-time AI-based safety solution designed to detect and respond to workplace safety violations. Built using the YOLOv5 deep learning architecture, the system continuously monitors live video feeds to identify workers and classify their safety status into three categories: HELMET, HEAD (violation), and PERSON. The system integrates a custom-trained model (best.pt) that has been trained on a massive dataset of 5,000+ images. Upon detecting a safety breach (a worker without a helmet), IHMS immediately triggers a multi-level response including high-frequency audio alarms and automated email notifications sent via the SendGrid API to safety supervisors.

**Features:**

* Real-time safety monitoring and object detection using YOLOv5.

* Interactive GUI dashboard with controls for Image and Live Recognition.

* Visual bounding boxes with confidence scores for all detected objects.

* Immediate audible emergency beep alerts (2500Hz) for no-helmet detection.

* Automated email alerts sent to thiruprasana003@gmail.com for remote awareness.

* High-accuracy classification of head, helmet, and person classes.

* Support for live webcam streams and local image analysis.

**Requirements:**

1. Python 3.13.7 or higher

2. Python packages:

3. torch (PyTorch)

4. pandas

5. sendgrid

6. opencv-python (cv2)

7. numpy

8. Pillow

**Installation:**

Clone or download the project repository: git clone <repo-url>

Install required dependencies: pip install -r requirements.txt

Ensure the custom trained model file best.pt is present in the yolov5/runs/train/exp/weights/ directory.

Set up your SendGrid API key in App.py.

Run the main application: python Main.py

**Usage Guide:**

Launch the system using Main.py to open the control dashboard.

Click Live Recognition to activate the webcam and start real-time safety tracking.

The system will automatically label every person and helmet it sees.

If a worker appears without a helmet (labeled as 'head'), the system will beep and send an email alert.

Use the Image Detection button to analyze static photos of your work site.

Click Exit to safely close the monitoring modules.

**How It Works:**

The YOLOv5 model processes every video frame, looking for visual features that match 'head' or 'helmet'.

The detection engine filters results based on a confidence threshold (e.g., 0.7) to ensure accuracy.

If a 'head' detection is confirmed, the script triggers the winsound module for local alerts.

Simultaneously, the send\_mail function uses the SendGrid SMTP service to push a notification to the supervisor's inbox.

The system is optimized for CPU performance on high-end laptops like the Acer Predator.

**Future Enhancements:**

Integration of SMS alerts using the SMS gateway API already defined in the code.

Multi-camera support for large-scale construction site monitoring.

Integration of a MySQL database to log the time, date, and image of every safety violation.

Development of a mobile app for supervisors to receive push notifications.
