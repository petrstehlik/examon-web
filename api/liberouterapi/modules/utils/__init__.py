import calendar, datetime, time
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

    if isinstance(obj, datetime.datetime):
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
    job = jobman.db[jobid]
    job_tmplt = copy.deepcopy(job['runjob'][0])
    job_tmplt['active'] = True
    job_tmplt['asoc_nodes'] = list()
    job_tmplt['backup_qtime'] = calendar.timegm((datetime.datetime.strptime(job_tmplt['backup_qtime'], "%Y-%m-%d %H:%M:%S")).timetuple()) * 1000

    if "exc_begin" in job:
        for item in job['exc_begin']:
            job_tmplt['asoc_nodes'].append({
                "node" : item['node_id'],
                "cores" : item['job_cores']
                })

        job_tmplt = merge_dicts(job_tmplt, job['exc_begin'][0])
        job_tmplt['start_time'] = calendar.timegm((datetime.datetime.strptime(job['exc_begin'][0]['start_time'], "%Y-%m-%d %H:%M:%S")).timetuple()) * 1000

    job_tmplt['ngpus_req'] = job_tmplt['ngpus']
    job_tmplt['ncpus_req'] = job_tmplt['req_cpus']
    job_tmplt['nmics_req'] = job_tmplt['nmics']
    job_tmplt['mem_req'] = job_tmplt['req_mem']
    job_tmplt['nnodes_req'] = len(job_tmplt['vnode_list'])
    job_tmplt['user_id'] = job_tmplt['job_owner']

    return(job_tmplt)


