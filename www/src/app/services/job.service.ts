import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { Job } from 'app/interfaces';

@Injectable()
export class JobService {

    public error = {
        message : '',
        status : false
    };

    public job = new Job();

    public duration = {
        days : 0,
        hours : 0,
        minutes : 0,
        seconds : 0
    };

    constructor(public http: HttpClient) { }

    fetch(jobid: string) {
        return new Observable(
            observer => this.http.get('/api/jobs/' + jobid).subscribe(
                data => {
                    console.log(data);
                    this.job.load(data);
                    this.calcDuration();
                    this.error.status = false;
                    observer.next();
                },
                error => {
                    console.log(error);

                    this.job.data = {};

                    if (error.status == 404) {
                        this.error.message = 'Cannot find job with job ID ' + this.job.id;
                        this.error.status = true;
                    }
                }
            ));
    }

    load(data) {
        this.job.load(data);
        this.calcDuration();
    }

    data() {
        return this.job.data;
    }

    private calcDuration() {
        const qTime = new Date(this.job.data['backup_qtime']);
        const eTime = new Date(this.job.data['end_time']);

        const difference = eTime.getTime() - qTime.getTime();
        this.duration.days = Math.floor(difference / (1000 * 60 * 60 * 24));
        this.duration.hours = Math.floor(difference / (1000 * 60 * 60) % 24);
        this.duration.minutes = Math.floor(difference / (1000 * 60) % 60);
        this.duration.seconds = Math.floor(difference / (1000) % 60);
    }

}
