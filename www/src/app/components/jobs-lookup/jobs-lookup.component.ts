import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { MessageService } from 'app/services';

@Component({
  selector: 'app-jobs-lookup',
  templateUrl: './jobs-lookup.component.html',
  styleUrls: ['./jobs-lookup.component.scss']
})
export class JobsLookupComponent implements OnInit {

    public jobid : string;
    public lastjob : Object;

    constructor(private router : Router,
        private http : HttpClient,
        private msg : MessageService) { }

    ngOnInit() {
        this.http.get('/api/jobs/latest').subscribe(
            data => {
                this.lastjob = data;
            },
            error => {
                console.log(error);
                this.msg.send("Cannot fetch latest job", "danger");
            });
    }

    public lookup() {
        // Strip whitespace and go to given route
        this.router.navigate(["/jobs", this.jobid.trim()])
    }

}
