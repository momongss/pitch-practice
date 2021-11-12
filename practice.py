import wave
import pyaudio
from pynput.keyboard import Listener

import threading
import random
from time import sleep

stream_map = {}
frame_cache = {}

chunk = 1024 * 10

pressed_key = [""]

def play(key):
    index, streams = stream_map[key]
    stream_map[key][0] += 1
    if stream_map[key][0] >= len(streams):
        stream_map[key][0] = 0

    for data in frame_cache[key]:
        streams[index].write(data)

def on_press(key_obj):
    key = key_obj.char.upper()
    try:
        pressed_key[0] = key.upper()
    except:
        print("올바르지 않은 키 입니다.")

def on_release(key_obj):
    pass

def init():
    key_list = ['Q', '2', 'W', '3', 'E', 'R', '5', 'T']
    # key_list = ['6', 'Y', '7', 'U', 'I', '9', 'O', '0', 'P']
    # key_list = ['Q', '2', 'W', '3', 'E', 'R', '5', 'T', '6', 'Y', '7', 'U', 'I', '9', 'O', '0', 'P']
    STREAM_BUFFER_SIZE = 10

    GAME_STEP = 10

    print("절대음감 훈련 게임")
    print("===============")
    print()

    for key in key_list:
        f = wave.open(f"./node/{key}.wav", 'rb')
        p = pyaudio.PyAudio()
        streams = [
            p.open(
                format=p.get_format_from_width(f.getsampwidth()),
                channels=f.getnchannels(),
                rate=f.getframerate(),
                output=True) for _ in range(STREAM_BUFFER_SIZE)
        ]

        stream_map[key] = [0, streams]
        frame_cache[key] = []

        data = f.readframes(chunk)
        frame_cache[key].append(data)
        while data:
            data = f.readframes(chunk)
            frame_cache[key].append(data)

    listener = Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()

    win = 0
    lose = 0

    for i in range(GAME_STEP):
        sleep(1)
        print("")
        print(f"====== 준비 STEP ({i+1}) =======")
        sleep(2)
        print("재생!! 건반을 맞추세요")
        key = random.choice(key_list)

        t = threading.Thread(target=play, args=key)
        t.start()

        count_down(3)
        print(f"{'''정답!!''' if pressed_key[0] == key else '''오답...'''} ")
        print(f"누른 건반 : {pressed_key[0]}")
        print(f"답 : {key} ")

        if pressed_key[0] == key:
            win += 1
        else:
            lose += 1

    print()
    print("====== 게임 결과 ======")
    print(f"정답 : {win} 오답 : {lose}")
    print(f"정답률 : {win / GAME_STEP * 100}%")

def count_down(sec):
    for i in range(sec):
        sleep(1)
        print(sec - i)
    sleep(1)

if __name__ == '__main__':
    init()
