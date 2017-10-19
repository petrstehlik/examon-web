import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';

import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { ChartsModule } from 'ng2-charts/ng2-charts';

import { appRoutes } from './app.routes';

import { AppComponent } from './app.component';
import { JobsLookupComponent } from './components/jobs-lookup/jobs-lookup.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { GraphComponent } from './components/graph/graph.component';

import { JobService } from 'app/services/job.service';
import { AuthService } from 'app/services/auth.service';

import { MessageService } from 'app/services';

import { MapToIterable, ObjectSize } from 'app/utils/keyIterable';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { SessionInterceptor } from 'app/utils/http.interceptor';

import {
    NullComponent,
    JobDashboardComponent,
    JobInfoComponent,
    JobPerfComponent,
    JobEnergyComponent,
    PublicDashboardComponent,
    PublicOverviewComponent,
    GeneralPublicViewComponent,
    SysadminDashboardComponent,
    SysadminOverviewComponent,
    RangepickerComponent,
    RenderComponent,
    SetupComponent } from 'app/components';

    @NgModule({
        declarations: [
            AppComponent,
            NullComponent,
            JobInfoComponent,
            JobsLookupComponent,
            NavbarComponent,
            GraphComponent,
            GeneralPublicViewComponent,
            JobDashboardComponent,
            JobPerfComponent,
            JobEnergyComponent,
            SysadminDashboardComponent,
            PublicDashboardComponent,
            PublicOverviewComponent,
            SysadminOverviewComponent,
            RangepickerComponent,
            RenderComponent,
            MapToIterable,
            ObjectSize,
            SetupComponent
        ],
        imports: [
            BrowserModule,
            FormsModule,
            HttpClientModule,
            ChartsModule,
            NgbModule.forRoot(),
            RouterModule.forRoot(appRoutes)
        ],
        providers: [
            JobService,
            MessageService,
            {
                provide: HTTP_INTERCEPTORS,
                useClass: SessionInterceptor,
                multi: true
            }
        ],
        bootstrap: [AppComponent]
    })
    export class AppModule { }
