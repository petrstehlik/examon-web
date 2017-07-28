import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JobsLookupComponent } from './jobs-lookup.component';

describe('JobsLookupComponent', () => {
  let component: JobsLookupComponent;
  let fixture: ComponentFixture<JobsLookupComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JobsLookupComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JobsLookupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
