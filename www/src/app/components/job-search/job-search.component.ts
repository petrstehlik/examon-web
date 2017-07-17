import { Component, OnInit } from '@angular/core';
import { Job } from 'app/interfaces';

@Component({
    selector: 'app-job-search',
    templateUrl: './job-search.component.html',
    styleUrls: ['./job-search.component.css']
})
export class JobSearchComponent implements OnInit {

    public job : Job = {};

    constructor() { }

    ngOnInit() {

    }

}
