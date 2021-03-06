# python_scripts
A bunch of Python scripts I use a lot

## whenchanged
typical fs watcher, using watchdog. Whenever a file gets modified, he sees it ;)

usage: whenchanged [-h] [-t T] [--s S [S ...]] [-c C]

optional arguments:       
  * -h, --help     show this help message and exit
  * -t T           target script to execute            
  * --s S [S ...]  source files to watch
  * -c C           execute a simple shell command   

## relsize
I3-wm does not support relative size of windows. This tiny script takes a 
class name and the relative size you wish and scales it.

usage: relsize [-h] name size size

positional arguments
  * name        class name of the window 
  * size        width x height of the Window in ppt 

optional arguments:
  * -h, --help  show this help message and exit

for instance I like having qutebrowsers tabs on the right of my screen and take 10% of its width. When I open mpv to play some video I like its scratchpad to fill the browsers screen but leave my messy tabpanel visible.

![alt text](https://github.com/l-behrens/python_scripts/blob/master/img/relsize.png)

## Rofi Scripts

These scripts are mods for the Rofi Application Launcher 
https://github.com/DaveDavenport/rofi

run them:

$> rofi -show <mod_name> -modi <mod_nam>:<path_to_script>

## convert.py

This script 
* reads in an mws inventory sheet
* groups products in all permutations of specified columns

what is done:
* conversion of excel sheet to matrix
* calculation of relevant groupings

todo:
* generation of unique child products
* generation of parent product pages
* parsing to flat file format
