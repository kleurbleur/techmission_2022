import subprocess

audio_01 = subprocess.run(
    ['mpg123', 'static/sound/03_pop_updated.mp3'], capture_output=True, text=True #this needs mpg123 installed
)
print("stderr:", audio_01.stderr) #stderr is part of subprocess.completedprocess and thus returns the error, in our case the message we get when done playing

if audio_01.stderr.find("finished"): #we're looking for the word finished if there's an error output
    print("done playing")
else:
    print("did not find it")