import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map'

@Injectable()
export class UsersService {

    constructor(private http: HttpClient) { }

    add(user: Object) {
        return this.http.post('/users', user)
            //.pipe(this.handleError);
    }

    remove(id: string) {
        return this.http.delete('/users/' + id)
            /*.subscribe((response: Response) => {
                // User successfully added
                // Extract data from response
                const body: Object = response.json();

                return body;
            })*/
            //.pipe(this.handleError);
    }

    list() {
        return this.http.get('/users')
            /*.subscribe((response: Response) => response.json())*/
            //.pipe(this.handleError);
    }

    get(id: String) {
        return this.http.get('/users/' + id);
            //.pipe(this.handleError);
    }

    update(id: String, user: Object) {
        return this.http.put('/users/' + id, user)
            /*.subscribe((response: Response) => {
                // User successfully updated
                // Extract data from response
                const body: Object = response.json();

                return body;
            })*/
            //.pipe(this.handleError);
    }
    handleError(err: Response | any) {
        return Promise.reject(err);
    }

}

