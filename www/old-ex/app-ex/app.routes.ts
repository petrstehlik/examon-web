import { JobInfoComponent,
    JobsLookupComponent,
    JobDashboardComponent,
    PublicDashboardComponent,
    SysadminDashboardComponent,
    SetupComponent
} from './components';
import { NullComponent } from './components';

export const appRoutes = [
    {
        path: 'examon',
        data: {
            basepath: true,
            name: 'Examon',
            description: 'Examon Web',
            role: 255
        },

        children: [
            /*{
                path: '',
                component: JobsLookupComponent,
                data: {
                    role: 10
                },
            },
            {
                path: 'jobs/:jobid',
                component: JobDashboardComponent,
                data: {
                    role: 10
                }
            },
            {
                path: 'sysadmin',
                component: SysadminDashboardComponent
            },
            {
                path: 'public',
                component: PublicDashboardComponent
            },
            {
                path: 'setup',
                component: SetupComponent
            },*/
        ]
    }
];
