import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule, Http, Request, XHRBackend, RequestOptions} from '@angular/http';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule, Routes, Router } from '@angular/router';

import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { AppComponent } from './app.component';
import { HomeComponent } from './components/';
import { LoginComponent } from './components/';
import { LogoutComponent } from './components/';
import { SetupComponent } from './components/';
import { NullComponent } from './components/';

import { AuthGuard } from './utils/auth.guard';
import { ApiInterceptor } from './utils/http.interceptor';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { SafePipe, SafePipeModule } from './utils/safe.pipe';

import { AppConfigService } from 'app/services/app-config.service';

import { modules } from './modules';

/**
  * Basic routes of the application
  */
const appRoutes: Routes = [
    {
        path : 'login',
        component : LoginComponent
    },
    {
        path : 'logout',
        component : LogoutComponent,
        canActivate : [AuthGuard]
    },
    {
        path : 'setup',
        component : SetupComponent
    },
    {
        path: '',
        component: HomeComponent,
        canActivate : [AuthGuard]
    },
    {
        path: '**',
        component: NullComponent
    }
];

export function httpFactory(router: Router,
                            appconfig: AppConfigService): ApiInterceptor {
    return new ApiInterceptor(router);
}

/**
  * Initialization class for the whole application
  */
@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    LoginComponent,
    LogoutComponent,
    SetupComponent,
    NullComponent,
  ],
  imports: [
      modules,
      SafePipeModule,
      BrowserModule,
      FormsModule,
      HttpClientModule,
      HttpModule,
      NgbModule.forRoot(),
      RouterModule.forRoot(appRoutes)
  ],
  providers: [
    AuthGuard,
    SafePipe,
    AppConfigService,
    {
        provide : HTTP_INTERCEPTORS,
        useFactory: (httpFactory),
        deps: [Router, AppConfigService],
        multi: true,
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
