import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-jobs-lookup',
  templateUrl: './jobs-lookup.component.html',
  styleUrls: ['./jobs-lookup.component.scss']
})
export class JobsLookupComponent implements OnInit {

    public jobid : string;

  constructor() { }

  ngOnInit() {
  }

}
