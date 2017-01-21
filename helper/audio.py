import pygame
import time
import sys, os

pathname = os.path.dirname(sys.argv[0])
full_path = os.path.abspath(pathname)
resource_file = os.path.join(full_path, "ignore", "resources", "alarm.wav")

pygame.mixer.init()
__s = pygame.mixer.Sound(resource_file)

# Start playback
def start_alarm():
    __s.play()

# Stop playback
def stop_alarm():
    __s.stop()
