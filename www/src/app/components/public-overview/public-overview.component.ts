import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'ex-public-overview',
  templateUrl: './public-overview.component.html',
  styleUrls: ['./public-overview.component.scss']
})
export class PublicOverviewComponent implements OnInit {

    @Input("data")
    set setData(data) {
        console.log(data);
    };

  constructor() { }

  ngOnInit() {
  }

}
