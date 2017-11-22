#!/usr/bin/python

'''
 Collect information regarding submitted jobs 
 This version of the PBS does not need to use
 temporary files to store job info

 Author: Andrea Borghesi
	  University of Bologna 
         andrea.borghesi3@unibo.it
 Date: 20170622
'''

from __future__ import with_statement
import sys
import os
import commands
import subprocess
import datetime
from subprocess import PIPE
import re
import pbs
import simplejson as json

'''
Testing only: 
    if the node doesn't belong the the test cluster, exit hook
'''
test_cluster_nodes = []
test_cluster_config = '/cinecalocal/sysprod/examon_pmu_pub/host_whitelist'
nodes = []
test_cluster_nodes_temp = []
try:
    with open(test_cluster_config,'r') as tcnf:
        test_cluster_nodes_temp = tcnf.read().splitlines() 
except:
    pbs.event().accept()

for n in test_cluster_nodes_temp:
    if not n.startswith('# Host') and not n.startswith('[BROKER:]') and not n == '':
        test_cluster_nodes.append(n)

templogs_dir = '/cineca/tmp/DO_NOT_DELETE-JOBS_INFO_SDHPCSY-6905/'
cores_info_table_dir = templogs_dir + 'cores_info_table'

info2mqtt_pyscript = '/galileo/home/userexternal/aborghes/' 
info2mqtt_pyscript += 'data_collection/galileo_pbs/mqtt_publisher'
info2mqtt_pyscript += '/info2mqtt_pub.py'

NCORE = 16

def convert_time(time_str):
    t = time_str.split(':')
    if len(t) < 2:
        time = 0
    # actually, I'm not sure that this is the HHMM format instead of MMSS
    elif len(t) == 2:
        if t[0] == '--' or t[1] == '--':
            time = 0
        else:
            time = 3600 * int(t[0]) + 60 * int(t[1])
    # HHMMSS format
    elif len(t) == 3:
        if t[0] == '--' or t[1] == '--' or t[2] == '--':
            time = 0
        else:
            time = 3600 * int(t[0]) + 60 * int(t[1]) + int(t[2])
    return time
    
def convert_size(value, units='b'):
    logs = {'b': 0, 'k': 10, 'm': 20, 'g': 30,
            't': 40, 'p': 50, 'e': 60, 'z': 70, 'y': 80}
    try:
        new = units[0].lower()
        if new not in logs:
            new = 'b'
        val, old = re.match('([-+]?\d+)([bkmgtpezy]?)',
                            str(value).lower()).groups()
        val = int(val)
        if val < 0:
            raise ValueError('Value may not be negative')
        if old not in logs.keys():
            old = 'b'
        factor = logs[old] - logs[new]
        val *= 2 ** factor
        slop = val - int(val)
        val = int(val)
        if slop > 0:
            val += 1
        # pbs.size() does not like units following zero
        if val <= 0:
            return '0'
        else:
            #return str(val) + new
            return str(val)
    except:
        return None

def parse_schedselect(schedselect):
    mpiprocs = -1
    Qlist = ''
    ngpus = -1
    nmics = -1
    if 'mpiprocs' in schedselect:
        mpiprocs = int(schedselect.split('mpiprocs=')[1].split(':')[0])
    if 'Qlist' in schedselect:
        Qlist = schedselect.split('Qlist=')[1].split(':')[0]
    if 'ngpus' in schedselect:
        ngpus = int(schedselect.split('ngpus=')[1].split(':')[0])
    if 'nmics' in schedselect:
        nmics = int(schedselect.split('nmics=')[1].split(':')[0])
    return mpiprocs, Qlist, ngpus, nmics

e = pbs.event()
j = e.job

if pbs.event().type == pbs.RUNJOB:
    try:

        txt = ''
        job_dict = {}

        queue=str(j.queue)
        job_id = str(j.id)
        job_name = str(j.Job_Name)
        job_owner = str(j.Job_Owner)[:-26]
        account_name = str(j.Account_Name)
        project = str(j.project)

        # job creation time, should be already in seconds
        ctime = -1
        qtime = -1
        if(j.ctime != None):
            ctime = int(j.ctime)
        # enter q time should be already in seconds
        if(j.qtime != None):
            qtime = int(j.qtime)

        # not sure qtime is always correctly specified..
        # we create a backup qtime just in case
        time_now = datetime.datetime.now()
        backup_qtime = datetime.datetime.strftime(time_now,"%Y-%m-%d %H:%M:%S")

        # requested resources
        req_cpus = int(j.Resource_List['ncpus'])

        # convert memory in megabyte
        req_mem = convert_size(str(j.Resource_List['mem']),'m')

        # covert requested wall-time in seconds
        req_time = convert_time(str(j.Resource_List['walltime']))

        mpiprocs, Qlist, ngpus, nmics = parse_schedselect(str(j.schedselect))

        # job variable list
        variable_list = j.Variable_List

        vnode_list_str = str(j.exec_vnode)
        exec_nodes = vnode_list_str.split('+')
        vnode_list = []
        for ex in exec_nodes:
            ex_info = ex.split(':')
            node = ex_info[0]
            node = node.replace('(', "")
            vnode_list.append(node)

        if str(j.exec_host) != 'None':
            execnode_list = str(j.exec_host)
        else:
            execnode_list = str(j.exec_host2)
        exec_nnodes = execnode_list.split('+')
        exec_node_list = []
        for ex in exec_nnodes:
            ex_info = ex.split(':')
            node = ex_info[0].split('.')[0]
            exec_node_list.append(node)

        job_dict['job_id'] = job_id
        job_dict['queue'] = queue
        job_dict['job_name'] = job_name
        job_dict['job_owner'] = job_owner 
        job_dict['account_name'] = account_name
        job_dict['project'] = project
        job_dict['ctime'] = ctime
        job_dict['qtime'] = qtime
        job_dict['backup_qtime'] = backup_qtime
        job_dict['req_cpus'] = req_cpus
        job_dict['req_mem'] = req_mem
        job_dict['req_time'] = req_time
        job_dict['mpiprocs'] = mpiprocs
        job_dict['Qlist'] = Qlist
        job_dict['ngpus'] = ngpus
        job_dict['nmics'] = nmics
        job_dict['variable_list '] = variable_list
        job_dict['node_list'] = exec_node_list
        job_dict['vnode_list'] = vnode_list

        # check if all execution nodes are in the whitelist
        all_nodes_whitelist = 1
        for n in vnode_list:
            if n not in test_cluster_nodes:
                all_nodes_whitelist = 0

        # if a job is a job array (i.e. job_id = 465677[].io01) discard it
        is_job_array = 0
        if '[]' in job_id:
            is_job_array = 1

        # if any exec node is not in the whitelist, do not send info
        if all_nodes_whitelist != 0 and is_job_array != 1:
            # call external python script and send info through MQTT
            subprocess.call([
                    "python", info2mqtt_pyscript, "RUNJOB", str(job_dict)])

    except:
        pass

    pbs.event().accept()

elif pbs.event().type == pbs.EXECJOB_BEGIN:
    try:

        queue=str(j.queue)
        job_id = str(j.id)
        job_name = str(j.Job_Name)
        job_owner = str(j.Job_Owner)[:-26]

        # read current time from SO (job start time)
        time_now = datetime.datetime.now()
        start_time = datetime.datetime.strftime(time_now,"%Y-%m-%d %H:%M:%S")

        vnode_list_str = str(j.exec_vnode)
        exec_nodes = vnode_list_str.split('+')
        vnode_list = []
        for ex in exec_nodes:
            ex_info = ex.split(':')
            node = ex_info[0]
            node = node.replace('(', "")
            vnode_list.append(node)

        if str(j.exec_host) != 'None':
            execnode_list = str(j.exec_host)
        else:
            execnode_list = str(j.exec_host2)
        exec_nnodes = execnode_list.split('+')
        exec_node_list = []
        for ex in exec_nnodes:
            ex_info = ex.split(':')
            node = ex_info[0].split('.')[0]
            exec_node_list.append(node)

        # the hook runs on the execution node
        hostname_str = "/etc/hostname"
        process = subprocess.Popen(
            ["cat",hostname_str], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)
        out, err = process.communicate()
        node_id = out.split('\n')[0]

        cpuset_str = "/sys/fs/cgroup/cpuset/pbspro/" + job_id + "/cpuset.cpus"
        process = subprocess.Popen(
            ["cat",cpuset_str], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)
        out, err = process.communicate()
        out_lines = out.split('\n')

        job_cores = []
        if len(out_lines) > 0:
            if out_lines[0] != '':
                core_sets = out_lines[0].split(',')
                for cs in core_sets:
                    core_range = cs.split('-')
                    if len(core_range) == 1:
                        job_cores.append(int(core_range[0]))
                    if len(core_range) == 2:
                        first_core = int(core_range[0])
                        last_core = int(core_range[1]) + 1
                        for i in range(first_core, last_core):
                            job_cores.append(i)

        job_dict = {}

        job_dict['job_id'] = job_id
        job_dict['job_name'] = job_name
        job_dict['job_owner'] = job_owner 
        job_dict['node_id'] = node_id
        job_dict['start_time'] = start_time
        job_dict['node_list'] = exec_node_list
        job_dict['vnode_list'] = vnode_list
        job_dict['job_cores'] = job_cores

        cores_info_table = cores_info_table_dir + '/' + str(
                node_id) + '_table.tmp'

        # check that core usage table for the current node_id does exist
        # if it doesn't, create  it
        if not os.path.isfile(cores_info_table):
            new_table_lines = []
            for i in range(NCORE):
                new_table_lines.append(str(i) + ';None;None;None\n')

            with open(cores_info_table, 'w') as fp:
                for line in new_table_lines:
                    fp.write(line)

        # update core usage table
        with open(cores_info_table, 'r') as fp:
            core_lines = fp.readlines() 

        for jc in job_cores:
            core_lines[jc] = str(jc) + ';' + job_id + ';' + job_owner + ';' 
            core_lines[jc] += job_name + '\n'

        with open(cores_info_table, 'w') as fp:
            for line in core_lines:
                fp.write(line)

        # check if all execution nodes are in the whitelist
        all_nodes_whitelist = 1
        for n in vnode_list:
            if n not in test_cluster_nodes:
                all_nodes_whitelist = 0

        # if a job is a job array (i.e. job_id = 465677[].io01) discard it
        is_job_array = 0
        if '[]' in job_id:
            is_job_array = 1

        # if any exec node is not in the whitelist, do not send info
        if all_nodes_whitelist != 0 and is_job_array != 1:
            # call external python script and send info through MQTT
            subprocess.call([
                    "python", info2mqtt_pyscript, 
                    "EXECJOB_BEGIN", str(job_dict)])
    except:
        pass

    pbs.event().accept()

elif pbs.event().type == pbs.EXECJOB_END:
    try:

        job_id = str(j.id)
        job_name = str(j.Job_Name)
        job_owner = str(j.Job_Owner)[:-26]

        cpupercent = int(j.resources_used['cpupercent'])
        used_mem = convert_size(str(j.resources_used['mem']),'m')
        used_vmem = convert_size(str(j.resources_used['vmem']),'m')

        # parse real wall time
        real_walltime = convert_time(str(j.resources_used['walltime']))
        cputime = convert_time(str(j.resources_used['cput']))

        # read current time from SO (job end time)
        time_now = datetime.datetime.now()
        end_time = datetime.datetime.strftime(time_now,"%Y-%m-%d %H:%M:%S")

        vnode_list_str = str(j.exec_vnode)
        exec_nodes = vnode_list_str.split('+')
        vnode_list = []
        for ex in exec_nodes:
            ex_info = ex.split(':')
            node = ex_info[0]
            node = node.replace('(', "")
            vnode_list.append(node)

        if str(j.exec_host) != 'None':
            execnode_list = str(j.exec_host)
        else:
            execnode_list = str(j.exec_host2)
        exec_nnodes = execnode_list.split('+')
        exec_node_list = []
        for ex in exec_nnodes:
            ex_info = ex.split(':')
            node = ex_info[0].split('.')[0]
            exec_node_list.append(node)

        # the hook runs on the execution node
        hostname_str = "/etc/hostname"
        process = subprocess.Popen(
            ["cat",hostname_str], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)
        out, err = process.communicate()
        node_id = out.split('\n')[0]

        job_dict = {}
       
        core_lines = []
        cores_info_table = cores_info_table_dir + '/' + str(
                node_id) + '_table.tmp'

        # check that core usage table for the current node_id does exist
        # if it doesn't, create  it
        if not os.path.isfile(cores_info_table):
            new_table_lines = []
            for i in range(NCORE):
                new_table_lines.append(str(i) + ';None;None;None\n')

            with open(cores_info_table, 'w') as fp:
                for line in new_table_lines:
                    fp.write(line)

        with open(cores_info_table, 'r') as fp:
            core_lines = fp.readlines() 
        
        # from the core table check the execution cores (we cannot look at 
        # cpuset anymore because now the job is finished)
        job_cores = []
        for cl in core_lines:
            core_info = cl.split(';')
            core = core_info[0]
            jid_info = core_info[1]
            if job_id == jid_info:
                job_cores.append(int(core))

        job_dict['job_id'] = job_id
        job_dict['job_name'] = job_name
        job_dict['job_owner'] = job_owner 
        job_dict['node_id'] = node_id
        job_dict['cpupercent'] = cpupercent
        job_dict['used_mem'] = used_mem 
        job_dict['used_vmem'] = used_vmem 
        job_dict['real_walltime'] = real_walltime
        job_dict['cputime'] = cputime 
        job_dict['end_time'] = end_time
        job_dict['node_list'] = exec_node_list
        job_dict['vnode_list'] = vnode_list
        job_dict['job_cores'] = job_cores

        # update core usage table
        for jc in job_cores:
            core_lines[jc] = str(jc) + ';None;None;None\n'

        with open(cores_info_table, 'w') as fp:
            for line in core_lines:
                fp.write(line)

        # check if all execution nodes are in the whitelist
        all_nodes_whitelist = 1
        for n in vnode_list:
            if n not in test_cluster_nodes:
                all_nodes_whitelist = 0
 
        # if a job is a job array (i.e. job_id = 465677[].io01) discard it
        is_job_array = 0
        if '[]' in job_id:
            is_job_array = 1

        # if any exec node is not in the whitelist, do not send info
        if all_nodes_whitelist != 0 and is_job_array != 1:
            # call external python script and send info through MQTT
            subprocess.call([
                    "python", info2mqtt_pyscript, 
                    "EXECJOB_END", str(job_dict)])
    except:
        pass
    pbs.event().accept()

else:
    pbs.event().accept()
