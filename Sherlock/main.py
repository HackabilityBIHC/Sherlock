import pygame
import json
import glob
from time import sleep
import time
import os
import sys
import RPi.GPIO as GPIO
from gpiozero import Button

SKIP = 5
index_audio = 0
stateMusic = False

def play_music(index):
	global stateMusic
	stateMusic = True
	music.stop()
	music.load("sound/"+soundtracks[index])
	music.play()
	
		
print("Ciao")
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(5,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(11,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(13,GPIO.OUT)
GPIO.output(13,GPIO.HIGH)

mixer = pygame.mixer
mixer.init()
music = mixer.music

soundtracks = os.listdir("./sound")
print(soundtracks)

def forwardBtn(channel):
	global index_audio
	start_time = time.time()
	longPress = False
	while GPIO.input(channel) == GPIO.LOW:
		time.sleep(.1)
		if(time.time()-start_time > 3):
			longPress = True
		
	
	if(not longPress):
		if(index_audio == len(soundtracks)-1):
			index_audio = 0
		else:
			index_audio += 1
		play_music(index_audio)

		print("Avanti: " , index_audio)
	else:
		music.set_pos(SKIP)


def backBtn(channel):
	global index_audio
	if(music.get_pos() > 3000):
		play_music(index_audio)
	else:
		if(index_audio == 0):
			index_audio = len(soundtracks)-1
		else:
			index_audio -= 1
		play_music(index_audio)
		print("Indietro: " , index_audio)
		



def pauseBtn(channel):
	global stateMusic
	if(stateMusic):
		music.pause()		
		print("Pausa")
		stateMusic = False
	else:
		music.unpause()
		print("Play")
		stateMusic = True


GPIO.add_event_detect(3, GPIO.FALLING, callback = forwardBtn, bouncetime=200)
GPIO.add_event_detect(5, GPIO.FALLING, callback = backBtn, bouncetime=200)
GPIO.add_event_detect(11, GPIO.FALLING, callback = pauseBtn, bouncetime=200)

while True:
	pass