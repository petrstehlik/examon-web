import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { MessageService } from 'app/services';

interface Job {
    qtime : number;
    start_time : number;
    end_time : number;
    backup_qtime : number;
    ctime : number;
    mean_power : any;
    var_list : string;
    qlist : string;
    account_name : string;
    project : string;
    user_id : string;
    job_id : string;
    job_name : string;
    queue : string;
    nmics_req : number;
    ngpus_req : number;
    ncpus_req : number;
    nnodess_req : number;
    mem_req : number;
    req_time : number;
    mpiprocs : number;
    node_list : string;
    vnode_list : string;
    used_nodes : string;
    used_cores : string;
}

@Component({
  selector: 'app-jobs-lookup',
  templateUrl: './jobs-lookup.component.html',
  styleUrls: ['./jobs-lookup.component.scss']
})
export class JobsLookupComponent implements OnInit {

    public jobid : string = "";
    public lastjob : Job;
    public active_jobs = {};
    public active_jobs_id = [];

    constructor(private router : Router,
        private http : HttpClient,
        private msg : MessageService) { }

    ngOnInit() {
        this.http.get<Job>('/api/jobs/latest').subscribe(
            data => {
                this.lastjob = data;
            },
            error => {
                console.log(error);
                this.msg.send("Cannot fetch latest job", "danger");
            });

        this.http.get('/api/jobs/active').subscribe(data => {
            this.active_jobs = data;
            this.active_jobs_id = Object.keys(data);
        });

    }

    public lookup() {
        // Strip whitespace and go to given route
        this.router.navigate(["/jobs", this.jobid.trim()])
    }

}
