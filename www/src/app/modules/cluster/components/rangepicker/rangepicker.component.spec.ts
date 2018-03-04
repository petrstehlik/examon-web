import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RangepickerComponent } from './rangepicker.component';

describe('RangepickerComponent', () => {
  let component: RangepickerComponent;
  let fixture: ComponentFixture<RangepickerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RangepickerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RangepickerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
