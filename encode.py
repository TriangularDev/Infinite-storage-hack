import os
import cv2
import base64
import gzip
import qrcode
import configparser
import threading
import time
import math
import json

def create_video_from_images(image_folder, video_name):
    images = sorted([img for img in os.listdir(image_folder) if img.endswith(".png")], key=lambda x: int(x.split(".")[0]))
    print(images)

    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, _ = frame.shape

    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*"mp4v"), math.ceil((len(images) / 1e6) / 2) * 2, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

def clear_folder(folder_path):
    try:
        os.mkdir(folder_path)
    except FileExistsError:
        pass

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        os.remove(file_path)

def process_data_chunk(chunksize, idx, f):
    global maxallowedthreads
    global shidandfard
    global turn
    
    while turn != idx or len(shidandfard) >= maxallowedthreads:
        time.sleep(0.025)
        
    print(f"Reading chunk #{idx}.")
    f.seek(chunksize * idx)
    data_raw = f.read(chunksize)
    print(f"Read {len(data_raw)} bytes.")
    fard = time.time()
    turn += 1
    
    shidandfard[idx] = "Doing shit."
    data = base64.urlsafe_b64encode(gzip.compress(data_raw))

    print(f"Processing node #{idx}.")
        
    qr = qrcode.QRCode(version=40, box_size=10, border=5)

    qr.add_data(json.dumps({"chunk": data.decode("ascii"), "time": fard}))

    qr.make(fit=True)
            
    img = qr.make_image(fill="black", back_color="white")
            
    img.save(f"framestmp/{idx}.png")

    print(f"Saved QRCode #{idx}.")
    shidandfard[idx] = "Done"

def main():
    global maxallowedthreads
    global shidandfard
    global turn
    
    turn = 0
    
    shidandfard = {}
    clear_folder("framestmp")

    config = configparser.ConfigParser()
    config.read('config.ini')

    pixels = []
    end = False
    
    maxallowedthreads = 500
    chunksize = int(2150)
    
    f = open(input("Input file?\n"), "rb")

    f.seek(0, os.SEEK_END)
    size = f.tell()
    f.seek(0)
    position = -1
    futures = []
    for idx in range(0, math.ceil(size / 2150) + 1):
            
        print(idx)
        threading.Thread(target=process_data_chunk, args=(chunksize, idx, f)).start()
        
        if end:
            break
            
    pixel = []
    pixels = []
    mmm = -1
    for _ in range(0, idx):
        asdf = None
        
        while not asdf:
            try:
                mmm = list(shidandfard.keys())[0]
                if shidandfard[mmm] == "Done":
                    asdf = shidandfard.pop(mmm)
            except:
                time.sleep(1)

    f.close()

    video_name = "output.mp4"

    try:
        os.mkdir("output")
    except FileExistsError:
        pass

    create_video_from_images("framestmp", os.path.join("output", video_name))

    print("Output saved to output folder.")

    clear_folder("framestmp")

if __name__ == "__main__":
    main()
