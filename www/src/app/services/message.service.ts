import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Subject } from 'rxjs/Subject';

@Injectable()
export class MessageService {
    private subject = new Subject<any>();

    constructor() { }

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
