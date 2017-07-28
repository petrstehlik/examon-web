import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

@Component({
  selector: 'ex-public-dashboard',
  templateUrl: './public-dashboard.component.html',
  styleUrls: ['./public-dashboard.component.scss']
})
export class PublicDashboardComponent implements OnInit {

    timewindow : Object = undefined;

    constructor(private http : HttpClient) { }

    ngOnInit() {
        this.timewindow = {
            from : (+Date.now() - 900000), // -15 mins
            to : +Date.now()
        };
        console.log(this.timewindow)
    }

    public onSelect(time : Object) : void {
        this.timewindow = time;
    }

}
