import RPi.GPIO as GPIO
import time
import smtplib
import requests

# Setup for GPIO
MQ2_PIN = 17  # GPIO pin where the MQ2 digital output is connected
GPIO.setmode(GPIO.BCM)
GPIO.setup(MQ2_PIN, GPIO.IN)

# ThingSpeak settings
THINGSPEAK_URL = "https://api.thingspeak.com/update"
THING_API_KEY = "XR2QGTLAQN2AUWYZ"  # Replace with your ThingSpeak API key

# Email settings
SENDER_EMAIL = "your_email@example.com"  # Replace with your email
RECIPIENT_EMAIL = "recipient_email@example.com"  # Replace with recipient email
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_PASSWORD = "your_email_password"  # Replace with your email password

def send_email():
    """Send email alert when gas is detected."""
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # Create email content
        subject = "Alchohol Detected!"
        body = "Alchohol has been detected by the MQ2 sensor."
        message = f"Subject: {subject}\n\n{body}"

        # Send email
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, message)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

def upload_to_thingspeak(gas_detected):
    """Upload data to ThingSpeak."""
    payload = {
        "api_key": THING_API_KEY,
        "field2": gas_detected
    }
    try:
        response = requests.post(THINGSPEAK_URL, data=payload)
        if response.status_code == 200:
            print("Data uploaded to ThingSpeak.")
        else:
            print("Failed to upload data to ThingSpeak.")
    except Exception as e:
        print(f"Error uploading data: {e}")

def read_mq2():
    """Read the MQ2 sensor and take action if gas is detected."""
    if GPIO.input(MQ2_PIN) == GPIO.HIGH:
        print("Alchohol detected!")
        send_email()  # Send email when gas is detected
        upload_to_thingspeak(1)  # Send 1 (gas detected) to ThingSpeak
    else:
        print("No Alchohol detected.")
        upload_to_thingspeak(0)  # Send 0 (no gas) to ThingSpeak

try:
    while True:
        read_mq2()  # Check the sensor status
        time.sleep(1)  # Wait for 1 second before reading again

except KeyboardInterrupt:
    print("Program terminated")

finally:
    GPIO.cleanup()  # Clean up GPIO settings
