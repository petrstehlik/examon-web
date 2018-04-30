from muapi.configurator import Config

class Aggregate():
    window = None
    default_window = None

    def __init__(self, default_window):
        self.default_window = default_window
        self.window = default_window
        self.tags = None
        self.config = Config()

    def set_window(self, window):
        if window != self.default_window:
            self.window = window

    def set_group_tags(self, tags):
        self.tags = tags

    def reset(self):
        self.window = self.default_window

    def attach_agg(self, query):
        """
        Attach aggregator field to a query if not present
        """

        for item in query["metrics"]:
            if "aggregators" not in item:
                item["aggregators"] = list()

        return query

    def group_tags(self, query):
        for item in query["metrics"]:
            item["group_by"] = [
                {
                    "name": "tag",
                    "tags": self.tags
                }]
        return query

    def aggregate(self, query):
        query = self.attach_agg(query)
        query = self.group_tags(query)
        query['cache_time'] = self.config['kairosdb'].get('cache_time', 864000)

        for item in query["metrics"]:
            item["aggregators"].append({
                    "name" : "avg",
                    "align_sampling" : True,
                    "align_start_time" : True,
                    "sampling" : {
                            "value" : self.window,
                            "unit" : "seconds"
                        }
                })
        import json
        print(json.dumps(query))
        return query

    def gaps(self, query):
        query = self.attach_agg(query)
        q2 = self.group_tags(query)
        q2 = self.aggregate(q2)

        for item in q2["metrics"]:
            item["aggregators"].append({
                    "name" : "gaps",
                    #"align_sampling" : True,
                    "align_start_time" : True,
                    "sampling" : {
                        "value" : self.window,
                        "unit" : "seconds"
                    }
                })
        return q2
