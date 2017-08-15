import calendar, time
from datetime import datetime
import decimal
import copy

def split_list(values, delim = ","):
    """
    Remove all whitespaces and split by delimiter
    """
    return values.replace(" ", "").split(delim)

def merge_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z

def get_duration(start, end):
    """
    Get duration in seconds from two datetimes
    """
    return (end - start).total_seconds()

def time_serializer(obj):
    """Default JSON serializer."""
    if isinstance(obj, datetime):
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()
        millis = int(
            calendar.timegm(obj.timetuple()) * 1000 +
            obj.microsecond / 1000
        )
        return millis
    if isinstance(obj, decimal.Decimal):
        return float(obj)

    raise TypeError('Not sure how to serialize %s' % (obj,))

def asoc_node_core(cores, nodes):
    """
    Associate nodes with theirs cores

    Expected format of cores:
        `core1, core2#core1#core1`
        where each core is separated by a comma and each node's core by a hashtag

    Expected format of nodes:
        commna separated list with the number of items as in cores list for nodes
    """
    asoc_nodes = list()

    nodes_list = split_list(nodes)
    cores_list = split_list(cores, delim="#")

    if len(nodes_list) != (len(cores_list) - 1):
        # Both lists must have the same length
        raise Exception("Cores' and nodes' list lenghts doesn't match!")

    for i in range(0, len(nodes_list)):
        asoc_nodes.append({
                "node" : nodes_list[i],
                "cores" : split_list(cores_list[i])
            })

    return asoc_nodes

def transform_live_job(jobid, jobman):
    job_raw = jobman.db[jobid]

    # Get the basic info from a job
    job = copy.deepcopy(job_raw['runjob'][0])

    # Set its active status
    job['active'] = True

    job['backup_qtime'] = datetime.strptime(job['backup_qtime'], "%Y-%m-%d %H:%M:%S")

    if "exc_begin" in job:
        job['exc_begin'] = True
        job['asoc_nodes'] = list()

        for item in job_raw['exc_begin']:
            job['asoc_nodes'].append({
                "node" : item['node_id'],
                "cores" : item['job_cores']
                })

        job = merge_dicts(job, job_raw['exc_begin'][0])
        job['start_time'] = datetime.strptime(job['start_time'], "%Y-%m-%d %H:%M:%S")

    job['ngpus_req']  = job['ngpus']
    job['ncpus_req']  = job['req_cpus']
    job['nmics_req']  = job['nmics']
    job['nnodes_req'] = len(job['vnode_list'])
    job['mem_req']    = job['req_mem']
    job['user_id']    = job['job_owner']

    return(job)

