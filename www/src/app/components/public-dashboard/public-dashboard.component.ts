import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { environment as env } from 'environments/environment';

@Component({
  selector: 'ex-public-dashboard',
  templateUrl: './public-dashboard.component.html',
  styleUrls: ['./public-dashboard.component.scss']
})
export class PublicDashboardComponent implements OnInit {

    timewindow: Object = undefined;

    constructor(private http: HttpClient) { }

    ngOnInit() {
        this.timewindow = {
            from : (+Date.now() - env.timeoffset),
            to : +Date.now()
        };
    }

    public onSelect(time: Object): void {
        this.timewindow = time;
    }

}
