import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smbus
import time

# Initialize the MPU6050
bus = smbus.SMBus(1)
MPU6050_ADDR = 0x68
bus.write_byte_data(MPU6050_ADDR, 0x6B, 0)  # Wake up the MPU6050

# Adjustable threshold for position change detection
threshold_value = 250  # Adjust this value as needed

# Email settings
def send_email_alert():
    from_email = 'vangarajesh181817@gmail.com'
    to_email = 'saiesh0809saiesh@gmail.com'
    password = 'npok iegw jztm eiyf'  # Update with your app-specific password

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'Emergency Alert: Chair Accident Detected!'

    body = 'High acceleration detected:9.90 m/s^2.Accident may occur.    https://maps.app.goo.gl/sx9jq1pQg1cD3W8o7'
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # For Gmail
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

try:
    while True:
        # Read acceleration data
        accel_x, accel_y, accel_z = read_mpu6050()
        print(f"Acceleration: X={accel_x}, Y={accel_y}, Z={accel_z}")

        # Check for a threshold to detect significant movement
        if abs(accel_x) > threshold_value or abs(accel_y) > threshold_value:
            print("Position change detected!")
            send_email_alert()
            time.sleep(1)  # Wait to avoid multiple emails

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program stopped by User")
