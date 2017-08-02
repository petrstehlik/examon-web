import { Component, OnInit, Input } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { JobService } from 'app/services/job.service';
import { Job } from 'app/interfaces';

@Component({
  selector: 'ex-job-perf',
  templateUrl: './job-perf.component.html',
  styleUrls: ['./job-perf.component.scss']
})
export class JobPerfComponent implements OnInit {

    private job : Job;
    public data = {};

    @Input("job")
    set setJob(job : Job) {
        if (job != null) {
            this.job = job;
            console.debug("Job is set, start querying.");
            //this.fetchLoad();
            this.fetch('utils', 'node', ['Mem_Utilization', 'CPU_Utilization', 'IO_Utilization', 'Sys_Utilization']);
            this.fetch('load_core', 'core', 'load_core');
            this.fetch('fe_bound', 'core', 'front_end_bound');
            this.fetch('be_bound', 'core', 'back_end_bound');
            this.fetch('ips', 'core', 'ips');
            this.fetch('cstates', 'node', ['C3res', 'C6res']);
        }
    }

    constructor(private http : HttpClient) { }

    ngOnInit() { }

    private fetchLoad() {
        this.data["loading"] = true;

        let params = new HttpParams();

        for (let key of this.job["data"]["asoc_nodes"]) {
            params = params.append('node', key["node"])
        }

        params = params.set('from', this.job['data']["start_time"])
            .set('to', this.job['data']["end_time"])
            .set('metric', "load_core")

        this.http.get('/api/kairos/core', {
          params : params
        }).subscribe(data => {
            let tmp_data = [];

            for(let key of Object.keys(data["points"])) {
                tmp_data.push([new Date(+key * 1000), ...data["points"][key]])
            }

            let tmp = {
                "labels" : ["Date", ...data["labels"]],
                "data" : tmp_data
            }

            this.data["job_load"]  = tmp;
            this.data["loading"] = false;
        });
    }

    private fetchMemUtil() {
        this.fetch('mem_util', 'node', 'Mem_Utilization');
    }

    private fetch(dict_name, endpoint, metric : string|string[]) {
        this.data["loading_" + dict_name] = true;

        let params = new HttpParams();

        for (let key of this.job["data"]["asoc_nodes"]) {
            params = params.append('node', key["node"])
        }

        params = params.set('from', this.job['data']["start_time"])
            .set('to', this.job['data']["end_time"])

        if (metric.constructor == Array) {
            for (let item of metric) {
                params = params.append('metric', item)
            }
        } else {
            params = params.set('metric', String(metric));
        }

        this.http.get('/api/kairos/' + endpoint, {
          params : params
        }).subscribe(data => {
            let tmp_data = [];

            for(let key of Object.keys(data["points"])) {
                tmp_data.push([new Date(+key * 1000), ...data["points"][key]])
            }

            let tmp = {
                "labels" : ["Date", ...data["labels"]],
                "data" : tmp_data
            }

            this.data["job_" + dict_name]  = tmp;
            this.data["loading_" + dict_name] = false;
        });

    }


}
