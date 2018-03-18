import { Component, OnInit, Input, SimpleChanges } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { TimeserieService } from 'app/services/timeserie.service';
import { environment as env } from "environments/environment";

interface Total {
    jobs: number;
    to: number;
    from: number;
    duration: number;
    gpus: number;
    nodes: number;
    mics: number;
    cpus: number;
}

@Component({
    selector: 'ex-system',
    templateUrl: './system.component.html',
    styleUrls: ['./system.component.scss'],
    providers : [TimeserieService]
})
export class SystemComponent implements OnInit {

    private time: Object;
    public data = {
        total : <Total>{},
        active_jobs : 0,

        load : {},
        loading_load : true,

        load_total : {},
        loading_load_total : true,

        temp : {},
        loading_temp : true,

        temp_total : {},
        loading_temp_total : true,

        power : {},
        loading_power : true,

        power_total : {},
        loading_power_total : true,

        gpu_total : {},
        loading_gpu_total : true,

        fan_total : {},
        loading_fan_total : true
    };

    public chart_data = {
        cluster_load : {},
        cluster_load_loading : false
    };

    @Input('time')
    set setData(time) {
        if (time != undefined) {
            this.time = time;

            //this.fetchTotal();
            //this.getActiveJobs();

            this.fetch('load_total', 'cluster', 'UTIL_P0', this.time['to'] - this.time['from'] + 10);
            this.fetch('temp', 'cluster', 'temp_pkg', 20);
            this.fetch('temp_total', 'cluster',  'temp_pkg', this.time['to'] - this.time['from'] + 10);
            this.fetch('power', 'cluster', 'Avg_Power', 20);
            this.fetch('power_total', 'cluster', 'Avg_Power', this.time['to'] - this.time['from'] + 10);

        }
    }

    constructor(private http: HttpClient,
        private timeserie: TimeserieService) { }

    ngOnInit() {
        this.time = {
            from : (+Date.now() - env.timeoffset),
            to : +Date.now()
        };

        //this.fetchTotal();

        this.fetch('load', 'cluster', 'UTIL_P0', 20);
        this.fetch('load_total', 'cluster', 'UTIL_P0', this.time['to'] - this.time['from'] + 10);
        this.fetch('temp', 'cluster', 'TEMP_P0', 20);
        this.fetch('temp_total', 'cluster',  'TEMP_P0', this.time['to'] - this.time['from'] + 10);
        this.fetch('power', 'cluster', 'PWR_null', 20);
        this.fetch('power_total', 'cluster', 'PWR_null', this.time['to'] - this.time['from'] + 10);
        this.fetch('gpu', 'cluster', 'GPU_Power', 20);
        this.fetch('gpu_total', 'cluster', 'GPU_Power', this.time['to'] - this.time['from'] + 10);
        this.fetch('fan', 'cluster', 'Fan_Power', 20);
        this.fetch('fan_total', 'cluster', 'Fan_Power', this.time['to'] - this.time['from'] + 10);
    }

    private getActiveJobs() {
        this.http.get<Total>('/api/jobs/active').subscribe(data => {
            this.data.active_jobs = Object.keys(data).length;
        });
    }

    private fetch(dict_name, endpoint, metric: string|string[], aggregate: number = null) {
        this.data['loading_' + dict_name] = true;

        this.timeserie.fetch(this.time, dict_name, endpoint, metric, aggregate, false, 1.0).subscribe(data => {
            this.data[dict_name] = data;
            this.data['loading_' + dict_name] = false;
        });
    }

    private fetchTotal() {
        this.http.get<Total>('/jobs/stats/total', {
            params: new HttpParams()
                        .set('from', this.time['from'])
                        .set('to', this.time['to'])
        }).subscribe(data => {
            this.data.total = data;
        });
    }
}
