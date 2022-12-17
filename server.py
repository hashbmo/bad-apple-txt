import cv2, os
from flask import Flask, send_file, request
from waitress import serve

app = Flask(__name__)

def validate_args(args, dict):
    for key in dict:
        val = args.get(key)
        if not val or not getattr(val, dict[key])():
            return False
    return True

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
    print("Creating new file")
    file = open('vid.txt','w')
    file.write(str(size)+"\n")
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
    file.close()
    cap.release()

@app.route('/txt', methods=["GET"])
def send():
    size = (48,36)
    if request.args and validate_args(request.args, {"w":"isdigit","h":"isdigit"}):
        size = abs(int(request.args['w'])),abs(int(request.args['h']))
    
    if os.path.exists('vid.txt'):
        f = open('vid.txt', 'r')
        info = f.readline(); f.close()
        if len(info) == 0 or info.lstrip().rstrip() != str(size):
            make_file()
    else: make_file()
    
    return send_file('vid.txt')
    
if __name__ == "__main__":
    print("Server online.")
    serve(app, host="0.0.0.0", port="2989")