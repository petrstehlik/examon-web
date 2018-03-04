import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import {BrowserModule} from "@angular/platform-browser";
import {FormsModule} from "@angular/forms";
import {HttpClientModule} from "@angular/common/http";
import {ChartsModule} from 'ng2-charts/ng2-charts';

import {GraphModule} from "../graph/graph.module";
import {SystemComponent} from './components/system/system.component';
import {MessageService} from "../../services/message.service";
import {RouterModule} from "@angular/router";

const appRoutes = [
    {
        path: 'system',
        data: {
            basepath: true,
            name: 'System',
            description: 'System',
            icon: 'fa-globe',
            role: 255
        },
        children: [
            {
                path: '',
                component: SystemComponent,
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
      RouterModule.forChild(appRoutes),
  ],
  declarations: [
      SystemComponent
  ],
    providers: [
        MessageService
    ]
})
export class SystemModule { }
