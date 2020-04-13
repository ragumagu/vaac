import curses
import logging
import subprocess
import os
from curses import wrapper
from multiprocessing import Manager, Process
from multiprocessing.sharedctypes import Value
from ctypes import c_bool, c_wchar_p
from vaac_code.executor import Executor
from vaac_code.extractor import Extractor
from vaac_code.speech_recognizer import VaacSpeech
from vaac_code.terminal import InputHandler, WindowHandler
from vaac_code.window_manager import WindowManager

model_path = "/home/shrinidhi/project/vaac/vaac_model"

def run_pocketsphinx(inputchars,command_length,cmd_char_idx,updateBool):    
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
        command_length.value = len(inputchars)
        cmd_char_idx.value = len(inputchars)
        updateBool.value = True
        if "".join(inputchars) == "exit":
            logging.debug("run_pocketsphinx: exiting")
            break

def take_keyboard_input(stdscr, pad, inputchars,command_length,cmd_char_idx,updateBool,maxlines,screen_log):
    inputHandler = InputHandler(stdscr, pad, inputchars,command_length,cmd_char_idx,updateBool,screen_log)
    while(1):
        inputHandler.takeInput()
        inputHandler.processArgs()        
        logging.debug("take_keyboard_input:inputHandler took input.")
        updateBool.value = True
        if inputHandler.checkIfExit():
            logging.info("take_keyboard_input: exiting")
            return
        

def output(stdscr, pad, inputchars,command_length,cmd_char_idx,updateBool,maxlines,screen_log):
    inputHandler = InputHandler(stdscr, pad, inputchars,command_length,cmd_char_idx,updateBool,screen_log)
    windowHandler = WindowHandler(stdscr, pad, inputHandler, maxlines)
    windowHandler.initscreen(inputHandler)
    windowHandler.refresh()
    import time
    while(1):
        time.sleep(0.01)
        if updateBool.value:
            windowHandler.writeInput(inputHandler)
            windowHandler.updateyx(inputHandler)
            windowHandler.move_cursor(inputHandler)
            windowHandler.refresh()
            input_string= "".join(inputchars)
            logging.info("output:input_string"+input_string)
            if input_string == "exit":
                logging.info("output: exiting")
                return
            updateBool.value = False

def main(stdscr):
    logging.basicConfig(filename='term.log',filemode="w", level=logging.DEBUG)
    logger = logging.getLogger("root")
    #logger.setLevel(logging.CRITICAL)
    
    manager = Manager()
    rc = manager.list()
    inputchars = manager.list()
    command_length = manager.Value('i',0)
    cmd_char_idx = manager.Value('i',0)
    updateBool = manager.Value(c_bool,True)
    screen_log = manager.Value(c_wchar_p,"")
    logger.debug("cmd_char_idx"+str(cmd_char_idx)+" "+str(type(cmd_char_idx)))
    logger.debug("updateBool"+str(updateBool)+" "+str(type(updateBool))+str(bool(updateBool)))
    maxlines = 2000
    pad = curses.newpad(maxlines, curses.COLS)

    # Start running pocketsphinx in a process.
    pocketsphinx_proc = Process(target=run_pocketsphinx, args=(inputchars,command_length,cmd_char_idx,updateBool,))
    pocketsphinx_proc.start()

    # Start taking input from keyboard.
    keyboard_proc = Process(target=take_keyboard_input, args=(stdscr, pad, inputchars,command_length,cmd_char_idx,updateBool,maxlines,screen_log))
    keyboard_proc.start()    

    output_proc = Process(target=output, args=(stdscr, pad, inputchars,command_length,cmd_char_idx,updateBool,maxlines,screen_log))
    output_proc.start()    

    output_proc.join()
    pocketsphinx_proc.join()
    keyboard_proc.terminate()

wrapper(main)
