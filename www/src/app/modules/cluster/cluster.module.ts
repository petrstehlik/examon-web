import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import {BrowserModule} from "@angular/platform-browser";
import {FormsModule} from "@angular/forms";
import {HttpClientModule} from "@angular/common/http";
import {ChartsModule} from 'ng2-charts/ng2-charts';

import {GraphModule} from "../graph/graph.module";
import {MessageService} from "../../services/message.service";
import {RouterModule} from "@angular/router";
import {NgbModule} from "@ng-bootstrap/ng-bootstrap";
import {RenderComponent} from "./components/render/render.component";
import {RangepickerComponent} from "./components/rangepicker/rangepicker.component";

const appRoutes = [
    {
        path: 'cluster',
        data: {
            basepath: true,
            name: 'Cluster',
            description: 'Cluster',
            icon: 'fa-server',
            role: 255
        },
        children: [
            {
                path: '',
                component: RenderComponent,
                data: {
                    role: 255
                }
            },
        ]
    }
]


@NgModule({
  imports: [
      BrowserModule,
      FormsModule,
      HttpClientModule,
      ChartsModule,
      GraphModule,
      NgbModule.forRoot(),
      RouterModule.forChild(appRoutes),
  ],
  declarations: [
      RenderComponent,
      RangepickerComponent
  ],
    providers: [
        MessageService
    ]
})
export class ClusterModule { }
