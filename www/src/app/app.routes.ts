import { JobInfoComponent,
    JobsLookupComponent,
    JobDashboardComponent,
    PublicDashboardComponent,
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
        component : PublicDashboardComponent
    },

    {
        path : '**',
        component : NullComponent
    },
]
