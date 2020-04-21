# VAAC

Vaac stands for Voice Assist and Control. It is a project in progress, and aims to provide vocal access to applications.

Vaac will eventually consist of a framework to ease creation of pocketsphinx voice models for an individual speaker to do command and control, and a simple interface to use the model to perform basic tasks in other applications.

Vaac initially will support a small group of applications: Mozilla Firefox, Visual Studio Code, Gedit, Gnome-Terminal, Nautilus and will work on Ubuntu 18.04 with the Gnome3 shell.

Vaac works by matching words in the command to standard commands supported by the applications. The standard commands will be then translated into different types of keyboard events, which are then sent to the target application via Xdotool and other utilities.

# Scripts:

### Recorder:
The recorder.py program prompts a phrase from the corpus and records it into a file in the recordings folder.
If the phrase is a single word, it will be stored in `recordings/{word}/{word}_{n}.wav`. Else if the phrase is a line from the corpus, it will be stored in `recordings/{corpus_name}/{line_number}_{n}.wav` where `n` is the nth recording of the phrase.

Read the prompted phrase vocally into the microphone.

Press j/s to start recording.  
Press k/d to stop recording.  
Press l/f to store recording.  
Press ;/g to re-record without storing.  
Press e or any other key to exit.  

Verify your recordings as often as possible. Make sure they are of good quality, and that the utterances are clear and complete. Lag in microphone might cause utterances to be cut off in the middle.

If needed, use
```
	$ pactl load-module module-echo-cancel
```
to reduce noise in recordings.

If you make any mistakes when recording you can skip it using the ;/g option. However if you save it and want to redo it, simply delete the recording and run recorder again. It will automatically search for missing files and prompt the corresponding phrase.

**Note:** You can use the mic_test.sh script to check if your mic is working properly.
```
	$ ./mic_test.sh
```
 After starting the script, it will start recording for five seconds, and then play the recorded audio.

### Terminal:
The terminal.py program provides an interface to use Vaac. You can type into this terminal, or speak into it. Because of inherent inaccuracies in speech recognition, the terminal will not prompt messages for commands that do not make 'sense'. That means, if Vaac cannot understand a certain command, it will not prompt errors in the terminal. However, such errors are recorded in the logs.

The terminal accepts simple, natural language commands.

You can provide one argument to help:
```
    > help [code|firefox|gedit|nautilus|terminal]
```
to get a list of commands supported for each application.

You can use up and down to navigate through commands history, and page up and page down to scroll.
You can set maximum number of lines in the config/vaac_config file.

### Preprocessor
The preprocessor.py script checks for errors in config. This script will also copy a sorted version of config/*.csv files to data/keys.

### AnalyzeConfig
The analyzeConfig.py script runs analysis on the current config. Results will be stored in the analytics folder.
For each config/{application}.csv file,
* {application}_counts.csv will have counts of each word in the config
* {application}_partitions.csv will have partitions showing words repeated in different commands.
* {application}_sorted.csv will have commands sorted by word length, sum of word frequencies (reversed:highest first), and then by the alphabetical order of commands.
Similarly, counts_summary.csv, partitions_summary.csv, sorted_summary.csv, will have the corresponding data combining all commands from all config/{application}.csv files.

### AnalyzeCorpus
The analyzeCorpus.py script generates the analytics/corpus_counts.csv file. It will also notify of words in config not found in corpus and imbalances in word frequencies. Max and min frequencies for words in corpus can be set in config/vaac_config.

### Config
*application.csv file format*: The first half will be a command phrase, and	command phrases should consist of alphabets and spaces only. This means that commands cannot have '1','2','3', instead, they can have 'one','two','three'. The second half should be a set of keystrokes, delimited by '+'. A small set of valid keystrokes is found in config/keys.csv, where the second parts in each line are valid keystrokes. A full list can be found at https://gitlab.com/cunidev/gestures/-/wikis/xdotool-list-of-key-codes .
The first half and second half are comma separated.

## Usage:

1. Use setup.sh to setup files and folders:
	```
		$ ./setup.sh
	```

2. In the config folder, add applications for which you want support. Vaac will provide configs for some applications by default. If you want to make changes to the keyboard shortcuts, do it in the config folder.

3. Once changes are made to config folder, run preprocessor.py:
	```
		$ python3 preprocesssor.py
	```  
   If it reports any errors, correct them in the config files before proceeding further.

4. Run analyzeConfig.py to run some analysis on the current config.
	```
		$ python3 analyzeConfig.py
	```

5. Run analyseCorpus.py to run analysis on the text corpuses.
	```
		$ python3 analyzeCorpus.py
	```

6. Use recorder.py to make recordings of the corpus.
	```
		$ python3 recorder.py
	```

7. Use generate_grammar.py to generate the grammar file:
	```
		$ python3 generate_grammar.py
	```

8. Upload the grammar file to lm tool:
	http://www.speech.cs.cmu.edu/tools/lmtool-new.html

9. Download the generated .tgz file into vaac folder.
10. Use setupModel script to setup a model:
	$ ./setupModel.sh tarfile=TAR****.tgz

11. Navigate into vaac_model/etc/. Edit sphinx_train.cfg as required. 
	You might set number of senones to 2000, like
	    $CFG_N_TIED_STATES = 2000;
	instead of 200.
12. Navigate to vaac_model/. Run sphinxtrain:
	$ sphinxtrain run

8. You can now use the terminal application.
	```
		$ python terminal.py
	```

## Corpus:
There are no set rules to create a corpus. However, here are some rules of thumb:
* Use short phrases (length ~ 3)
* Phrases need not be exact commands, they can be nonsensical too.
* Try to balance the word frequencies, so that the model trains on each word equally. To help do this, you can use the analyzeCorpus.py script, which generates the corpus_counts.csv file.
* If you have to add new words, and have recorded the current corpus, create and add a new corpus file to the corpus folder. Do not edit the current corpus files, as there has to be a one to one match between the corpus files and recordings.

## Tips:
This is work in progress, so, you will need work-arounds till each problem is taken care of.
* If you have problems with focus, try restarting Gnome shell by using Alt+F2 and typing in 'r' into the prompt.
* Try having only one instance/window of every application to make sure that the commands are directed to the correct window.
