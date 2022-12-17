import cv2, os
from flask import Flask, send_file
from waitress import serve

app = Flask(__name__)

def encode(arr):
    encoded = []
    cur, count = None, 0
    for x in arr:
        if cur != x:
            if cur != None: encoded.append((cur,count))
            cur, count = x, 1
        else:
            count += 1
    encoded.append((cur,count))
    return encoded

def make_file(size=(48,36)):
    file = open('vid.txt','w')
    cap = cv2.VideoCapture('badapple.mp4')
    while True:
        ret, frame = cap.read()
        if not ret: break
        img_data = cv2.resize(frame,size).tolist()
        serial = []
        for row in img_data:
            for x in row: serial.append(x[0])
        encoded = encode(serial)
        line = ""
        for x in encoded: line += f'[{str(x[0])+"."+str(x[1])}]'
        line += "_"
        file.write(line)
    cap.release()

@app.route('/txt', methods=["GET"])
def send():
    if os.path.getsize('vid.txt') == 0:
        make_file()
    return send_file('vid.txt')
    
if __name__ == "__main__":
    print("Server online.")
    serve(app, host="0.0.0.0", port="2989")