import time, subprocess

time.sleep(3.03)

audio_05 = subprocess.Popen(["omxplayer", "static/sound/05_kabels_ok_loop.mp3", "-o", "local", "--loop"])
