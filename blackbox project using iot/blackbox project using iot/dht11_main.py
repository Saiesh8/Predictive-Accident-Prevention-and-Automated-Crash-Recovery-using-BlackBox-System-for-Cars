import Adafruit_DHT
import time
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ThingSpeak Configuration
THINGSPEAK_WRITE_API_KEY = "XR2QGTLAQN2AUWYZ"  # Replace with your ThingSpeak Write API Key
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# Email Configuration
SENDER_EMAIL = "your_email@gmail.com"  # Replace with your email address
RECEIVER_EMAIL = "receiver_email@gmail.com"  # Replace with receiver's email address
EMAIL_PASSWORD = "your_email_password"  # Replace with your email password

# DHT11 Sensor Configuration
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # GPIO pin connected to the DHT11 sensor

# Temperature threshold (e.g., 30°C) for sending email alert
TEMP_THRESHOLD = 27.0

def send_email_alert(subject, body):
    """Send an email alert"""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Start TLS encryption
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)  # Login to the email account
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())  # Send email
        server.quit()
        print("Email alert sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_to_thingspeak(temperature, humidity):
    """Send the temperature and humidity data to ThingSpeak"""
    payload = {
        'api_key': THINGSPEAK_WRITE_API_KEY,
        'field3': temperature,
        'field4': humidity
    }

    try:
        response = requests.post(THINGSPEAK_URL, data=payload)
        if response.status_code == 200:
            print("Data sent to ThingSpeak successfully!")
        else:
            print("Failed to send data to ThingSpeak.")
    except Exception as e:
        print(f"Error sending data to ThingSpeak: {e}")

def read_dht11():
    """Read data from the DHT11 sensor"""
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    
    if humidity is not None and temperature is not None:
        print(f"Temperature: {temperature:.1f}°C  Humidity: {humidity:.1f}%")
        
        # Send data to ThingSpeak
        send_to_thingspeak(temperature, humidity)
        
        # Check if temperature exceeds the threshold and send email alert
        if temperature > TEMP_THRESHOLD:
            subject = "High Temperature Alert!"
            body = f"Warning! The temperature has exceeded {TEMP_THRESHOLD}°C. Current temperature: {temperature}°C."
            send_email_alert(subject, body)
    else:
        print("Failed to retrieve data from DHT11 sensor")

if __name__ == '__main__':
    while True:
        read_dht11()  # Read sensor data
        time.sleep(20)  # Wait for 20 seconds before reading again

