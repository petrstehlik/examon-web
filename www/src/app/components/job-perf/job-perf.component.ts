import { Component, OnInit, Input } from '@angular/core';
import { environment as env } from 'environments/environment';

import { JobService } from 'app/services/job.service';
import { TimeserieService } from 'app/services/timeserie.service';
import { Job } from 'app/interfaces';

@Component({
  selector: 'ex-job-perf',
  templateUrl: './job-perf.component.html',
    styleUrls: ['./job-perf.component.scss'],
    providers : [TimeserieService]
})
export class JobPerfComponent implements OnInit {

    private job : Job;
    public data = {};

    @Input("job")
    set setJob(job : Job) {
        if (job != null) {
            this.job = job;
            this.fetch('utils', 'node', ['Mem_Utilization', 'CPU_Utilization', 'IO_Utilization', 'Sys_Utilization'], env.window.ipmi);
            this.fetch('load_core', 'core', 'load_core');
            this.fetch('fe_bound', 'core', 'front_end_bound');
            this.fetch('be_bound', 'core', 'back_end_bound');
            this.fetch('ips', 'core', 'ips');
            this.fetch('cstates', 'node', ['C3res', 'C6res']);
        }
    }

    constructor(private timeserie : TimeserieService) { }

    ngOnInit() { }

    private fetch(dict_name, endpoint, metric : string|string[], aggregate : number = null) {
        this.data["loading_" + dict_name] = true;

        this.timeserie.fetch(this.job, dict_name, endpoint, metric, aggregate).subscribe(data => {
            this.data["job_" + dict_name] = data;
            this.data["loading_" + dict_name] = false;
        });
    }
}
