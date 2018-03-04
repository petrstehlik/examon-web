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
import { Request,
    RequestOptions,
    RequestOptionsArgs,
    RequestMethod,
    URLSearchParams,
    Response,
    Http,
    Headers } from '@angular/http';
import {HttpEvent, HttpInterceptor, HttpHandler, HttpRequest} from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { Router } from '@angular/router';
import { environment } from 'environments/environment';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';

@Injectable()
export class SessionInterceptor implements HttpInterceptor {
    private currentUser: Object;
    private configPath: string = environment.configPath;
    private prefixUrl: string;
    private api: Object = {};
    private promise;

    constructor(private router: Router) {
        this.fetchConfig().then((data : string) => {
            console.info("Initializing application");

            let conf;

            try {
                conf = JSON.parse(data);
                this.api = conf['api'];
            } catch (e) {
                console.log("Error");
                console.log(e);
                let el = document.getElementById("error");
                el.innerText = "Failed to parse configuration file for front-end";
                return;
            }
        });
    }

    intercept(request : HttpRequest<any>, next : HttpHandler) : Observable<HttpEvent<any>> {
        // Prefix the URL with environment prefix if set
        let req = request.clone({
            url : this.buildUrl(request.url)
        });

        const session = localStorage.getItem('session');

        // Set Authorization header
        if (session !== null) {
            req.headers.set('Authorization', session);
        }

        // Set specific content type if "specific-content-type" header is set
        if (req.headers.has('specific-content-type')) {
            req.headers.delete('specific-content-type')
        } else {
            req.headers.set('Content-Type', 'application/json')
        }

        return next.handle(req).catch((error : any, _) => {
            if (error.status === 401) {
                localStorage.removeItem('user');
                localStorage.removeItem('session');
                this.router.navigate(['/login']);
            } else if (error.status === 442) {
                // SETUP is required
                // Maybe you ask why 442. Well, 42 is answer to everything, right?
                this.router.navigate(['/setup']);
            }
            return Observable.throw(error);
        });
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

    /**
      * Retrieve config.json from a path specified in environment
      *
      * This cannot use the Angular HTTP module, therefore uses good old XMLHttpRequest
      */
    private fetchConfig() {
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            xhr.open('GET', environment.configPath);
            xhr.onload = () => {
                if (xhr.status >= 200 && xhr.status < 300) {
                    resolve(xhr.response);
                } else {
                    reject(xhr.statusText);
                }
            };
            xhr.onerror = () => reject(xhr.statusText);
            xhr.send();
        });
    }
}

