import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';

import { NgbModule } from '@ng-bootstrap/ng-bootstrap'

import { appRoutes } from './app.routes';

import { AppComponent } from './app.component';
import { NullComponent } from './components/null/null.component';
import { JobInfoComponent } from './components';
import { JobsLookupComponent } from './components/jobs-lookup/jobs-lookup.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { GraphComponent } from './components/graph/graph.component';
import { GeneralPublicViewComponent } from './components/general-public-view/general-public-view.component';
import { JobDashboardComponent } from './components/job-dashboard/job-dashboard.component';

import { JobService } from 'app/services/job.service';
import { JobPerfComponent } from 'app/components/job-perf/job-perf.component';
import { JobEnergyComponent } from 'app/components/job-energy/job-energy.component';
import { SysadminDashboardComponent } from 'app/components/sysadmin-dashboard/sysadmin-dashboard.component';

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
    SysadminDashboardComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    NgbModule.forRoot(),
    RouterModule.forRoot(appRoutes)
  ],
  providers: [JobService, MessageService],
  bootstrap: [AppComponent]
})
export class AppModule { }
