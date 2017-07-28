import { Component, OnInit, Input, SimpleChanges } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

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
    styleUrls: ['./public-overview.component.scss']
})
export class PublicOverviewComponent implements OnInit {

    private time : Object;
    public data : Data;
    public chart_data = {
        cluster_load : {}
    };

    @Input('time')
    set setData(time) {
        console.log(time);
        if (time != undefined) {
            this.time = time;
            this.fetchTotal();
            this.fetchClusterLoad();
        }
    };

    constructor(private http : HttpClient) { }

    ngOnInit() { }

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

    private fetchClusterLoad() {
        this.http.get('/api/kairos/load', {
            params : new HttpParams()
                        .set('from', this.time['from'])
                        .set('to', this.time['to'])
        }).subscribe(data => {
            let tmp_data = [];

            for(let key of Object.keys(data["points"])) {
                tmp_data.push([new Date(+key * 1000), ...data["points"][key]])
            }

            let tmp = {
                "labels" : ["Date", ...data["labels"]],
                "data" : tmp_data
            }

            this.chart_data["cluster_load"]  = tmp;
        });

    }

}
