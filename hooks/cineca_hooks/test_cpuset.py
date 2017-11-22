from __future__ import with_statement
import sys
import os
import commands
import subprocess
import datetime
from subprocess import PIPE

job_id = "62.node522"
cpuset_str = "/sys/fs/cgroup/cpuset/pbspro/" + job_id + "/cpuset.cpus"

process = subprocess.Popen(
    ["cat",cpuset_str], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)
out, err = process.communicate()
out_lines = out.split('\n')

print out_lines

job_cores = []
if len(out_lines) > 0:
    core_sets = out_lines[0].split(',')
    for cs in core_sets:
        core_range = cs.split('-')
        if len(core_range) == 1:
            job_cores.append(int(core_range[0]))
        if len(core_range) == 2:
            first_core = int(core_range[0])
            last_core = int(core_range[1])
            for i in range(first_core, last_core):
                job_cores.append(i)

print  job_cores


