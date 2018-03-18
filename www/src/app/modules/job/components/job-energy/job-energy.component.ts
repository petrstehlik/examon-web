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
            this.fetch('cpu', 'node', 'PWR_null');
            this.fetch('temp', 'node', 'TEMP_P0');
            this.fetch('cpu_temp', 'cpu', ["Proc0_Power", "Proc1_Power"], 10);
            this.fetch('gpu', 'node', 'GPU_Power', 10);
            this.fetch('fan', 'node', 'Fan_Power', 10);
            this.fetch('pci', 'node', ['PCIE_Proc1_Power', 'PCIE_Proc0_Pwr'], 10);
            this.fetch('mem', 'node', ['Mem_Proc0_Pwr', 'Mem_Proc1_Pwr', 'Mem_Cache_Power'], 10);
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
