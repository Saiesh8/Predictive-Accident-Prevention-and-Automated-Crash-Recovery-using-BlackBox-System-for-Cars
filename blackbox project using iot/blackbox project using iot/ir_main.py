import RPi.GPIO as GPIO
import time
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up the GPIO mode and pins
GPIO.setmode(GPIO.BCM)
IR_SENSOR_PIN = 27  # GPIO pin for IR sensor
GPIO.setup(IR_SENSOR_PIN, GPIO.IN)

# ThingSpeak settings
THINGSPEAK_API_KEY = 'XR2QGTLAQN2AUWYZ'
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

# Email settings
sender_email = "your_email@gmail.com"
receiver_email = "recipient_email@gmail.com"
email_password = "your_email_password"

# Email function
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, email_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to send data to ThingSpeak
def send_to_thingspeak(status):
    payload = {
        'api_key': THINGSPEAK_API_KEY,
        'field1': status  # Field1 is for the status of the IR sensor (1 = Object detected, 0 = No object)
    }
    try:
        response = requests.post(THINGSPEAK_URL, data=payload)
        if response.status_code == 200:
            print("Data sent to ThingSpeak successfully!")
        else:
            print(f"Failed to send data: {response.status_code}")
    except Exception as e:
        print(f"Error sending data to ThingSpeak: {e}")

# Main loop
try:
    while True:
        if GPIO.input(IR_SENSOR_PIN):
            print("No object detected!")
            send_to_thingspeak(0)  # Send '0' for no object detected
        else:
            print("Object detected!")
            send_to_thingspeak(1)  # Send '1' for object detected
            send_email("IR Sensor Alert", "An object was detected by the IR sensor!")
        
        time.sleep(1)  # Check every second

except KeyboardInterrupt:
    print("Program terminated")
    GPIO.cleanup()
