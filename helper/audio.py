import pygame
import time

pygame.mixer.init()
__s = pygame.mixer.Sound("C:\\Users\\alexs\\Google Drive\\NMCT\\A & V Productions\\Project\\fall-detector\\ignore\\resources\\alarm.wav")

# Start playback
def start_alarm():
    __s.play()

# Stop playback
def stop_alarm():
    __s.stop()
