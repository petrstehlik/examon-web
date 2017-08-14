import { Component, OnInit } from '@angular/core';

import { MessageService } from 'app/services/message.service';

@Component({
  selector: 'ex-general-public-view',
  templateUrl: './general-public-view.component.html',
  styleUrls: ['./general-public-view.component.scss']
})
export class GeneralPublicViewComponent implements OnInit {

  constructor(private message: MessageService) { }

    ngOnInit() { }

}
