from liberouterapi import app
from ..module import Module

from flask import Blueprint

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory
import json
import calendar, datetime

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
    raise TypeError('Not sure how to serialize %s' % (obj,))


jobs = Blueprint('jobs', __name__, url_prefix = '/jobs')

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

    def split_list(values, delim = ","):
        """
        Remove all whitespaces and split by delimiter
        """
        return values.replace(" ", "").split(delim)

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


@jobs.route('/<string:jobid>', methods=['GET'])
def jobs_hello(jobid):
    res = session.execute(prepared["sel_by_job_id"], (jobid,))
    if len(res.current_rows) == 0:
        return('', 404)


    try:
        res[0]["asoc_nodes"] = asoc_node_core(res[0]["used_cores"], res[0]["vnode_list"])
    except Exception as e:
        return(json.dumps({
                "message" : str(e),
                "error" : True
            }), 500)

    print(res[0])

    res[0]['ctime'] = calendar.timegm(res[0]['ctime'].timetuple()) * 1000
    return(json.dumps(res[0], default=default))

