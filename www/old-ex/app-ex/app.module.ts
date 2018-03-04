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

import { JobService } from './services/job.service';

import { MessageService } from 'app/services';

import { MapToIterable, ObjectSize } from 'app/utils/keyIterable';

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
    SetupComponent } from './components';
import {GraphModule} from "../graph/graph.module";

    @NgModule({
        declarations: [
            AppComponent,
            NullComponent,
            //JobInfoComponent,
            JobsLookupComponent,
            NavbarComponent,
            GeneralPublicViewComponent,
            //JobDashboardComponent,
            JobPerfComponent,
            JobEnergyComponent,
            SysadminDashboardComponent,
            PublicDashboardComponent,
            PublicOverviewComponent,
            SysadminOverviewComponent,
            RangepickerComponent,
            RenderComponent,
            SetupComponent
        ],
        imports: [
            BrowserModule,
            FormsModule,
            HttpClientModule,
            ChartsModule,
            GraphModule,
            NgbModule.forRoot(),
            RouterModule.forChild(appRoutes)
        ],
        providers: [
            JobService,
            MessageService,
        ]
    })
    export class ExamonModule { }
