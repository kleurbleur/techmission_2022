import subprocess

flits_4s = subprocess.Popen(["python", "/home/pi/Desktop/techmission/software/python/flits_b_groen_4s.py"], stdout=subprocess.PIPE)
stdout = int(flits_4s.communicate()[0])
print("stdout", type(stdout), stdout)
if stdout == 1: 
    print("done playing")