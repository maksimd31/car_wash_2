import subprocess

subprocess.run(['pip', 'install -r', 'requirements.txt'], shell=True)
print('Вы установили все зависимости из файла requirements.txt')