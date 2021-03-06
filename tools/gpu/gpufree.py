#!/usr/bin/python2
import os, sys, subprocess
import re
import multiprocessing as mp
from collections import Counter

#GPUS = {"goneril":2, "cepheus":2, "gpuhost3": 2, "gpuhost2": 2}#, "gpuhost1": 3}
# HOSTS = ['goneril','cepheus','gpuhost3','gpuhost2','gpuhost1']
HOSTS = ['decore1',
         'decore2',
         'dvorak0',
         'dvorak1']
HOSTS +=  ['decore0'] # SOW
HOSTS_NOT_NA =   [('decore1', 0), ('decore1', 1),
                  ('decore2', 0), ('decore2', 1),
                  ('dvorak0', 0), ('dvorak0', 1),
                  ('dvorak1', 0), ('dvorak1', 1)]
HOSTS_NOT_NA += [('decore0', 0), ('decore0', 1)]
# HOSTS_NOT_NA = [('goneril',1),('cepheus',0),('cepheus',1),('gpuhost3',0),('gpuhost3',1)]

def exec_cmd(command): # return stdout, stderr output of a command
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

def get_gpuusers(hostname, gpuid):
    # out, _ = exec_cmd('ssh elbayadm@%s.ligone \'M=""; K="";for i in `nvidia-smi -q -i %d | grep "Process ID" | cut -f 2 -d ":" | tr -d "[[:blank:]]"`; do J=`ps -o user $i`; if [ ${J/USER} == "elbayadm" ]; then M="$M $(ps $i)"; fi; K="$K ${J/USER/}($i)"; done; echo $K; echo $M\''%(hostname, gpuid))
    out , _ = exec_cmd('ssh elbayadm@%s.ligone "source ~/.envrc && getgpujobs %d"' % (hostname, gpuid))
    lines = [l.strip() for l in out.split('\n')]
    # remove empty :
    lines = [l for l in lines if l]
    users = "FREE"
    jobs = []
    if lines:
        users = lines[0]
        if len(lines) > 1:
            ll = lines[1]
            starts = re.finditer('python', ll)
            ends = re.finditer('.yaml', ll)
            for s, e in zip(starts, ends):
                jobs.append(ll[s.start():e.start()])
    print " | %-8s %2d | %-70s |" % (hostname, gpuid, users)
    if jobs:
        for job in jobs:
            print " | %15s %-68s |" % ( "|>>", job)

def get_gpuinfo(hostname):
    # return product-name, fan(%), temperature (C), used-memory, total-memory, process-running?
    try:
        out, _ = exec_cmd('ssh elbayadm@%s.ligone "nvidia-smi -q"'%(hostname))
        # print('out:', out)
        igpu=0
        d = dict()
        for l in out.splitlines()[8:]+["GPU"]:
            if l.startswith("GPU"):
                running_process = "No" if "Processes" in d.keys() and d["Processes"]=="None" else ("Yes" if "Processes Process ID" in d.keys() else "N/A")
                infos = (d["Product Name"], d["Fan Speed"], d["Temperature GPU Current Temp"], d["FB Memory Usage Used"], d["FB Memory Usage Total"], running_process)
                print " | %-8s %2d | %-23s | %-4s | %5s | %5s | %5d/%5d |"%(hostname, igpu, infos[0], infos[5], infos[1], infos[2], int(infos[3][:infos[3].find(" ")]), int(infos[4][:infos[4].find(" ")]))
                d.clear()
                igpu+=1
            elif ":" in l:
                if l[4]!=" ": last=""
                d[last+l.split(":")[0].strip()] = l.split(":")[1].strip()
            else:
                last = l.split("',")[0].strip()+" "
    except Exception as e:
        print " | %-8s    | %-23s |      |       |       |             |"%(hostname,"down")



def show_gpuinfos(show_users=False):
    print "  ----------------------------------------------------------------------------"
    print " |                         %20s                      |"%(exec_cmd("date")[0].strip())
    print " |----------------------------------------------------------------------------|"
    print " | Hostname ID |         gpuname         | Run. |  Fan  | Temp. |    Memory   |"
    print " |----------------------------------------------------------------------------|"
    processes = [mp.Process(target=get_gpuinfo, args=(k,)) for k in HOSTS]
    for p in processes: p.start()
    for p in processes: p.join()
    if show_users:
        print " |----------------------------------------------------------------------------|"
        print " | Hostname ID |  users                                                       |"
        print " |--------------------------------------------------------------------------------------|"
        processes = [mp.Process(target=get_gpuusers, args=(k,i)) for k,i in HOSTS_NOT_NA]
        for p in processes: p.start()
        for p in processes: p.join()
    print " ---------------------------------------------------------------------------------------"


if __name__ == '__main__':
    if len(sys.argv)==1:
        show_gpuinfos(show_users=True)
    else:
        try:
            loop = int(sys.argv[1])
            import signal
            class AlarmException(Exception):
                pass
            def alarmHandler(signum, frame):
                raise AlarmException
            def nonBlockingRawInput(timeout=30, prompt='', no_input_message=None):
              signal.signal(signal.SIGALRM, alarmHandler)
              signal.alarm(timeout)
              try:
                text = raw_input(prompt)
                signal.alarm(0)
                return text
              except AlarmException:
                if no_input_message is not None:
                  print no_input_message
              except KeyboardInterrupt:
                signal.signal(signal.SIGALRM, signal.SIG_IGN)
                raise KeyboardInterrupt
              signal.signal(signal.SIGALRM, signal.SIG_IGN)
              return None

            a = ""
            while True:
                show_gpuinfos(show_users=True)
                a = nonBlockingRawInput(timeout=loop)
        except:
            # Slow mode:
            assert sys.argv[1] == "slow"
            HOSTS +=  ['decore1'] # SLOW
            HOSTS_NOT_NA += [('decore1', 0), ('decore1', 1)]
            show_gpuinfos(show_users=True)

