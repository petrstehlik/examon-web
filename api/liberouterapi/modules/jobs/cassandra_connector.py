from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory

from liberouterapi.configurator import Config

def connect():
    """
    Connect to a Cassandra cluster specified in config

    @return session instance
    """
    conf = Config()
    auth = PlainTextAuthProvider(
            username = conf["cassandradb"].get("user"),
            password = conf["cassandradb"].get("password"))
    cluster = Cluster(
            contact_points=([conf["cassandradb"].get("server")]),
            auth_provider = auth)
    print(conf["cassandradb"].get("cluster"))
    session = cluster.connect(conf["cassandradb"].get("cluster"))
    session.row_factory = dict_factory
    return session

def prepare_statements(session):
    """
    Prepare CQL statements for querying data
    """
    prepared = dict()

    # Select one row by job ID
    prepared["sel_by_job_id"] = session.prepare(
            "SELECT * FROM galileo_jobs_simplekey WHERE job_id = ? LIMIT 1")

    return prepared
