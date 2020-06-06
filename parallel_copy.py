#!/usr/bin/python
from subprocess import Popen, PIPE
from threading import Thread
try:
    import queue as Queue
except ImportError:
    import Queue

def function_rsync(source_loc,dest_loc,remote_hostname):
    while True:
        file_name = q.get()
        cmd = "rsync -aPt --ignore-existing %s:%s%s %s" % (remote_hostname, source_loc, file_name, dest_loc)
        print("Copying "+file_name+" from "+hostname+":"+source_loc+" to "+dest_loc)
        run_cmd = Popen(cmd, shell=True)
        output, err = run_cmd.communicate()
        print("Finished : "+str(output))
        q.task_done()


PARALLEL = 10
source_loc = "/nasdump/exp/"
dest_loc = "/local_acfs/imp/"
hostname = "remotehost.gsp.com"


FILE_LIST = []
fh = open('files.txt')
while True:
    line = fh.readline()
    FILE_LIST.append(line)
    if not line:
        break
fh.close()
FILE_LIST = filter(None, FILE_LIST)

q = Queue.Queue()
for i in range(PARALLEL):
    t = Thread(target=function_rsync, args=(source_loc,dest_loc,hostname))
    t.daemon = True
    t.start()


for file_name in FILE_LIST:
    file_name = file_name.strip()
    print(file_name)
    q.put(file_name)

q.join()
