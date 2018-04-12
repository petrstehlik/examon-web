import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';

import { MessageService } from 'app/services';
import { Job } from 'app/interfaces';

@Component({
  selector: 'ex-job-dashboard',
  templateUrl: './job-dashboard.component.html',
  styleUrls: ['./job-dashboard.component.scss']
})
export class JobDashboardComponent implements OnInit {

    public job = null;

    public error = {
        message : '',
        status : false
    };

    public duration = {
        days : 0,
        hours : 0,
        minutes : 0,
        seconds : 0
    };

    constructor(private http: HttpClient,
        private router: ActivatedRoute,
        private msg: MessageService) { }

    ngOnInit() {
        this.router.params.subscribe(params => {

            this.http.get('/jobs/' + params['jobid']).subscribe(
                data => {
                    this.job = new Job(params['jobid']);
                    this.job.load(data);
                    this.calcDuration();
                    this.error.status = false;
                    this.job.loaded = true;
                },
                error => {
                    console.log(error);

                    this.job = new Job();

                    if (error.status == 404) {
                        this.msg.send('Cannot find job with job ID ' + this.job.id, 'danger');
                    } else {
                        this.msg.send('Something went wrong fetching a job.', 'danger');
                    }
                }
            );
        });
    }

    /**
     * Calculate time duration of the loaded job
     *
     * Duration is computed from queue time and end time,
     * for queue time backup_time is used (more reliable)
     *
     * After calcution new property is set to the job data.
     */
    private calcDuration(): void {
        const qTime = new Date(this.job.data['start_time']);
        const eTime = new Date(this.job.data['end_time']);

        if (this.job.data['active']) {
            this.fillDuration(+Date.now() - qTime.getTime());

            setInterval(() => {
                this.fillDuration(+Date.now() - qTime.getTime());
            }, 1000);
        } else {
            this.fillDuration(eTime.getTime() - qTime.getTime());
        }
    }

    private fillDuration(difference) {
        this.duration.days = Math.floor(difference / (1000 * 60 * 60 * 24));
        this.duration.hours = Math.floor(difference / (1000 * 60 * 60) % 24);
        this.duration.minutes = Math.floor(difference / (1000 * 60) % 60);
        this.duration.seconds = Math.floor(difference / (1000) % 60);

        this.job.data['duration'] = this.duration;
    }

}
