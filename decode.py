import cv2
import os
from pyzbar import pyzbar
import base64
import gzip
import json

def read_qr_code(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    barcodes = pyzbar.decode(gray)
    
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type
        
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "{} ({})".format(barcode_data, barcode_type)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        os.remove(image_path)
        
        return barcode_data
        
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    
def clear_folder(folder_path):
    try:
        os.mkdir(folder_path)
    except FileExistsError:
        pass

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        os.remove(file_path)

def extract_frames(video_path, output_dir):
    video = cv2.VideoCapture(video_path)
    
    clear_folder(output_dir)
    
    frame_count = 0
    last_time = None
    
    with open(os.path.join("output", input("Output file?\n")), "wb") as f:
        while video.isOpened():
            ret, frame = video.read()
            
            if not ret:
                break
            
            frame_path = os.path.join(output_dir, f"{frame_count}.png")
            cv2.imwrite(frame_path, frame)
            the = json.loads(read_qr_code(frame_path))
            
            if last_time != the["time"]:
                f.write(base64.a85decode(the["chunk"].encode("utf-8")))
            
            last_time = the["time"]
            
            frame_count += 1
    
    video.release()
    
    print(f"Finished doing shit. Saved into output folder.")
    
video_path = input("Input file?\n")
output_dir = 'framestmp'
extract_frames(video_path, output_dir)