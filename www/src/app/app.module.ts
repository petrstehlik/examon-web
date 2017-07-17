import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

import { NgbModule } from '@ng-bootstrap/ng-bootstrap'

import { appRoutes } from './app.routes';

import { AppComponent } from './app.component';
import { NullComponent } from './components/null/null.component';
import { JobSearchComponent } from './components/job-search/job-search.component';

@NgModule({
  declarations: [
    AppComponent,
    NullComponent,
    JobSearchComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    NgbModule.forRoot(),
    RouterModule.forRoot(appRoutes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
