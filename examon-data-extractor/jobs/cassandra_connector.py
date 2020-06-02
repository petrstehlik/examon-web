from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory
import logging


def connect():
    """
    Connect to a Cassandra cluster specified in config

    @return session instance
    """
    # Set logging level only to ERROR
    # When running API in debug mode, the logging info from Cassandra is too dense
    cas_logger = logging.getLogger("cassandra")
    cas_logger.setLevel(logging.ERROR)

    logger = logging.getLogger(__name__)
    logger.info("Connecting to Cassandra cluster")

    auth = PlainTextAuthProvider(
            username='petr',
            password='e55Z958!')
    cluster = Cluster(
            contact_points=['137.204.213.225'],
            port=9042,
            auth_provider=auth,
            connect_timeout=10.0,
            control_connection_timeout=10.0)
    session = cluster.connect('cineca')

    logger.info("Successfully connected to Cassandra cluster")
    session.row_factory = dict_factory

    return session
