import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'ex-job-energy',
  templateUrl: './job-energy.component.html',
  styleUrls: ['./job-energy.component.scss']
})
export class JobEnergyComponent implements OnInit {

    @Input() job;

    constructor() { }

    ngOnInit() { }

}
