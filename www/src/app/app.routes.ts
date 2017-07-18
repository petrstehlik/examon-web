import { JobSearchComponent, JobsLookupComponent } from './components';
import { NullComponent } from './components';

export const appRoutes = [
    {
        path : '',
        component : JobsLookupComponent
    },
    {
        path : 'jobs/:jobid',
        component : JobSearchComponent
    },
    {
        path : '**',
        component : NullComponent
    }
]
