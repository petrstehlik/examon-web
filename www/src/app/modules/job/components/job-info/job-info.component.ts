import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { HttpClient } from "@angular/common/http";

import { environment as env } from 'environments/environment';

import { Job } from 'app/interfaces';

import { TimeserieService } from 'app/services/timeserie.service';

@Component({
    selector: 'ex-job-info',
    templateUrl: './job-info.component.html',
    styleUrls: ['./job-info.component.scss'],
    providers : [TimeserieService]
})
export class JobInfoComponent implements OnInit, OnDestroy {

    public job: Job = new Job();
    public data: Object = {};

    private socket;
    private fetchInt;

    private default_chart_options = {
        legend : false,
        title : {
            display : true,
            text : '',
            fontSize: 16,
            fontColor : '#000'
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

    public job_classification;

    /**
     * Process job data and if event is live start websocket
     */
    @Input('job')
    set setJob(data) {
        if (data != undefined && data.loaded) {
            this.job = data;
            this.processJob();
        }
    }

    constructor(private modal: NgbModal,
                private timeserie: TimeserieService,
                private http : HttpClient) { }

    ngOnInit() {
        this.load_core_options['title']['text'] = 'Cores\' Load';
    }

    private processJob() {
        this.job['from'] = this.job['data']['start_time'];

        this.fetchClassification();

        if (this.job['data']['active']) {
            // this.startSocket();
            this.fetchInt = setInterval(() => {
                this.startFetchRaw('load_core', 'node', 'load_core', this.aggWindow());
            }, env.interval);
        }
        //this.fetchRaw('load_core', 'node', 'load_core', this.aggWindow());
    }

    private fetchClassification() {
        console.log('fetching classification');
        /*this.http.get('/classifier/' + this.job.id).subscribe(
            (res) => {
                this.job_classification = res
            });
            */
    }

    /**
     * Fetch new data for barchart with shifting 'to' date
     **/
    private startFetchRaw(dict_name,
        endpoint,
        metric: string|string[],
        aggregate: number = null)
    {
        this.job['to'] = +Date.now();
        this.timeserie.fetch(this.job, dict_name, endpoint, metric, aggregate, true)
        .subscribe(data => {
            const key = Object.keys(data['points'])[0];

            this.data['job_' + dict_name]['data'] = data['points'][key];
        });
    }

    /**
     * Fetch initial data for bar chart
     */
    private fetchRaw(dict_name,
        endpoint,
        metric: string|string[],
        aggregate: number = null)
    {
        this.data['loading_' + dict_name] = true;

        if (this.job['data']['active'])
            this.job['to'] = +Date.now();
        else
            this.job['to'] = this.job['data']['end_time'];

        this.timeserie.fetch(this.job, dict_name, endpoint, metric, aggregate, true)
        .subscribe(data => {
            const key = Object.keys(data['points'])[0];

            this.data['job_' + dict_name] = {
                data : data['points'][key],
                labels : data['labels']
            };

            this.data['loading_' + dict_name] = false;
        });
    }


    /**
     * Get an exact time duration of the job in order to aggregate to one single number
     */
    private aggWindow(): number {
        if (this.job['data']['active']) {
            return(Math.floor((+Date.now() - this.job['from']) / 1000));
        } else {
            return(Math.floor(this.job['data']['end_time'] - this.job['from']) / 1000);
        }
    }

    /**
     * Clear interval for fetching new data, unsubscribe from a room and disconnect socket
     */
    ngOnDestroy() {
        clearInterval(this.fetchInt);

        if (this.socket != undefined) {
            this.socket.emit('unsubscribe', {jobid : this.job['data']['job_id']});
            this.socket.disconnect();
        }
    }
}
