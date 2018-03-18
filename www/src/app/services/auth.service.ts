import { Injectable } from '@angular/core';
import { HttpClient} from "@angular/common/http";
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';
import { Subject} from "rxjs/Subject";

@Injectable()
export class AuthService {
    subject = new Subject();

    constructor(private http: HttpClient) { }

    login(username: string, password: string) {
        console.log("logging in")
        return this.http.post('/authorization',{ username: username, password: password });
    }

    logout() {
        // remove user from local storage to log user out
        const user = JSON.parse(localStorage.getItem('user'));
        console.log(user);
        return this.http.delete('/authorization');

    }

    public checkSession() {
        console.log(localStorage.getItem('session'));
        return this.http.get('/authorization');
    }

    admin(user: Object) {
        return this.http.post('/setup', user);
    }

    private handleError(err: Response | any) {
        return Promise.reject(err);
    }
}
