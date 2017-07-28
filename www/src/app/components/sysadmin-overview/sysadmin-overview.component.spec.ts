import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SysadminOverviewComponent } from './sysadmin-overview.component';

describe('SysadminOverviewComponent', () => {
  let component: SysadminOverviewComponent;
  let fixture: ComponentFixture<SysadminOverviewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SysadminOverviewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SysadminOverviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
