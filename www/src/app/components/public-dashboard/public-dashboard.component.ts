import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

@Component({
  selector: 'ex-public-dashboard',
  templateUrl: './public-dashboard.component.html',
  styleUrls: ['./public-dashboard.component.scss']
})
export class PublicDashboardComponent implements OnInit {

    data : Object = {};

    constructor(private http : HttpClient) { }

    ngOnInit() {
    }

    public onSelect(time : Object) : void {
        this.http.get('/api/jobs/stats/total', {
            params: new HttpParams()
                        .set('from', time['from'])
                        .set('to', time['to'])
        }).subscribe(data => {
            this.data["total"] = data;
        })
    }

}
