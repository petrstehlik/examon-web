import { Component, OnInit } from '@angular/core';
import { MessageService } from 'app/services/message.service';

@Component({
  selector: 'ex-sysadmin-dashboard',
  templateUrl: './sysadmin-dashboard.component.html',
  styleUrls: ['./sysadmin-dashboard.component.scss']
})
export class SysadminDashboardComponent implements OnInit {

    constructor(private msg : MessageService) { }

    ngOnInit() { }
}
