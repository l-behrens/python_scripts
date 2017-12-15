# python_scripts
A bunch of Python scripts I use a lot

##whenchanged
typical fs watcher, using watchdog. Whenever a file gets modified, he sees it ;)

usage: whenchanged [-h] [-t T] [--s S [S ...]] [-c C]

optional arguments:       
  -h, --help     show this help message and exit
  -t T           target script to execute            
  --s S [S ...]  source files to watch
  -c C           execute a simple shell command   


##relsize
I3-wm does not support relative size of windows. This tiny script takes a 
class name and the relative size you wish and scales it.

usage: relsize [-h] name size size

positional arguments
  name        class name of the window 
  size        width x height of the Window in ppt 

optional arguments:
  -h, --help  show this help message and exit

for instance I like having qutebrowsers tabs on the right of my screen and take 10% of its width. When I open mpv to play some video I like its scratchpad to fill the browsers screen but leave my messy tabpanel visible.



