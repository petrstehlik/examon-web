import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { Job } from '../../interfaces';

@Component({
  selector: 'ex-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {

    public job: Job = new Job('');

  constructor(private router: ActivatedRoute) { }

  ngOnInit() {
      this.router.params.subscribe(params => {
            this.job.id = params['jobid'];
        });
  }

}
