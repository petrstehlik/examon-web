import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { MessageService } from 'app/services';

@Injectable()
export class TimeserieService {

    constructor(private http : HttpClient,
         private msg : MessageService) { }

    /**
     * General method for fetching data from API in a dygraphs-friendly format
     *
     * Some transformations must be done anyway but still better than doing everything in front-end
     */
    fetch(job,
        dict_name,
        endpoint,
        metric : string|string[],
        aggregate : number = null,
        raw : boolean = false) {
        return new Observable(observer =>
            this.http.get('/api/kairos/' + endpoint, {
              params : this.prepareParams(job, metric, aggregate)
            }).subscribe(data => {
                if (raw)
                    observer.next(data);
                else
                    observer.next(this.parseData(data));
            }, error => {
                this.msg.send("Something went wrong for '" + dict_name + "' (status: " + String(error.status) +")", "danger");
            }));
    }

    private prepareParams(job, metric, aggregate) : HttpParams {
        let params = new HttpParams();

        if ("data" in job) {
            for (let key of job["data"]["asoc_nodes"]) {
                params = params.append('node', key["node"]);
            }

            params = params.set('from', job['data']["start_time"])
                .set('to', job['data']["end_time"])
        } else {
            params = params.set('from', job["from"])
                .set('to', job["to"])
        }

        if (metric.constructor == Array) {
            for (let item of metric) {
                params = params.append('metric', item);
            }
        } else {
            params = params.set('metric', String(metric));
        }

        if (aggregate !== null) {
            params = params.set('aggregate', String(aggregate));
        }

        return params;
    }

    private parseData(data : Object) : Object {
        let tmp_data = [];

        for(let key of Object.keys(data["points"])) {
            tmp_data.push([new Date(+key * 1000), ...data["points"][key]]);
        }

        let tmp = {
            "labels" : ["Date", ...data["labels"]],
            "data" : tmp_data
        }

        return tmp;
    }
}
