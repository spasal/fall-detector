import pygame
import time

pygame.mixer.init()
__s = pygame.mixer.Sound("C:\\Users\\alexs\\Google Drive\\NMCT\\A & V Productions\\Project\\fall-detector\\ignore\\resources\\alarm.wav")
__is_running = False

# Start playback
def start_alarm():
    global __is_running
    if not __is_running:
        __s.play()
        __is_running = True

# Stop playback
def stop_alarm():
    __s.stop()
    global __is_running
    __is_running = False
