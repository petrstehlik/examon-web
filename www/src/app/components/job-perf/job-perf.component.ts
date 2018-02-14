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

    private job: Job;
    public data = {};

    @Input('job')
    set setJob(job: Job) {
        if (job != null) {
            this.job = job;
            this.fetch('load_core', 'node', 'UTIL_P0', null,100.0);
            this.fetch('ips', 'node', ['IPS_P0']); // MIPS
            this.fetch('freq', 'node', ['FREQA_P0'], );
            this.fetch('load_core_cluster', 'cluster', 'UTIL_P0', env.window.pmu, 100.0);
            /*
            this.fetch('utils', 'node', ['Mem_Utilization', 'CPU_Utilization', 'IO_Utilization', 'Sys_Utilization'], env.window.ipmi + 5);
            this.fetch('fe_bound', 'core', 'front_end_bound');
            this.fetch('be_bound', 'core', 'back_end_bound');
            this.fetch('febe_bound', 'cluster', ['retiring', 'L1L2_bound', 'L3_bound']);
            this.fetch('cstates', 'node', ['C3res', 'C6res']);*/
        }
    }

    constructor(private timeserie: TimeserieService) { }

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
}
