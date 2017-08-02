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
    }
}
