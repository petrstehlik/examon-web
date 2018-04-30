import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';

import { environment as env } from 'environments/environment';

@Injectable()
export class MessageService {
    private subject = new Subject<any>();

    private socket;

    constructor() {}


    send(message: string, type: 'warning'|'danger'|'info'|'success' = 'warning') {
        this.subject.next({ text: message, type : type });
    }

    clear() {
        this.subject.next();
    }

    get(): Observable<any> {
        return this.subject.asObservable();
    }

}
