import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-jobs-lookup',
  templateUrl: './jobs-lookup.component.html',
  styleUrls: ['./jobs-lookup.component.scss']
})
export class JobsLookupComponent implements OnInit {

    public jobid : string;

  constructor(private router : Router) { }

  ngOnInit() {
  }

  public lookup() {
  console.log(this.jobid)
    // Strip whitespace and go to given route
    this.router.navigate(["/jobs", this.jobid.trim()])
  }

}
