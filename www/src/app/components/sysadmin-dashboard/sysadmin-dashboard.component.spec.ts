import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SysadminDashboardComponent } from './sysadmin-dashboard.component';

describe('SysadminDashboardComponent', () => {
  let component: SysadminDashboardComponent;
  let fixture: ComponentFixture<SysadminDashboardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SysadminDashboardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SysadminDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
