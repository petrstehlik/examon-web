import { Component, OnInit, Input } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

import { Job } from 'app/interfaces/job';

import { TimeserieService } from 'app/services/timeserie.service';

@Component({
    selector: 'ex-job-info',
    templateUrl: './job-info.component.html',
    styleUrls: ['./job-info.component.scss'],
    providers : [TimeserieService]
})
export class JobInfoComponent implements OnInit {

    public job : Job = new Job();
    public data : Object = {};

    @Input("job")
    set setJob(data) {
        if (data != undefined) {
            console.log(data);
            this.job = data;
            this.fetchRaw("load_core", "core", "load_core", this.aggWindow()*10);
            console.log(this.data)
        }
    }

    constructor(private modal: NgbModal,
        private timeserie : TimeserieService) { }

    ngOnInit() {
    }

    private fetch(dict_name,
        endpoint,
        metric : string|string[],
        aggregate : number = null)
    {
        this.data["loading_" + dict_name] = true;

        this.timeserie.fetch(this.job, dict_name, endpoint, metric, aggregate).subscribe(data => {
            this.data["job_" + dict_name] = data;
            this.data["loading_" + dict_name] = false;
        });
    }

    private fetchRaw(dict_name,
        endpoint,
        metric : string|string[],
        aggregate : number = null)
    {
        this.data["loading_" + dict_name] = true;

        this.timeserie.fetch(this.job,
            dict_name,
            endpoint,
            metric,
            aggregate,
            true)
            .subscribe(data => {
                let tmp_data = {data : [], labels : []};

                let key = Object.keys(data["points"])[0];

                for (var i = 0; i < data["labels"].length; i++) {
                    tmp_data["data"].push([i, data["points"][key][i]]);
                }

                //tmp_data["data"] = data["points"][Object.keys(data["points"])[0]];
                tmp_data["labels"] = ["Core", "Load"]//data["labels"];

                this.data["job_" + dict_name] = tmp_data;
                this.data["loading_" + dict_name] = false;
            });
    }


    /**
     * Get an exact time duration of the job in order to aggregate to one single number
     */
    private aggWindow() : number {
        return(Math.floor(this.job["data"]["end_time"] - this.job["data"]["backup_qtime"])/1000);
    }

}
