import subprocess
import time

audio_01 = subprocess.Popen(['mplayer', '-loop', '0', '/home/pi/Desktop/techmission/software/python/static/sound/03_goede_kabel_groep.mp3'])
time.sleep(3)
print("1")
time.sleep(3)
print("2")
time.sleep(3)
print("3")
time.sleep(3)
print("4")
time.sleep(3)
print("5-kill")
audio_01.terminate()
audio_01.wait()
audio_01.kill()