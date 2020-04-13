import os
import subprocess

from pocketsphinx import LiveSpeech, get_model_path

from vaac_code.extractor import Extractor
from vaac_code.window_manager import WindowManager

if __name__ == "__main__":
	cmd = "xdotool getwindowfocus getwindowname"
	vaac_window_title = subprocess.getoutput(cmd)
	wm = WindowManager(vaac_window_title)
	wm.resize_all()
	extractor = Extractor(wm)
	model_path = "vaac_model"

	speech = LiveSpeech(
		verbose=False,
		sampling_rate=16000,
		buffer_size=2048,
		no_search=False,
		full_utt=False,
		hmm=os.path.join(model_path, 'vaac_model.cd_cont_2000'),
		lm=os.path.join(model_path, 'vaac_model.lm.DMP'),
		dic=os.path.join(model_path, 'vaac_model.dic')
	)

	for phrase in speech:
		phrase = str(phrase)	
		print("> ",phrase)
		if phrase != "EXIT":
			extractor.extract_and_run(phrase)
			print("Ready...")
		else:
			break
