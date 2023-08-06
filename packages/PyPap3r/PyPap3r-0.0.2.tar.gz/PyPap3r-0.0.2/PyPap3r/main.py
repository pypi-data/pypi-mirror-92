import os
import getpass


changefile = "osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file \"" + '{}' +"\"'"

changeurl = "osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file \"" + '{}' +"\"'"


def wallpaper_file(path):
	os.system(changefile.format(path))

def wallpaper_url(url):
    os.system('/usr/bin/curl -o ~/Documents/wallpaperfromwallpaperpackage.png ' + url)
    os.system('clear')
    os.system(changeurl.format('/Users/'+ getpass.getuser() +'/Documents/wallpaperfromwallpaperpackage.png'))
    os.remove('/Users/'+ getpass.getuser() +'/Documents/wallpaperfromwallpaperpackage.png')
    
#wallpaper_file('/Users/dean/Documents/wallpaperfromwallpaperpackage.png')

wallpaper_url('https://www.thebaconpug.com/css/img/background.jpg')