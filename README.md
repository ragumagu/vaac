# VAAC

Vaac stands for Voice Assist and Control. It is a project in progress, and aims to provide vocal access to applications.

Vaac will eventually consist of a speech recognizer module, which will convert user's vocal commands into text, a extractor module which will identify necessary entities and an exectutor module which will execute the commands.

Vaac initially will support a small group of applications: Mozilla Firefox, Visual Studio Code, Gedit, Gnome-Terminal, Nautilus and will work on Ubuntu 18.04 with the Gnome3 shell.

Vaac works by matching words in the command to standard commands supported by the applications. The standard commands will be then translated into different types of keyboard events, which are then sent to the target application via Xdotool and other utilities.

## Tips:
This is work in progress, so, you will need work-arounds till each problem is taken care of.
* If you have problems with focus, try restarting Gnome shell by using Alt+F2 and typing in 'r' into the prompt.
* Try having only one instance/window of every application to make sure that the commands are directed to the correct window.