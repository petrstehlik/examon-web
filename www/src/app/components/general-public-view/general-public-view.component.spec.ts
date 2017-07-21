import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GeneralPublicViewComponent } from './general-public-view.component';

describe('GeneralPublicViewComponent', () => {
  let component: GeneralPublicViewComponent;
  let fixture: ComponentFixture<GeneralPublicViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GeneralPublicViewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GeneralPublicViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
