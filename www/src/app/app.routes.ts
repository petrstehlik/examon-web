import { JobInfoComponent,
    JobsLookupComponent,
    JobDashboardComponent,
    GeneralPublicViewComponent,
    SysadminDashboardComponent
} from './components';
import { NullComponent } from './components';

export const appRoutes = [
    {
        path : '',
        component : JobsLookupComponent
    },
    {
        path : 'jobs/:jobid',
        component : JobDashboardComponent
    },
    {
        path : 'sysadmin',
        component : SysadminDashboardComponent
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
