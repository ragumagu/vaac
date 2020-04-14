from vaac_code.extractor import Extractor
from vaac_code.window_manager import WindowManager
wm = WindowManager()
e = Extractor(wm)
while True:
	s = input("> ")
	if s =="exit":
		break
	e.command = s
	print(e.extract())

