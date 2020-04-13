import curses
import logging
import os
import subprocess
import time
from ctypes import c_bool, c_wchar_p
from curses import wrapper
from multiprocessing import Manager, Process
from multiprocessing.sharedctypes import Value

from vaac_code.speech_recognizer import VaacSpeech
from vaac_code.terminal import InputHandler, WindowHandler

model_path = "/home/shrinidhi/project/vaac/vaac_model"
MAXLINES = 2000


def run_pocketsphinx(inputchars, cmd_char_idx, submitBool):
    logging.debug("run_pocketsphinx(): started")
    speech = VaacSpeech(
        verbose=False,
        sampling_rate=16000,
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        hmm=os.path.join(model_path, 'vaac_model.cd_cont_2000'),
        lm=os.path.join(model_path, 'vaac_model.lm.DMP'),
        dic=os.path.join(model_path, 'vaac_model.dic'),
    )
    for phrase in speech:
        for char in str(phrase).lower().strip():
            inputchars.append(char)
        logging.debug("run_pocketsphinx(): "+"".join(inputchars))
        cmd_char_idx.value = len(inputchars)
        submitBool.value = True


def take_keyboard_input(stdscr, char, updateBool):
    logging.debug("take_keyboard_input(): started")
    while(1):
        char.value = stdscr.getch()
        logging.debug("take_keyboard_input:inputHandler took input.")
        updateBool.value = True

def output(inputchars, cmd_char_idx, submitBool,
           stdscr, char, updateBool):
    logging.debug("output(): started")
    pad = curses.newpad(MAXLINES, curses.COLS)
    inputHandler = InputHandler(
        inputchars, cmd_char_idx, char,
        updateBool, stdscr, pad
    )    
    windowHandler = WindowHandler(stdscr, pad, inputHandler, MAXLINES)    
    windowHandler.initscreen(inputHandler)    
    windowHandler.refresh()    
    while(1):        
        time.sleep(0.01)
        if "".join(inputchars) == "exit":
            logging.info("output: exiting")
            return
        if submitBool.value:
            inputHandler.takeInput(char=ord('\n'))
            logging.info("output thread: sent input key_enter")
            updateBool.value = True
        if updateBool.value:
            inputHandler.processArgs()
            windowHandler.writeInput(inputHandler)
            windowHandler.updateyx(inputHandler)
            windowHandler.move_cursor(inputHandler)
            windowHandler.refresh()
            updateBool.value = False
            submitBool.value = False


def main(stdscr):
    logging.basicConfig(filename='term.log', filemode="w", level=logging.DEBUG)
    logger = logging.getLogger("root")
    # logger.setLevel(logging.CRITICAL)

    manager = Manager()
    rc = manager.list()
    inputchars = manager.list()
    cmd_char_idx = manager.Value('i', 0)
    char = manager.Value('i', 0)
    updateBool = manager.Value(c_bool, False)
    submitBool = manager.Value(c_bool, False)

    # Process for running pocketsphinx.
    pocketsphinx_proc = Process(target=run_pocketsphinx, args=(
        inputchars, cmd_char_idx, submitBool,))

    # Process for taking input from keyboard.
    keyboard_proc = Process(target=take_keyboard_input,
                            args=(stdscr, char, updateBool))

    # Process for putting input onto the screen.
    output_proc = Process(
        target=output,
        args=(
            inputchars, cmd_char_idx, submitBool,
            stdscr, char, updateBool,
        )
    )
    
    keyboard_proc.start()    
    pocketsphinx_proc.start()
    time.sleep(0.1)
    output_proc.start()

    output_proc.join()
    keyboard_proc.terminate()
    #keyboard_proc.join()
    pocketsphinx_proc.terminate()
    #pocketsphinx_proc.join()


wrapper(main)
