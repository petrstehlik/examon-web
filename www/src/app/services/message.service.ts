import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';

import { environment as env } from 'environments/environment';

declare const io;

@Injectable()
export class MessageService {
    private subject = new Subject<any>();

    private socket;

    constructor() {
        this.socket = io.connect(env.ws.host + ':' + env.ws.port + '/jobs');
        this.socket = io.connect(env.ws.host + ':' + env.ws.port + '/render');

        this.socket.on('connect', () => {
            console.info('Message service connected');
        });

        this.socket.on('error', (data) => {
            console.error('ERROR', data);
            this.subject.next({ text: data, type : 'danger' });
        });
    }

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
