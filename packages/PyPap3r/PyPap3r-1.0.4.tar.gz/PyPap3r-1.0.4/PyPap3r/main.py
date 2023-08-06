import os
import random
import getpass
import time


changefile = "osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file \"" + '{}' +"\"'"

changeurl = "osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file \"" + '{}' +"\"'"

number = random.randint(1000,9999)

def wallpaper_file(path):
	os.system(changefile.format(path))


def wallpaper_url(url):
    os.system('/usr/bin/curl -o ~/Documents/' + str(number) + '.png ' + url)
    os.system('clear')
    os.system(changeurl.format('/Users/'+ getpass.getuser() +'/Documents/' + str(number) + '.png'))
    time.sleep(5)
    os.remove('/Users/'+ getpass.getuser() +'/Documents/' + str(number) + '.png')
    


