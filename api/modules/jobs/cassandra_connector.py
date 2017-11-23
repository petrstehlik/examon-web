from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory
import logging

from muapi.configurator import Config

def connect():
    """
    Connect to a Cassandra cluster specified in config

    @return session instance
    """
    conf = Config()

    # Set logging level only to ERROR
    # When running API in debug mode, the logging info from Cassandra is too dense
    cas_logger = logging.getLogger("cassandra")
    cas_logger.setLevel(logging.ERROR)

    logger = logging.getLogger(__name__)
    logger.info("Connecting to Cassandra cluster")

    auth = PlainTextAuthProvider(
            username = conf["cassandradb"].get("user"),
            password = conf["cassandradb"].get("password"))
    cluster = Cluster(
            contact_points=([conf["cassandradb"].get("server")]),
            auth_provider = auth,
            connect_timeout = 10.0,
            control_connection_timeout = 10.0)
    session = cluster.connect(conf["cassandradb"].get("cluster"))

    logger.info("Successfully connected to Cassanda cluster")
    session.row_factory = dict_factory

    return session

def prepare_statements(session):
    """
    Prepare CQL statements for querying data
    """
    prepared = dict()

    # Select one row by job ID
    prepared["sel_by_job_id"] = session.prepare(
            "SELECT * FROM galileo_jobs_complexkey WHERE job_id = ? LIMIT 1 ALLOW FILTERING")

    #prepared["measures"] = session.prepare(
    #    """SELECT
    #        ipmi_avg_io_util,
    #        ipmi_avg_cpu_util,
    #        ipmi_avg_sys_util,
    #        ipmi_job_avg_power,
    #        job_node_avg_powerlist,
    #        job_tot_avg_power,
    #        job_tot_avg_load,
    #        job_tot_avg_temp
    #    FROM jobs_measures_aggregate
    #    WHERE job_id = ?""")

    #prepared["latest_job"] = session.prepare(
    #    """SELECT *
    #        FROM galileo_jobs_simplekey
    #        WHERE token(user_id) > token('') and start_time >= ? ALLOW FILTERING
     #   """)

    #    prepared["latest_job"] = session.prepare(
            #"SELECT * FROM galileo_jobs_complexkey WHERE start_time EQ 1400000000 ORDER BY start_time LIMIT 1")
    return prepared
