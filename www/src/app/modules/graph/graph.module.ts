import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { GraphComponent} from "./graph/graph.component";
import {BrowserModule} from "@angular/platform-browser";

@NgModule({
  imports: [
      BrowserModule
  ],
  declarations: [
      GraphComponent
  ],
    exports: [
        GraphComponent
    ]
})
export class GraphModule { }
