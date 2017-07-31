import json

class Aggregate():
    window = None
    default_window = None

    def __init__(self, default_window):
        self.default_window = default_window
        self.window = default_window

    def set_window(self, window):
        if window != self.default_window:
            self.window = window

    def set_tags(self, tags):
        self.tags = tags

    def reset():
        self.window = self.default_window

    def group_tags(self, query):
        query["metrics"][0]["group_by"] = [
            {
                "name": "tag",
                "tags": self.tags
            }]
        return query

    def aggregate(self, query):
        q2 = self.group_tags(query)
        q2["metrics"][0]["aggregators"] = [
                {
                    "name" : "avg",
                    "align_sampling" : True,
                    "align_start_time" : True,
                    "sampling" : {
                            "value" : self.window,
                            "unit" : "seconds"
                        }
                }]

        return q2
