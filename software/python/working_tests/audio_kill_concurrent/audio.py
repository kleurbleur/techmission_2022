import subprocess
import time

audio_01 = subprocess.Popen(['mpg123', 'static/sound/03_pop_updated.mp3'])
time.sleep(1)
print("1")
time.sleep(1)
print("2")
time.sleep(1)
print("3")
time.sleep(1)
print("4")
time.sleep(1)
print("5-kill")
audio_01.kill()