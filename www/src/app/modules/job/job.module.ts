import { NgModule } from '@angular/core';
import {BrowserModule} from "@angular/platform-browser";
import { RouterModule } from '@angular/router';
import {FormsModule} from "@angular/forms";
import {HttpClientModule} from "@angular/common/http";
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { ChartsModule } from 'ng2-charts/ng2-charts';

import {
    JobInfoComponent,
    JobPerfComponent,
    JobEnergyComponent,
    JobDashboardComponent,
    JobsLookupComponent
} from './components';
import {AppPipesModule} from "app/modules/app-pipes/app-pipes.module";
import {GraphModule} from "../graph/graph.module";
import {JobService} from "../../services/job.service";
import {MessageService} from "../../services/message.service";

const appRoutes = [
    {
        path: 'jobs',
        data: {
            basepath: true,
            name: 'Jobs',
            description: 'Job-related info',
            icon: 'fa-tachometer',
            role: 255
        },
        children: [
            {
                path: '',
                component: JobsLookupComponent,
                data: {
                    role: 255
                }
            },
            {
                path: ':jobid',
                component: JobDashboardComponent,
            }
        ]
    }
];

@NgModule({
  imports: [
      BrowserModule,
      FormsModule,
      HttpClientModule,
      AppPipesModule,
      ChartsModule,
      GraphModule,
      NgbModule.forRoot(),
      RouterModule.forChild(appRoutes),
  ],
  declarations: [
      JobInfoComponent,
      JobPerfComponent,
      JobEnergyComponent,
      JobDashboardComponent,
      JobsLookupComponent
  ],
    providers: [
        JobService,
        MessageService
    ]

})
export class JobModule { }
