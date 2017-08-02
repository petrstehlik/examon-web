import { TestBed, inject } from '@angular/core/testing';

import { TimeserieService } from './timeserie.service';

describe('TimeserieService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [TimeserieService]
    });
  });

  it('should be created', inject([TimeserieService], (service: TimeserieService) => {
    expect(service).toBeTruthy();
  }));
});
