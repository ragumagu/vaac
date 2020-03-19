import subprocess

cmd = "pocketsphinx_continuous -hmm en-us -lm twocommands.lm.bin -dict twocommands.dic -inmic yes -logfn /dev/null"
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1, shell=True)
for line in p.stdout:
    line = line.decode("UTF-8")
    print(line.rstrip(),type(line))
p.stdout.close()
p.wait()
