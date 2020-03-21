# VAAC

Vaac stands for Voice Assist and Control. It is a project in progress, and aims to provide vocal access to applications.

Vaac will eventually consist of a speech recognizer module, which will convert user's vocal commands into text, a extractor module which will identify necessary entities and an exectutor module which will execute the commands.

Vaac initially will support a small group of applications: Mozilla Firefox, Visual Studio Code, Gedit, Gnome-Terminal, Nautilus and will work on Ubuntu 18.04 with the Gnome3 shell.

Vaac works by matching words in the command to standard commands supported by the applications. The standard commands will be then translated into different types of keyboard events, which are then sent to the target application via Xdotool and other utilities.

## Training:
Put the en-us acoustic model into the current directory before running these scripts.

1. Use setup.sh:
	$ ./setup.sh [model_dir_name]
	to setup a model directory with necessary files and folders. A sample model_dir_name would be foo_model.

2. Make a corpus file and name it model_name_corpus. Upload to lm tool (http://www.speech.cs.cmu.edu/tools/lmtool-new.html) and download the result tarball into this folder.
	Use the following script to extract tarball:
		$ ./extract.sh tarball_name model_name
	Do not give any "./" or "/" in the model_name parameter.
	Also, store the corpus file in the model_dir for later use.

3. Use recorder.py to make recordings:
	$ python recorder.py [-h] [--count COUNT] --corpus CORPUS --modeldir MODELDIR
	--corpus CORPUS      Takes path to corpus file.
  	--modeldir MODELDIR  Takes path to model directory.

4. Use trainer.sh to train the model:
	$ ./trainer.sh model_name
	
5. Use pocketsphinx_run_model.sh to run the model:
	$ ./pocketsphinx_run_model.sh model_name
	

## Tips:
This is work in progress, so, you will need work-arounds till each problem is taken care of.
* If you have problems with focus, try restarting Gnome shell by using Alt+F2 and typing in 'r' into the prompt.
* Try having only one instance/window of every application to make sure that the commands are directed to the correct window.
