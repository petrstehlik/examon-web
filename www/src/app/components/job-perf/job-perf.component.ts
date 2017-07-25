import { Component, OnInit, Input } from '@angular/core';
import { JobService } from 'app/services/job.service';
import { Job } from 'app/interfaces';

@Component({
  selector: 'ex-job-perf',
  templateUrl: './job-perf.component.html',
  styleUrls: ['./job-perf.component.scss']
})
export class JobPerfComponent implements OnInit {

    private job : Job;

    @Input("job")
    set setJob(job : Job) {
        if (job != null) {
            this.job = job;
            console.debug("Job is set, start querying.")
        }
    }

    constructor(private jobService : JobService) { }

    ngOnInit() { }

}
