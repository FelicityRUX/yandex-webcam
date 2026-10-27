##############################################
#   ЭТО ДОЛЖНО БЫТЬ НА ПК (ну или где ещё)   #
##############################################

import cv2
import socket
import numpy
import signal
import sys
import subprocess
import threading

pixels = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 87, 89, 91, 103, 105, 107, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143, 145, 147, 149, 151, 153, 155, 157, 159, 161, 163, 165,167, 169, 171, 173, 175, 177, 179, 181, 183, 185, 187, 189, 191, 193, 112, 110, 81, 83]

try:
    res = subprocess.run(["ffmpeg", "--version"], capture_output=True)
except FileNotFoundError:
    print("ffmpeg не установлен. установи его пж")
    exit(228)

print("Какой IP колонки?")
IP = input("> ")

if sys.platform == "win32":
    subprocess.run("ffmpeg -list_devices true -f dshow -i dummy", stdout=sys.stdout, stderr=subprocess.STDOUT)
    micname = input('Обычно винда не видит дефолтный микро. Напиши ПОЛНОЕ имя нужного микрофона. (ffmpeg уже всё показал) (если уверен, что default сработает, пиши default)\n> ')

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

process = None
run = True

def killffmpeg():
    global process, run
    run = False

    if process:
        process.kill()

    exit(0)

signal.signal(signal.SIGINT, killffmpeg)

def webcam():
    print("Загрузка камеры...")
    vc = cv2.VideoCapture(0)
    suc = True
    while suc:
        suc, frame = vc.read()
        # Форматируем
        img = cv2.resize(frame, (15, 13), interpolation=cv2.INTER_NEAREST)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Делаем array [R,G,B,0,R,G,B,0...]
        arr = img.reshape(-1, 3)
        rgba = numpy.zeros((len(arr[pixels]), 4), dtype=numpy.uint8)
        rgba[:, :3] = arr[pixels]

        client.sendto(bytes(rgba), (IP, 8388))

def microphone():
    global process
    print("Загрузка микрофона...")

    # Какая у тебя ОС?
    if sys.platform.startswith("linux"):
        audio_input = ["-f", "alsa", "-i", "default"]
    elif sys.platform == "win32":
        audio_input = ["-f", "dshow", "-i", f"audio={micname}"]
    elif sys.platform == "darwin":
        audio_input = ["-f", "avfoundation", "-i", ":0"]
    else:
        print("Я не знаю че за ОС ты используешь")
        return


    ffmpeg_cmd = ["ffmpeg", "-re", "-rtbufsize", "100M", *audio_input, "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "1", "-f", "s16le", f"udp://{IP}:8188?pkt_size=1024"]

    try:
        process = subprocess.Popen(ffmpeg_cmd, stderr=sys.stdout)
        print("Микрофон отправляет данные")
    except Exception as e:
        print(f"чет пошло не так с микрофоном: {e}")

threading.Thread(target=webcam, daemon=True).start()
threading.Thread(target=microphone, daemon=True).start()

while run:
    pass
