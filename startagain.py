import subprocess

filename = 'C:/Users/Korisnik/OneDrive/Desktop/CAT/cat_breed/app.py'
while True:
    p = subprocess.Popen('python '+filename, shell=True).wait()
    if p != 0:
        continue
    else:
        pass