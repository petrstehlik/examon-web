import { Component, OnInit, Input } from '@angular/core';
import { TimeserieService } from 'app/services/timeserie.service';
import { Job } from 'app/interfaces';

@Component({
    selector: 'ex-job-energy',
    templateUrl: './job-energy.component.html',
    styleUrls: ['./job-energy.component.scss'],
    providers : [TimeserieService]
})
export class JobEnergyComponent implements OnInit {

    public data = {};
    private job: Job;

    @Input('job')
    set setJob(job: Job) {
        if (job != null) {
            this.job = job;
            this.fetch('power', 'node', 'Avg_Power', 20);
            this.fetch('temp', 'node', ['CPU1_Temp', 'CPU2_Temp'], 20);
            this.fetch('cpu_dram_power', 'cpu', ['pow_dram', 'pow_pkg'], 2);
        }
    }

    constructor(private timeserie: TimeserieService) { }

    ngOnInit() { }

    private fetch(dict_name, endpoint, metric: string|string[], aggregate: number = null) {
        this.data['loading_' + dict_name] = true;

        this.timeserie.fetch(this.job, dict_name, endpoint, metric, aggregate).subscribe(data => {
            this.data['job_' + dict_name] = data;
            this.data['loading_' + dict_name] = false;
        });
    }
}
