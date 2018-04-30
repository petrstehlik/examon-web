import { Component, OnInit, Input } from '@angular/core';
import { environment as env } from 'environments/environment';

import { TimeserieService } from 'app/services/timeserie.service';
import { Job } from 'app/interfaces';
import { HttpClient} from "@angular/common/http";

@Component({
  selector: 'ex-job-perf',
  templateUrl: './job-perf.component.html',
    styleUrls: ['./job-perf.component.scss'],
    providers : [TimeserieService]
})
export class JobPerfComponent implements OnInit {

    private job: Job;
    public data = {};
    public resp;
    public classifier = {
        "load_core" : 0,
        "Sys_Utilization": 0,
        "IO_Utilization": 0,
        "Mem_Utilization": 0,
        "CPU_Utilization": 0,
        "L1L2_Bound": 0,
        "L3_Bound": 0,
        "C3res": 0,
        "C6res": 0,
        "ips": 0,
        "front_end_bound": 0,
        "back_end_bound": 0,
        "jobber": 0
    };

    metrics_ranged = [
        "load_core",
        "Sys_Utilization",
        "IO_Utilization",
        "Mem_Utilization",
        "CPU_Utilization",
        "L1L2_Bound",
        "L3_Bound",
        "C3res",
        "C6res"
    ]

    metrics_null = [
        "ips",
        "front_end_bound",
        "back_end_bound",
    ]

    @Input('job')
    set setJob(job: Job) {
        if (job != null) {
            this.job = job;

            for (let metric of [...this.metrics_ranged, ...this.metrics_null]) {
                this.fetch(metric, 'cluster', metric);
            }
        //     this.fetch('load_core', 'node', 'load_core');
        //     this.fetch('load_core_cluster', 'node', 'load_core', env.window.pmu);
        //     this.fetch('utils', 'node', ['Mem_Utilization', 'CPU_Utilization', 'IO_Utilization', 'Sys_Utilization'], env.window.ipmi + 5);
        //     this.fetch('fe_bound', 'node', 'front_end_bound');
        //     this.fetch('be_bound', 'node', 'back_end_bound');
        //     this.fetch('febe_bound', 'node', ['retiring', 'L1L2_bound', 'L3_bound']);
        //     this.fetch('ips', 'node', ['ips', /*'freq'*/]);
        //     this.fetch('cstates', 'node', ['C3res', 'C6res']);
        //
        }
    }

    constructor(private timeserie: TimeserieService, private http: HttpClient) { }

    ngOnInit() { }

    private fetch(dict_name,
                  endpoint,
                  metric: string|string[],
                  aggregate: number = null,
                  factor: number = 1.0) {
        this.data['loading_' + dict_name] = true;

        this.timeserie.fetch(this.job, dict_name, endpoint, metric, aggregate, false, factor).subscribe(data => {
            this.data['job_' + dict_name] = data;
            this.data['loading_' + dict_name] = false;
        });
    }

    public checkChange(event, metric) {
        this.classifier[metric] = Number(event);
    }

    public saveClassifier() {
        console.log(this.classifier);

        this.http.post('/classifier/' + this.job['id'], this.classifier).subscribe(
            data => {
                console.log(data)
                this.resp = data
            }
        )
    }
}
