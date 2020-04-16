import os
import subprocess

from pocketsphinx import LiveSpeech, get_model_path

from vaac_code.extractor import Extractor
from vaac_code.window_manager import WindowManager

if __name__ == "__main__":

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
    
    wm = WindowManager()	
    extractor = Extractor(wm)
    
    for phrase in speech:
        phrase = str(phrase)
        print("> ", phrase)
        if phrase != "EXIT":
            output = extractor.extract_and_run(phrase)
            if output is not None:
                print(output)
            print("Ready...")
        else:
            break
