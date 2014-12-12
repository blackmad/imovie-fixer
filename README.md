imovie-fixer
============

Script to move all external resources into an imovie project and rewrite the project file

iMovie doesn't copy in external project resources like mp3s and jpgs, making it very hard to move imovie projects between computers

run ./fix.py -i Project -o StaticFiles
from inside an iMovie rcproject to rewrite the Project to have all mp3s, movs and jpgs in StaticFiles. You can then copy this entire directory to a new computer.

From that new computer, you may need to rewrite the file again if it doesn't end up in the same directory (it seems like the project file requires absolute paths for a few things - relative paths appear to break movies)

rewriting the project file without copying 
./fix -i Project --old /Users/blackmad/Movies/iMovie Projects/Elaine.rcproject/StaticFiles -o StaticFiles
will rewrite all the paths that start with --old (untested ...)
