from liberouterapi import app
from ..module import Module

from flask import Blueprint

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory
import json
import calendar, datetime, time
import decimal

from cassandra_connector import connect, prepare_statements

session = connect()
prepared = prepare_statements(session)

def default(obj):
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


jobs = Blueprint('jobs', __name__, url_prefix = '/jobs')

def split_list(values, delim = ","):
    """
    Remove all whitespaces and split by delimiter
    """
    return values.replace(" ", "").split(delim)

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

def merge_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z


@jobs.route('/<string:jobid>', methods=['GET'])
def jobs_hello(jobid):
    info = session.execute(prepared["sel_by_job_id"], (jobid,))
    if len(info.current_rows) == 0:
        return('', 404)

    try:
        info[0]["asoc_nodes"] = asoc_node_core(info[0]["used_cores"], info[0]["vnode_list"])
        info[0]["vars"] = split_list(info[0]["var_list"])
    except Exception as e:
        return(json.dumps({
                "message" : str(e),
                "error" : True
            }), 500)

    measures = session.execute(prepared["measures"], (jobid,))

    if len(measures.current_rows) > 0:
        result = merge_dicts(info[0], measures[0])
    else:
        result = info[0]

    result['ctime'] = calendar.timegm(result['ctime'].timetuple()) * 1000
    return(json.dumps(result, default=default))

@jobs.route('/latest')
def jobs_latest():
    """
        Fetch all jobs that finished in last 15 minutes,
        sort them by start_time and return the last one.
    """
    tstamp = (int(time.time()) - 86400) * 1000
    qres = session.execute("SELECT * FROM galileo_jobs_complexkey \
            WHERE token(user_id) > token('') and start_time >= " \
            + str(tstamp) + " ALLOW FILTERING")

    results = []
    for item in qres:
        results.append(item)

    ordered = sorted(results, key = lambda k : k['end_time'])
    for item in ordered:
        print(item["job_id"], item["end_time"])
    return(json.dumps(ordered[-1], default=default))
