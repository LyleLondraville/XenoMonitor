import os

for file in list(f for f in os.listdir('.') if os.path.isfile(f)):
    if '.out' in file:
        os.remove(file)
