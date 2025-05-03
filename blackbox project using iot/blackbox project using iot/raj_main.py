import io
import cv2
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from threading import Condition, Thread
from http import server
import smbus
import time
import socketserver

# MPU6050 Initialization
bus = smbus.SMBus(1)
MPU6050_ADDR = 0x68
bus.write_byte_data(MPU6050_ADDR, 0x6B, 0)  # Wake up the MPU6050
threshold_value = 250  # Adjustable threshold for position change detection

# Email Function
def send_email_alert():
    from_email = 'vangarajesh181817@gmail.com'
    to_email = 'vangarajesh184@gmail.com'
    password = 'npok iegw jztm eiyf'  # Replace with your app-specific password

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'Emergency Alert:  Accident Detected!'

    body = 'High acceleration detected. Accident may occur. https://maps.app.goo.gl/sx9jq1pQg1cD3W8o7'
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def read_mpu6050():
    accel_x = bus.read_byte_data(MPU6050_ADDR, 0x3B)
    accel_y = bus.read_byte_data(MPU6050_ADDR, 0x3D)
    accel_z = bus.read_byte_data(MPU6050_ADDR, 0x3F)
    return accel_x, accel_y, accel_z

# Camera Streaming Setup
PAGE = """\
<html>
<head>
<title>USB Camera - Surveillance Camera</title>
</head>
<body>
<center><h1>Live Monitoring - Surveillance Camera</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>
</body>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning('Removed streaming client %s: %s', self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

def capture_frame(camera, output):
    while True:
        ret, frame = camera.read()
        if not ret:
            continue
        ret, jpeg = cv2.imencode('.jpg', frame)
        if ret:
            output.write(jpeg.tobytes())

def record_video(camera, duration=60, output_file="single_record.mp4"):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 20.0
    frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    start_time = time.time()
    print(f"Recording started: {output_file}")

    try:
        while time.time() - start_time < duration:
            ret, frame = camera.read()
            if not ret:
                break
            out.write(frame)
    finally:
        print(f"Recording finished: {output_file}")
        out.release()

if __name__ == '__main__':
    output = StreamingOutput()
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Failed to open camera.")
        exit()

    # Start the streaming thread
    capture_thread = Thread(target=capture_frame, args=(camera, output))
    capture_thread.daemon = True
    capture_thread.start()

    # Start recording
    record_thread = Thread(target=record_video, args=(camera, 60, "single_record.mp4"))
    record_thread.start()

    # Start MPU6050 monitoring
    try:
        while True:
            accel_x, accel_y, accel_z = read_mpu6050()
            print(f"Acceleration: X={accel_x}, Y={accel_y}, Z={accel_z}")

            if abs(accel_x) > threshold_value or abs(accel_y) > threshold_value:
                print("Position change detected!")
                send_email_alert()
                time.sleep(1)

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Program stopped by User")
    finally:
        camera.release()

