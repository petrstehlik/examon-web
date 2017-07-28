import { Component, OnInit, Input } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
    selector: 'ex-job-info',
    templateUrl: './job-info.component.html',
    styleUrls: ['./job-info.component.scss']
})
export class JobInfoComponent implements OnInit {

    @Input("job") job;

    constructor(private modal: NgbModal) { }

    ngOnInit() {
    }
}
