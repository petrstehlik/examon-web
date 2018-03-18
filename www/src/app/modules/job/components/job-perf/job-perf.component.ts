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
            this.fetch('utilization', 'core', 'UTIL_P0', null,1.0);
            this.fetch('ips', 'node', ['IPS_P0']); // MIPS
            this.fetch('freq', 'node', ['FREQA_P0'], );
            //this.fetch('load_core_cluster',  'cluster', 'UTIL_P0', env.window.pmu, 1.0);
            this.fetch('notfin', 'core', ['NOTFIN_P0', 'NOTBZE_P0']);
            this.fetch('volt', 'core', ['VOLT_V0', 'VOLT_V1'], null, 0.1);
            this.fetch('mem_rd', 'core', ['MRD_P0', 'MWR_P0']);
            this.fetch('l4', 'core', ['M4RD_MEM', 'M4WR_MEM']);
            /*
            this.fetch('utils', 'node', ['Mem_Utilization', 'CPU_Utilization', 'IO_Utilization', 'Sys_Utilization'], env.window.ipmi + 5);
            this.fetch('be_bound', 'core', 'back_end_bound');
            this.fetch('fe_bound', 'core', 'front_end_bound');
            */
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
