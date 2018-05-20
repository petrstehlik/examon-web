import calendar
from datetime import datetime
import decimal
import json

from cassandra_connector import connect


def time_serializer(obj):
    """Default JSON serializer."""
    if isinstance(obj, datetime):
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()

        millis = int(calendar.timegm(obj.timetuple()) * 1000 + obj.microsecond / 1000)

        return millis
    if isinstance(obj, decimal.Decimal):
        return float(obj)

    raise TypeError('Not sure how to serialize %s' % (obj,))

def save():
    session = connect()

    st = """
            SELECT job_id, start_time, end_time
            FROM galileo_jobs_complexkey
            WHERE start_time >= 1509580800000 AND start_time <= 1511184044000
            ALLOW FILTERING
    """

    res = session.execute(st)
    jobs = []

    print(res.current_rows)

    for item in res:
        # print(item['job_id'], item['start_time'], item['end_time'])
        jobs.append({
            'id': item['job_id'],
            'start': item['start_time'],
            'end': item['end_time']
        })

    with open('out.json', 'w') as o:
        json.dump(jobs, o, default=time_serializer)


def load():
    jobs = None
    with open('out.json', 'r') as o:
        jobs = json.load(o)

    print(len(jobs))

if __name__ == '__main__':
    load()
