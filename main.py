import pygame
import json
import glob
from time import sleep
import os
import sys
import RPi.GPIO as GPIO

def play_music(index):
	music.stop()
	music.load("sound/"+soundtracks[index])
	music.play()
	while music.get_busy() == True:
		continue
		
print("Ciao")
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(5,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(11,GPIO.IN,pull_up_down=GPIO.PUD_UP)
mixer = pygame.mixer
mixer.init()
music = mixer.music

index_audio = 0
soundtracks = os.listdir("./sound")
print(soundtracks)
while True:
	if(GPIO.input(3) == GPIO.LOW):
		if(index_audio == len(soundtracks)-1):
			index_audio = 0
		else:
			index_audio += 1
		print("avanti: " , index_audio)
		play_music(index_audio)

	if(GPIO.input(5) == GPIO.LOW):
		if(index_audio == 0):
			index_audio = len(soundtracks)-1
		else:
			index_audio -= 1
		print("indietro: " , index_audio)
		play_music(index_audio)
		
	if(GPIO.input(11) == GPIO.LOW):
		music.stop()
		print("stop")
	

		
		
