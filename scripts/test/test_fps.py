"""test fps"""

import os
import sys
import magent

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tmp_name = 'tmp'

if len(sys.argv) < 2:
    print("usage python test_fps.py max_gpu")

if len(sys.argv) == 3:
    tmp_name += sys.argv[2]

max_gpu = eval(sys.argv[1])

number = [1000, 10000, 100000, 1000000]
gpus   = range(max_gpu+1)

ret = []

for n in number:
    row = []
    for g in gpus:
        n_step = 30000000 / n
        cmd = ("python scripts/test/test_1m.py --n_step %d --agent_number %d --num_gpu %d > /dev/shm/aha"
                "&& cat /dev/shm/aha | grep FPS > %s" % (n_step, n, g, tmp_name))
        if n < 1000000:
            cmd = 'OMP_NUM_THREADS=8  ' + cmd
        else:
            cmd = 'OMP_NUM_THREADS=16 ' + cmd
        print(cmd)
        os.system(cmd)
        with open(tmp_name) as fin:
            line = fin.readline()
            x = eval(line)[1]
        row.append(x)
        print(x)

    ret.append(row)

for row in ret:
    print(magent.round(row))
