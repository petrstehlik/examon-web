export const environment = {
    production: true,
    // Default time offset for rangepicker
    timeoffset : 1800000,

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
    active_metric : 'Ambient_Temp',
    active_metric_name : 'Ambient Temperature',
    ws : {
        host : window.location.hostname,
        port : 5555
    },
    interval : 5000,    // Interval in miliseconds to resfresh data in job info
    /**
     * Path to configuration file
     */
    configPath : 'assets/config-sample.json',
    /**
     * Used only when fetching config.json failed
     */
    apiUrl : '',

};
