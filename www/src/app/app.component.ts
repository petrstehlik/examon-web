import { Component, OnInit } from '@angular/core';
import { Router, NavigationStart } from '@angular/router';
import { Subscription } from 'rxjs/Subscription';

import { MessageService } from './services/message.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
    message : string;
    type : string;
    subscription: Subscription;

    constructor(private msg : MessageService,
        private router : Router) { }

    ngOnInit() {
        this.subscription = this.msg.get().subscribe(
            message => {
                if (message != undefined) {
                    this.message = message.text;
                    this.type = message.type;
                } else {
                    this.message = null;
                }
            });

        this.router.events.subscribe(val => {
            if (val instanceof NavigationStart) {
                this.msg.clear();
            }
        })
    }

    close(reason) {
        this.message = null;
        this.type = null;
    }
}
