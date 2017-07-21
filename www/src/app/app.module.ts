import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';

import { NgbModule } from '@ng-bootstrap/ng-bootstrap'

import { appRoutes } from './app.routes';

import { AppComponent } from './app.component';
import { NullComponent } from './components/null/null.component';
import { JobSearchComponent } from './components/job-search/job-search.component';
import { JobsLookupComponent } from './components/jobs-lookup/jobs-lookup.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { GraphComponent } from './components/graph/graph.component';
import { GeneralPublicViewComponent } from './components/general-public-view/general-public-view.component';

@NgModule({
  declarations: [
    AppComponent,
    NullComponent,
    JobSearchComponent,
    JobsLookupComponent,
    NavbarComponent,
    GraphComponent,
    GeneralPublicViewComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    NgbModule.forRoot(),
    RouterModule.forRoot(appRoutes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
