import { Component, OnInit, Input, SimpleChanges } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { TimeserieService } from 'app/services/timeserie.service';

interface Total {
    jobs: number;
    to : number;
    from : number;
    duration : number;
    gpus : number;
    nodes: number;
    mics : number;
    cpus : number
}

interface Data {
    total : Total;
}

@Component({
    selector: 'ex-public-overview',
    templateUrl: './public-overview.component.html',
    styleUrls: ['./public-overview.component.scss'],
    providers : [TimeserieService]
})
export class PublicOverviewComponent implements OnInit {

    private time : Object;
    public data = {};
    public chart_data = {
        cluster_load : {},
        cluster_load_loading : false
    };

    @Input('time')
    set setData(time) {
        console.log(time);
        if (time != undefined) {
            this.time = time;

            this.fetchTotal();

            //this.fetchClusterLoad();
            //this.fetchClusterTemp();

            this.fetch('load', 'cluster', 'load_core', 20);
            this.fetch('load_total', 'cluster', 'load_core', this.time['to'] - this.time['from'] + 10);
            this.fetch('temp', 'cluster', 'temp_pkg', 20);
            this.fetch('temp_total', 'cluster',  'temp_pkg', this.time['to'] - this.time['from'] + 10);
            this.fetch('power', 'cluster', 'Avg_Power', 20);
            this.fetch('power_total', 'cluster', 'Avg_Power', this.time['to'] - this.time['from'] + 10);

            console.log(this.data['power_total'])
        }
    };

    constructor(private http : HttpClient,
        private timeserie : TimeserieService) { }

    ngOnInit() { }

    private fetch(dict_name, endpoint, metric : string|string[], aggregate : number = null) {
        this.data["loading_" + dict_name] = true;

        this.timeserie.fetch(this.time, dict_name, endpoint, metric, aggregate).subscribe(data => {
            this.data[dict_name] = data;
            this.data["loading_" + dict_name] = false;
        });
    }

    private fetchTotal() {
        this.http.get<Total>('/api/jobs/stats/total', {
            params: new HttpParams()
                        .set('from', this.time['from'])
                        .set('to', this.time['to'])
        }).subscribe(data => {
            this.data = {
                total : data
            };
        })
    }
}
