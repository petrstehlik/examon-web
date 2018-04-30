/**
  * HTTP Interceptor class for liberouterapi backend communication
  *
  * The interceptor adds to every request the Authorization header with session
  * ID (if present) and prefixes each request with API URL (if set)
  *
  * Author: Petr Stehlik <stehlik@cesnet.cz>
  * Date: 15/06/2017
  */

import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest } from '@angular/common/http';
import { environment } from 'environments/environment';

@Injectable()
export class ApiInterceptor implements HttpInterceptor {
    private currentUser: Object;
    private prefixUrl: string;
    private api = {};

    constructor(private router : Router) {
        this.api = environment['config']['api'];
    }

    /**
      * For each request add:
      *     - Authorization header if session is present
      *     - API URL prefix
      */
    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

        // Prefix the URL with environment prefix if set
        const apiReq = req.clone({
            url: this.buildUrl(req.url),
            setHeaders: {
                'Authorization': localStorage.getItem('session') || '',
            }
        });

        // Set specific content type if "specific-content-type" header is set
        if (apiReq.headers.has('specific-content-type')) {
            apiReq.headers.delete('specific-content-type')
        } else {
            apiReq.headers.set('Content-Type', 'application/json')
        }

        // Call the original Http
        return next.handle(apiReq).catch(this.catchErrors());
    }

    private catchErrors() {
        return (res: Response) => {
            if (res.status === 401) {
                console.warn('Unauthorized access, remove session and user and redirect to /login');
                localStorage.removeItem('user');
                localStorage.removeItem('session');
                this.router.navigate(['/login']);
            } else if (res.status === 442) {
                // SETUP is required
                // Maybe you ask why 442. Well, 42 is answer to everything, right?
                this.router.navigate(['/setup']);
            }
            return Observable.throw(res);
        };
    }

    /**
      * Create URL string for the request based on local configuration
      */
    private buildUrl(url: string) {
        let urlString = '';

        urlString += this.api['proto'] || '';
        urlString += this.api['host'] || '';
        urlString += this.api['port'] ? ':' + this.api['port'] : '';
        urlString += this.api['url'] || environment.apiUrl || '';
        return urlString + url;
    }

}
