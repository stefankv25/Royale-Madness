from machine import Pin, PWM
import neopixel
from utime import sleep
import time

pin = Pin(10, Pin.OUT)
np = neopixel.NeoPixel(pin, 33)
takki1 = Pin(14, Pin.IN, Pin.PULL_UP)
takki2 = Pin(3, Pin.IN, Pin.PULL_UP)
buzzer = PWM(Pin(12))

brightness = 200
group1_left = 9
group2_left = 9
group3_left = 15

tones = {
    "B0":31,"C1":33,"CS1":35,"D1":37,"DS1":39,"E1":41,"F1":44,"FS1":46,
    "G1":49,"GS1":52,"A1":55,"AS1":58,"B1":62,"C2":65,"CS2":69,"D2":73,
    "DS2":78,"E2":82,"F2":87,"FS2":93,"G2":98,"GS2":104,"A2":110,"AS2":117,
    "B2":123,"C3":131,"CS3":139,"D3":147,"DS3":156,"E3":165,"F3":175,"FS3":185,
    "G3":196,"GS3":208,"A3":220,"AS3":233,"B3":247,"C4":262,"CS4":277,"D4":294,
    "DS4":311,"E4":330,"F4":349,"FS4":370,"G4":392,"GS4":415,"A4":440,"AS4":466,
    "B4":494,"C5":523,"CS5":554,"D5":587,"DS5":622,"E5":659,"F5":698,"FS5":740,
    "G5":784,"GS5":831,"A5":880,"AS5":932,"B5":988,"C6":1047,"CS6":1109,"D6":1175,
    "DS6":1245,"E6":1319,"F6":1397,"FS6":1480,"G6":1568,"GS6":1661,"A6":1760,
    "AS6":1865,"B6":1976,"C7":2093,"CS7":2217,"D7":2349,"DS7":2489,"E7":2637,
    "F7":2794,"FS7":2960,"G7":3136,"GS7":3322,"A7":3520,"AS7":3729,"B7":3951,
    "C8":4186,"CS8":4435,"D8":4699,"DS8":4978
}

intro_song = ["C5","E5","G5","C6",0,"C6","B5","A5","G5",0,"E5","G5","A5","C6","E6",0,"G6",0,"G6",0]
lose_song = ["C5",0,"B4",0,"AS4",0,"A4",0,"GS4",0,"G4",0,"FS4",0,0,"C3",0,0]
destruction_song = ["G5","G5",0,"DS5",0,"C5","G4",0,"DS4","D4","CS4",0,"CS4","D4",0,"DS4",0,"C4",0,"C4","C4",0,0,"B3"]

def playtone(freq):
    buzzer.duty_u16(1000)
    buzzer.freq(freq)

def playsong(song, note_delay=0.15):
    for note in song:
        if note == 0:
            buzzer.duty_u16(0)
        else:
            playtone(tones[note])
        sleep(note_delay)
    buzzer.duty_u16(0)

def get_color(total):
    ratio = total / 33
    if ratio > 0.66:
        return [0, brightness, 0]
    elif ratio > 0.33:
        t = (ratio - 0.33) / 0.33
        return [int(brightness * (1 - t)), brightness, 0]
    else:
        t = ratio / 0.33
        return [brightness, int(brightness * t), 0]

def update_leds():
    total = group1_left + group2_left + group3_left
    color = get_color(total)
    for i in range(9):
        np[i] = color if i < group1_left else [0, 0, 0]
    for i in range(9):
        np[9 + i] = color if i < group2_left else [0, 0, 0]
    for i in range(15):
        np[18 + i] = color if i < group3_left else [0, 0, 0]
    np.write()

def lose_animation():
    playsong(lose_song, note_delay=0.18)
    for _ in range(3):
        for i in range(33):
            np[i] = [brightness, 0, 0]
        np.write()
        time.sleep_ms(400)
        for i in range(33):
            np[i] = [0, 0, 0]
        np.write()
        time.sleep_ms(400)

update_leds()
playsong(intro_song, note_delay=0.12)

last_press1 = False
last_press2 = False

while True:
    pressed1 = not takki1.value()
    pressed2 = not takki2.value()
    phase3_unlocked = (group1_left == 0 and group2_left == 0)

    if pressed1 and not last_press1:
        if group1_left > 0:
            group1_left -= 1
            update_leds()
            time.sleep_ms(50)
            if group1_left == 0:
                playsong(destruction_song, note_delay=0.10)
        elif phase3_unlocked and group3_left > 0:
            group3_left -= 1
            update_leds()
            time.sleep_ms(50)
            if group3_left == 0:
                lose_animation()

    if pressed2 and not last_press2:
        if group2_left > 0:
            group2_left -= 1
            update_leds()
            time.sleep_ms(50)
            if group2_left == 0:
                playsong(destruction_song, note_delay=0.10)
        elif phase3_unlocked and group3_left > 0:
            group3_left -= 1
            update_leds()
            time.sleep_ms(50)
            if group3_left == 0:
                lose_animation()

    last_press1 = pressed1
    last_press2 = pressed2
    time.sleep_ms(20)