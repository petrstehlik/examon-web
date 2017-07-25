import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JobPerfComponent } from './job-perf.component';

describe('JobPerfComponent', () => {
  let component: JobPerfComponent;
  let fixture: ComponentFixture<JobPerfComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JobPerfComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JobPerfComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
