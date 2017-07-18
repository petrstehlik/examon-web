import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';

import { Job } from 'app/interfaces';

@Component({
    selector: 'app-job-search',
    templateUrl: './job-search.component.html',
    styleUrls: ['./job-search.component.scss']
})
export class JobSearchComponent implements OnInit {

    public job = new Job("2702409.io01");
    public error = {
        message : "",
        status : false
    }
    public duration = {
        days : 0,
        hours : 0,
        minutes : 0,
        seconds : 0
    };

    constructor(private http: HttpClient,
                private router : ActivatedRoute) { }

    ngOnInit() {
        this.router.params.subscribe(params => {
            this.job.id = params["jobid"];
            this.searchJob();
        })

    }

    private calcDuration() {
        let qTime = new Date(this.job.data["backup_qtime"])
        let eTime = new Date(this.job.data["end_time"])

        let difference = eTime.getTime() - qTime.getTime();
        this.duration.days = Math.floor(difference / (1000 * 60 * 60 * 24));
        this.duration.hours = Math.floor(difference / (1000 * 60 * 60) % 24);
        this.duration.minutes = Math.floor(difference / (1000 * 60) % 60);
        this.duration.seconds = Math.floor(difference / (1000) % 60);
        console.log(this.duration, qTime, eTime)
    }

    public searchJob() {
        console.info("Searching for job", this.job.id);
        this.http.get('/api/jobs/' + this.job.id).subscribe(
            data => {
                this.job.load(data);
                this.calcDuration();
                this.error.status = false;
            },
            error => {
                console.log(error);

                this.job.data = {};

                if (error.status == 404) {
                    this.error.message = "Cannot find job with job ID " + this.job.id;
                    this.error.status = true;
                }
            }
        )
    }

}
