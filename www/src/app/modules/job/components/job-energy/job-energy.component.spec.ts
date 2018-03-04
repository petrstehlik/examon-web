import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JobEnergyComponent } from './job-energy.component';

describe('JobEnergyComponent', () => {
  let component: JobEnergyComponent;
  let fixture: ComponentFixture<JobEnergyComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JobEnergyComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JobEnergyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
