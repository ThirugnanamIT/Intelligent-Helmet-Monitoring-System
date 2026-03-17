import cv2
import torch
import numpy as np
# Load the model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp/weights/best.pt', force_reload=True)
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
    dd2 +=1

    # Perform object detection
    results = model(img)
    #print(results)

    try:
        # Access the detection results
        class_names = ['head', 'helmet', 'person']  # List of class names in the order corresponding to the model's output

        # Assuming results contains bounding box coordinates and class indices
        bounding_boxes = results.xyxy[0]  # Assuming the first image in results
        class_indices = bounding_boxes[:, -1].int().tolist()  # Extracting class indices
        # Mapping class indices to class names
        prediction_names = [class_names[idx] for idx in class_indices]
        # Printing prediction names
        print(prediction_names[0])

        if prediction_names[0]=="helmet":
            dd1 +=1


    except:
        pass

    if dd1 == 20:
        dd1 = 0

        cv2.waitKey(1)
        break
        cam.release()
        cv2.destroyAllWindows()

    if dd2 == 50:
        cv2.waitKey(1)
        break
        cam.release()
        cv2.destroyAllWindows()

    cv2.imshow("Output", np.squeeze(results.render()))

    # Press 'q' or 'Esc' to quit
    if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1) == 27):
        break

# Close the camera
cam.release()
cv2.destroyAllWindows()