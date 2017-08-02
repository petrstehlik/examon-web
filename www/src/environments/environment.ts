// The file contents for the current environment will overwrite these during build.
// The build system defaults to the dev environment which uses `environment.ts`, but if you do
// `ng build --env=prod` then `environment.prod.ts` will be used instead.
// The list of which env maps to which file can be found in `.angular-cli.json`.

export const environment = {
    production: false,
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
    window : {
        ipmi : 20,
        pmu : 2,
        tmam : 2
    }
}
