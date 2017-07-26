import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PublicOverviewComponent } from './public-overview.component';

describe('PublicOverviewComponent', () => {
  let component: PublicOverviewComponent;
  let fixture: ComponentFixture<PublicOverviewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PublicOverviewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PublicOverviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
