import { Component, OnInit, Input } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

import { Job } from 'app/interfaces/job';

import { TimeserieService } from 'app/services/timeserie.service';

@Component({
    selector: 'ex-job-info',
    templateUrl: './job-info.component.html',
    styleUrls: ['./job-info.component.scss'],
    providers : [TimeserieService]
})
export class JobInfoComponent implements OnInit {

    public job : Job = new Job();
    public data : Object = {};

    private default_chart_options = {
        legend : false,
        title : {
            display : true,
            text : '',
            fontSize: 16,
            fontColor : "#000"
        },
        layout : {
            padding : {
                left : 0,
                right : 0,
                top : 0,
                bottom : 0
            }
        },
        maintainAspectRatio: false,
        responsive : true,
        scales : {
            yAxes : [{
                ticks: {
                    min : 0,
                    max : 100,
                    stepSize : 10
                },
                labelString : 'Load (%)'
            }],
            xAxes : [{
                ticks : {
                    autoSkip : false
                }
            }]
        }
    };

    public load_core_options = this.default_chart_options;

    @Input("job")
    set setJob(data) {
        if (data != undefined && data.loaded) {
            this.job = data;
            this.fetchRaw("load_core", "core", "load_core", this.aggWindow());
        }
    }

    constructor(private modal: NgbModal,
        private timeserie : TimeserieService) { }

    ngOnInit() {
        this.load_core_options['title']['text'] = 'Cores\' Load'
    }

    private fetch(dict_name,
        endpoint,
        metric : string|string[],
        aggregate : number = null)
    {
        this.data["loading_" + dict_name] = true;

        this.timeserie.fetch(this.job, dict_name, endpoint, metric, aggregate).subscribe(data => {
            this.data["job_" + dict_name] = data;
            this.data["loading_" + dict_name] = false;
        });
    }

    private fetchRaw(dict_name,
        endpoint,
        metric : string|string[],
        aggregate : number = null)
    {
        this.data["loading_" + dict_name] = true;

        this.timeserie.fetch(this.job,
            dict_name,
            endpoint,
            metric,
            aggregate,
            true)
            .subscribe(data => {
                console.log(data)
                let tmp_data = {data : [], labels : []};

                let key = Object.keys(data["points"])[0];

                tmp_data["data"] = data["points"][key];
                tmp_data["labels"] = data["labels"];

                this.data["job_" + dict_name] = tmp_data;
                this.data["loading_" + dict_name] = false;
            });
    }


    /**
     * Get an exact time duration of the job in order to aggregate to one single number
     */
    private aggWindow() : number {
        return(Math.floor(this.job["data"]["end_time"] - this.job["data"]["backup_qtime"])/1000);
    }

}
