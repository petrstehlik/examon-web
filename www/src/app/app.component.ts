import { Component } from '@angular/core';
import { Subscription } from 'rxjs/Subscription';

import { MessageService } from './services/message.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
    message: any;
    subscription: Subscription;

    constructor(private msg : MessageService) {
        this.subscription = this.msg.getMessage().subscribe(
            message => {
                this.message = message;
            });
    }
}
