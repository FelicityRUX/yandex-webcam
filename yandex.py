##################################
#   ЭТО ДОЛЖНО БЫТЬ НА КОЛОНКЕ   #
##################################

import socket
import subprocess
import threading

def draw(arr):
    with open("/dev/fb0", "wb", buffering=0) as fb:
        fb.write(bytes(arr))

try:
    subprocess.run(["nc", "-h"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except FileNotFoundError:
    print("У тебя нету netcat! Надо его установить (yse install netcat).")
    exit(228)


def webcam():
    webcam_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    webcam_socket.bind(('0.0.0.0', 8388))
    print("порт 8388 (камера) готов")
    while True:
        data, client_address = webcam_socket.recvfrom(1024)
        draw(data)

def microphone():
    subprocess.Popen("nc -u -l -p 8188 | aplay -t raw -f S16_LE -r 44100 -c 1 --buffer-time=200000", shell=True)
    print("порт 8188 (микрофон) готов")

threading.Thread(target=webcam, daemon=True).start()
threading.Thread(target=microphone,  daemon=True).start()

threading.Event().wait()
