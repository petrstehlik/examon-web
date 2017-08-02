import { Component, OnInit } from '@angular/core';
import { environment as env } from 'environments/environment';

import { MessageService } from 'app/services/message.service';

@Component({
  selector: 'ex-sysadmin-dashboard',
  templateUrl: './sysadmin-dashboard.component.html',
  styleUrls: ['./sysadmin-dashboard.component.scss']
})
export class SysadminDashboardComponent implements OnInit {

    public timewindow : Object = undefined;

    constructor(private msg : MessageService) { }

    ngOnInit() {
        this.timewindow = {
            from : (+Date.now() - env.timeoffset), // -15 mins
            to : +Date.now()
        };
    }

    public onSelect(time : Object) : void {
        this.timewindow = time;
    }
}
