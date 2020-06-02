"""
Extract Job Data tables from Cassandra cluster
"""

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory, SimpleStatement
from datetime import datetime, timedelta
import json
import calendar
import time
import decimal


def time_serializer(obj):
    """Default JSON serializer."""
    if isinstance(obj, datetime):
        millis = 0
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()

        millis = int(calendar.timegm(obj.timetuple()) * 1000 + obj.microsecond / 1000)

        if obj.utcoffset() is None:
            millis -= (0 * 1000)
        return millis
    if isinstance(obj, decimal.Decimal):
        return float(obj)


# Set up authorization provider
auth = PlainTextAuthProvider(
        username = "petr",
        password = "e55Z958!")

# Set up cluster
cluster = Cluster(
            contact_points=["137.204.213.225"],
            auth_provider=auth,
            connect_timeout=30.0,
            control_connection_timeout=10.0
        )

# Initialize session
session = cluster.connect("cineca")

# Set row factory for our session
session.row_factory = dict_factory

if __name__ == "__main__":
    """
    Query for jobs in last 3 weeks and dump to json only the ones which occupy the whole node and
    took 10 to 60 minutes. This ensures there will be enough data and not too much data at once.

    Notes:
    to export all data from DB: COPY galileo_jobs_complexkey FROM 'export.csv';
    This dumps everything to the same host as the cqlsh was run
    """

    # Run it
    #q = "SELECT * from galileo_jobs_complexkey where user_id = 'pstehlik' and start_time < {} ALLOW FILTERING;".format(int(time.time()) * 1000 - 1000*60*60*24*14)
    #q = "SELECT * from galileo_jobs_complexkey where start_time > {} ALLOW FILTERING".format(int(time.time()) * 1000 - 1000*60*60*24*21)
    q = SimpleStatement("""SELECT *
            FROM galileo_jobs_complexkey
            WHERE start_time >= 1509580800000 AND start_time <= 1511184044000
            ALLOW FILTERING""", fetch_size=10000)

    print("Query: {}".format(q))

    duration = None
    records = list()


    print('Got the data, now prepping.')

    for row in session.execute(q):
        duration = int(timedelta.total_seconds(row["end_time"] - row["backup_qtime"]))

        record = {
                "cpus": [item.split(",") for item in row["used_cores"].replace(" ", "").split("#")[:-1]],
                "cpus_req": row["ncpus_req"],
                "nodes": row["vnode_list"].replace(" ", "").split(","),
                "nodes_req": row["nnodes_req"],
                "from": int(calendar.timegm(row["backup_qtime"].timetuple())),
                "to": int(calendar.timegm(row["end_time"].timetuple())),
                "job_id": row["job_id"]
            }
        records.append(record)

        if len(records) % 100 == 0:
            print('Prepared records: {}'.format(len(records)))

    print("Total # of jobs: %s" % len(records))

    with open("target_jobs_{}.json".format(int(time.time())), "w+") as f:
        json.dump(records, f)
