import configparser
import curses
import logging
import os
import subprocess
import time
from ctypes import c_bool, c_wchar_p
from curses import wrapper
from multiprocessing import Manager, Process
from multiprocessing.sharedctypes import Value

from pocketsphinx import LiveSpeech

from vaac_code.terminal import InputHandler, WindowHandler


def run_pocketsphinx(inputchars, cmd_char_idx, submitBool,hmm,lm,dic):    
    speech = LiveSpeech(
        verbose=True,
        logfn='logs/pocketsphinx_log',
        sampling_rate=16000,
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        hmm=hmm,
        lm=lm,
        dic=dic,
    )
    for phrase in speech:
        for char in str(phrase).lower().strip():
            inputchars.append(char)
        cmd_char_idx.value = len(inputchars)
        submitBool.value = True


def take_keyboard_input(stdscr, char, updateBool):
    while(1):
        char.value = stdscr.getch()
        updateBool.value = True


def output(inputchars, cmd_char_idx, submitBool,
           stdscr, char, updateBool, logger,maxlines):
    pad = curses.newpad(maxlines, curses.COLS)
    inputHandler = InputHandler(
        inputchars, cmd_char_idx, char,
        stdscr, pad,maxlines
    )
    windowHandler = WindowHandler(stdscr, pad, inputHandler, maxlines)
    stdscr.refresh()
    while(1):
        time.sleep(0.01)
        if inputHandler.checkIfExit():
            logger.info("Exiting...")
            return
        if submitBool.value:
            inputHandler.takeInput(char=ord('\n'))
            updateBool.value = True
        if updateBool.value:
            inputHandler.processArgs()
            windowHandler.writeInput(inputHandler)
            windowHandler.updateyx(inputHandler)
            windowHandler.move_cursor()
            windowHandler.refresh()
            updateBool.value = False
            submitBool.value = False


def main(stdscr):
    logging.basicConfig(
        format='%(asctime)s:%(levelname)s:%(module)s:%(funcName)s:%(message)s', filename='logs/vaac_terminal.log',
        filemode="a",
        level=logging.DEBUG
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    config = configparser.ConfigParser()
    config.read('./config/vaac_config')
    hmm = config['PATHS']['hmm']
    lm = config['PATHS']['lm']
    dic = config['PATHS']['dic']
    maxlines = config.getint('VAAC_TERMINAL','maxlines')    

    manager = Manager()
    inputchars = manager.list()
    cmd_char_idx = manager.Value('i', 0)
    char = manager.Value('i', 0)
    updateBool = manager.Value(c_bool, True)

    # The following variable submitBool is necessary, because voice inputs can 
    # be triggered only by using inputHandler.takeInput(char=ord('\n')) which
    # is not the same as inputchars.append('\n'). This is done in output().
    submitBool = manager.Value(c_bool, False)

    # Process for running pocketsphinx.
    pocketsphinx_proc = Process(target=run_pocketsphinx, args=(
        inputchars, cmd_char_idx, submitBool,hmm,lm,dic))

    # Process for taking input from keyboard.
    keyboard_proc = Process(target=take_keyboard_input,
                            args=(stdscr, char, updateBool))

    # Process for putting input onto the screen.
    output_proc = Process(
        target=output,
        args=(
            inputchars, cmd_char_idx, submitBool,
            stdscr, char, updateBool, logger, maxlines
        )
    )

    keyboard_proc.start()
    pocketsphinx_proc.start()
    output_proc.start()

    output_proc.join()
    keyboard_proc.terminate()
    pocketsphinx_proc.terminate()


wrapper(main)
