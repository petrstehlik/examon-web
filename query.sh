#curl -u petr:e55Z958! -H "Content-Type: application/json" http://130.186.13.80:8010/api/v1/version

curl -u galileo:g4l1l30975 -H "Content-Type: application/json" -X POST -d '{
  "metrics": [
    {
      "limit":100,
      "order": "asc",
      "tags": {
          "org": [
              "cineca"
          ],
          "cluster": [
            "galileo"
          ],
          "node": [
            "node061"
          ]
      },
      "name": "temp",
      "group_by": [
        {
            "name": "tag",
           "tags": [
              "node"
            ]
        }
      ]
    }
  ],
  "cache_time": 0,
  "start_absolute": 1509580800000,
  "end_absolute": 1509590800000
}' http://137.204.213.218:8083/api/v1/datapoints/query

#curl -u petr:e55Z958! http://130.186.13.80:8010/api/v1/health/status


#{'metrics': [{'aggregators': [{'align_sampling': True, 'name': 'avg', 'align_start_time': True, 'sampling': {'unit': 'seconds', 'value': 2}}], 'group_by': [{'name': 'tag', 'tags': ['node', 'core']}], 'name': u'back_end_bound', 'tags': {'node': [u'node100']}}], 'end_absolute': 1522230940000000, 'cache_time': 86400, 'start_absolute': 0}
#"start_relative": {
#    "value": "10",
#    "unit": "minutes"
#  },

#{'metrics': [{'aggregators': [{'align_sampling': True, 'name': 'avg', 'align_start_time': True, 'sampling': {'unit': 'seconds', 'value': 2}}], 'group_by': [{'name': 'tag', 'tags': ['node', 'core']}], 'name': u'back_end_bound', 'tags': {'node': [u'node100']}}], 'end_absolute': 1509590000, 'cache_time': 86400, 'start_absolute': 1509580000}


curl -u galileo:g4l1l30975 -H "Content-Type: application/json" -X POST -d '{

    "metrics":[
        {
            "aggregators":[
                {
                    "align_sampling":true,
                    "name":"avg",
                    "align_start_time":true,
                    "sampling":{
                        "unit":"seconds",
                        "value":2
                    }
                }
            ],
            "group_by":[
                {
                    "name":"tag",
                    "tags":[
                        "node",
                        "core"
                    ]
                }
            ],
            "name":"temp",
            "tags":{
                "node":[
                    "node061"
                ],
                "org":"cineca",
                "cluster":"galileo"
            }
        }
    ],
    "end_absolute":1509590800000,
    "cache_time":86400,
    "start_absolute":1509580800000

}' http://137.204.213.218:8083/api/v1/datapoints/query