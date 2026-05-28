import pygame
import threading
import os

pygame.mixer.init()

def _play_sound(file_path):
    if os.path.exists(file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    else:
        print(f"Peringatan: File audio tidak ditemukan di {file_path}!")

def play_warning():
    audio_path = os.path.join("assets", "alarm.mp3")
    
    audio_thread = threading.Thread(target=_play_sound, args=(audio_path,))
    audio_thread.start()

def stop_warning():
    pygame.mixer.music.stop()