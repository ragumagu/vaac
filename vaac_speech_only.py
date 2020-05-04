import configparser

from pocketsphinx import LiveSpeech

from vaac_code.extractor import Extractor

if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read('./config/vaac_config')
    hmm = config['PATHS']['hmm']
    lm = config['PATHS']['lm']
    dic = config['PATHS']['dic']

    speech = LiveSpeech(
        verbose=False,
        sampling_rate=16000,
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        hmm=hmm,
        lm=lm,
        dic=dic
    )

    extractor = Extractor()

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
