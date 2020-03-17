from vaac_code.buffer import extractor
e = extractor()
while True:
	s = input("> ")
	if s =="exit":
		break
	e.find_commands(s)

