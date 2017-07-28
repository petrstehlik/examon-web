import { Component, OnInit, Output, EventEmitter, ViewChild } from '@angular/core';
import { NgbDateStruct, NgbTimeStruct } from '@ng-bootstrap/ng-bootstrap';
import { environment as env } from 'environments/environment';

interface Time {
    from : number;
    to : number;
}

@Component({
    selector: 'ex-rangepicker',
    templateUrl: './rangepicker.component.html',
    styleUrls: ['./rangepicker.component.scss']
})
export class RangepickerComponent implements OnInit {

    @Output("onSelect")
    select : EventEmitter<Object> = new EventEmitter<Object>();

    @ViewChild("dropdown") dropdown;

    public intervals_minutes : Array<number> = [1, 2, 5, 10, 15, 30, 45];
    public intervals_hours : Array<number> = [1, 2, 3, 6, 12, 24, 48];

    from_date: NgbDateStruct;
    from_time: NgbTimeStruct;
    to_date: NgbDateStruct;
    to_time: NgbTimeStruct;
    query : Time;

    constructor() { }

    ngOnInit() {
        this.reset();
    }

    /**
      * Manually adjust date in query since we are using it as a composite
      * for both the date and time
      */
    selectDate(event, type : "to" | "from") {
        let prev = new Date(this.query[type]);

        if (event['hour'] && event['minute']) {
            prev.setMinutes(event['minute']);
            prev.setHours(event['hour']);
        } else {
            prev.setFullYear(event['year']);
            prev.setMonth(event['month']);
            prev.setDate(event['day']);
        }

        this.query[type] = prev.getTime();

        console.log(this.query)
    }

    /**
     * Select a relative interval for query
     */
    selectInterval(mins : number) {
        this.query = {
            from : +Date.now() - mins*60000,
            to : +Date.now()
        }

        this.apply();
    }

    apply() {
        this.select.emit(this.query);
        this.dropdown.close();
    }

    private reset(params = {}) {
        const from_time = new Date();
        const to_time = new Date();

        this.query = {
            from : +Date.now() - env.timeoffset,
            to : +Date.now()
        }

        this.from_date = {
            year: from_time.getFullYear(),
            month: from_time.getMonth(),
            day: from_time.getDate()
        }
        this.from_time = {
            hour : (from_time.getHours() - 1),
            minute : from_time.getMinutes(),
            second : 0
        }

        this.to_date = {
            year: to_time.getFullYear(),
            month: to_time.getMonth(),
            day: to_time.getDate()
        }
        this.to_time = {
            hour : to_time.getHours(),
            minute : to_time.getMinutes(),
            second : 0
        }
    }
}
