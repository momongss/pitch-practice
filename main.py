import wave
import pyaudio
from pynput.keyboard import Key, Listener

import threading

stream_map = {}
key_lock = {}

frame_cache = {}

chunk = 1024 * 10

def play(key):
    if key not in key_lock or key_lock[key]:
        return

    key_lock[key] = True
    index, streams = stream_map[key]
    stream_map[key][0] += 1
    if stream_map[key][0] >= len(streams):
        stream_map[key][0] = 0

    for data in frame_cache[key]:
        streams[index].write(data)

def on_press(key_obj):
    try:
        key = key_obj.char.upper()
        t = threading.Thread(target=play, args=key)
        t.start()
    except:
        pass

def on_release(key_obj):
    if key_obj == Key.esc:
        return False

    try:
        key = key_obj.char.upper()
        if key in key_lock:
            key_lock[key] = False
    except:
        pass

def init():
    key_list = ['0', '2', '3', '5', '6', '7', '9', 'E', 'I', 'O', 'P', 'Q', 'R', 'T', 'U', 'W', 'Y']
    STREAM_BUFFER_SIZE = 10

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

        key_lock[key] = False

    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

    print("전처리 완료")


if __name__ == '__main__':
    init()
