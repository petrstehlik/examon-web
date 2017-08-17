import { Component, OnInit, Input } from '@angular/core';
import { environment as env } from 'environments/environment';
import { TimeserieService } from 'app/services/timeserie.service';

@Component({
  selector: 'ex-sysadmin-overview',
  templateUrl: './sysadmin-overview.component.html',
    styleUrls: ['./sysadmin-overview.component.scss'],
    providers : [TimeserieService]
})
export class SysadminOverviewComponent implements OnInit {

    public data: Object = {};
    time: Object;

    @Input('time')
    set setData(time) {
        if (time != undefined) {
            this.time = time;
            this.fetch('utils', 'cluster', ['Mem_Utilization', 'CPU_Utilization', 'IO_Utilization', 'Sys_Utilization'], env.window.ipmi);
            this.fetch('temp', 'cluster', 'PCH_Temp', env.window.ipmi);
            this.fetch('power', 'cluster', 'Avg_Power', env.window.ipmi + 10);
        }
    }

    constructor(private timeserie: TimeserieService) { }

    ngOnInit() { }

    private fetch(dict_name, endpoint, metric: string|string[], aggregate: number = null) {
        this.data['loading_' + dict_name] = true;

        this.timeserie.fetch(this.time, dict_name, endpoint, metric, aggregate).subscribe(data => {
            this.data['job_' + dict_name] = data;
            this.data['loading_' + dict_name] = false;
        });
    }
}
