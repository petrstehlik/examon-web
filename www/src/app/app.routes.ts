import { JobSearchComponent, JobsLookupComponent, GeneralPublicViewComponent } from './components';
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
        path : 'public',
        component : GeneralPublicViewComponent
    },

    {
        path : '**',
        component : NullComponent
    },
]
