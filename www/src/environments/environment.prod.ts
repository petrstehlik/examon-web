// The file contents for the current environment will overwrite these during build.
// The build system defaults to the dev environment which uses `environment.ts`, but if you do
// `ng build --env=prod` then `environment.prod.ts` will be used instead.
// The list of which env maps to which file can be found in `.angular-cli.json`.

export const environment = {
    production: true,
    // Default time offset for rangepicker
    timeoffset : 900000,

    // Defaults for chart configuration
    chart : {
        height : 250,           // Default height of the chart's container (px)
        labels : {
            offsetX : 10,       // X-axis offset for label position (px)
            offsetY : 20        // Y-axis offset for label position (px)
        }
    },

    // Aggregation window sizes for each MQTT publisher
    window : {
        ipmi : 20,
        pmu : 2,
        tmam : 2
    },
    active_metric : 'M4WR_MEM',
    active_metric_name : 'Level 4 Memory Write/Read Requests',
    ws : {
        //host : window.location.hostname,
        host : 'localhost',
        port : 5555
    },
    interval : 5000,    // Interval in miliseconds to resfresh data in job info,
    /**
     * Path to configuration file
     */
    configPath : 'assets/config-sample.json',
    /**
     * Used only when fetching config.json failed
     */
    apiUrl : 'api',
    config: {
        api: {
            "url" : "/api",
            "host" : null,
            "port" : null,
            "proto" : null
        },
        logo : "assets/examon_logo.png",
        name : "Examon Web",
        metrics: {
            "core_load": {
                "name": "Core's Load",
                "metric": "load_core",
                "level": "core",
                "factor": 1,
                "unit": "%",
                "range": [0, 100],
            },
            "node_load": {
                "name": "Node's Load",
                "metric": "load_node",
                "level": "node",
                "factor": 1,
                "unit": "%",
                "range": [0, 100],
            },
            "cluster_load": {
                "name": "Cluster's Load",
                "metric": "load_cluster",
                "level": "cluster",
                "factor": 1,
                "unit": "%",
                "range": [0, 100],
            },
        },
    },
};
