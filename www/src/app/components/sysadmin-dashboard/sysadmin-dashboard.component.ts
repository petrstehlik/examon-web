import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'ex-sysadmin-dashboard',
  templateUrl: './sysadmin-dashboard.component.html',
  styleUrls: ['./sysadmin-dashboard.component.scss']
})
export class SysadminDashboardComponent implements OnInit {
    public job = {};
    public error = {
        message : "",
        status : false
    }

    constructor() { }

    ngOnInit() { }
}
