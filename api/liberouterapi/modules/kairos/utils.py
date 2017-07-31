from .error import JobsError

def check_times(args):
    """
    Check timestamps in a GET request
    """
    if "from" in args:
        # Convert to int so we can compare it
        args["from"] = int(args["from"])
    else:
        raise JobsError("Missing 'from' in GET parameters")

    if "to" not in args:
        # Generate timestamp
        args["to"] = int(time.time()) * 1000
    else:
        args["to"] = int(args["to"])

    if args["to"] < args["from"]:
        raise JobsError("'from' time cannot precede 'to' time")

def generate_base_url():
    return("{0}://{1}:{2}/api/v1".format(conn.schema, conn.server, conn.port))

def generate_health_url():
    return("{0}://{1}:{2}/api/v1/health".format(conn.schema, conn.server, conn.port))


def extract_data(raw_data, data, labels, grouper):
    for result in raw_data["queries"][0]["results"]:
        labels.append(result["group_by"][0]["group"][grouper])

        for item in result["values"]:
            round_time = int(round(item[0], 1))

            if str(round_time) not in data:
                data[str(round_time)] = [item[1]]
            else:
                data[str(round_time)].append(item[1])
