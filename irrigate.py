import RPi.GPIO as GPIO
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from time import sleep
from datetime import datetime
from picamera import PiCamera

def take_picture():
    now = datetime.now()
    pic_name = now.strftime("%m_%d_%Y_%H_%M_%S.jpg")
    print(pic_name)
    camera = PiCamera()
    camera.rotation = 180

    camera.start_preview()
    sleep(5)
    camera.capture(pic_name)
    camera.stop_preview()
    print("took a picture!")


def send_email(pic_name):
    port = 465
    email = "pumptydumpty2000@gmail.com"
    password = "irrigate2020"
    message = MIMEMultipart("alternative")

    context = ssl.create_default_context()

    message["Subject"] = "Garden has been watered"
    message["From"] = email
    message["To"] = email

    with open(pic_name, "rb") as f:
        mime = MIMEBase("image", "jpg", filename=pic_name)
        mime.add_header("Content-Disposition", "attachment", filename=pic_name)
        mime.add_header("X-Attachment-Id", "0")
        mime.add_header("Content-ID", "<0>")
        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        message.attach(mime)

    # create the image tag in html
    html = """\
      <html>
       <body>
         <h1>Garden Automation Update:</h1>
         <p>Your garden has been watered by Pumpty Dumpty 2000!</p>
       </body>
      </html>
    """

    body = MIMEText(html, "html")
    message.attach(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email, password)
        server.sendmail(email, email, message.as_string())

    print("sending email...")

def main():
    # cleanup the GPIO
    GPIO.cleanup()

    # pin number
    gpio_out = 7

    # set up the board and pin
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(gpio_out, GPIO.OUT)

    # initialize the pin value
    GPIO.output(gpio_out, GPIO.LOW)

    # toggle the pin value every 10 seconds
    while True:
        sleep(10)
        print("switching output value on! woohoo!!!")
        GPIO.output(gpio_out, GPIO.HIGH)
        sleep(10)
        print("switching output value off!")
        GPIO.output(gpio_out, GPIO.LOW)

        # take picture and get the file name
        pic_name=take_picture()

	# call send email function
        send_email(pic_name)

if __name__ == "__main__":
	main()

