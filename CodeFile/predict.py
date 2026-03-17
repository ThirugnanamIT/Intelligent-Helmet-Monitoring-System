import cv2
import torch
import numpy as np
# Load the model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp/weights/best.pt', force_reload=True)

# --- ADD THESE LINES TO IMPROVE ACCURACY ---
model.conf = 0.25  # Lower this to 0.20 if it misses helmets, raise to 0.40 if it gives false alarms
model.iou = 0.45   # Helps with overlapping boxes (NMS threshold)
model.classes = None # Ensure it checks all trained classes (head, helmet, person)
# -------------------------------------------

# Set webcam input
cam = cv2.VideoCapture(0)

while True:
    # Read frames
    ret, img = cam.read()

    # Perform object detection
    results = model(img)

    # Display predictions
    #results.show()
    cv2.imshow("Output", np.squeeze(results.render()))

    # Press 'q' or 'Esc' to quit
    if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1) == 27):
        break

# Close the camera
cam.release()
cv2.destroyAllWindows()
