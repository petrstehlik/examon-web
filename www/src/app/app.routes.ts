import { JobSearchComponent } from './components';
import { NullComponent } from './components';

export const appRoutes = [
    {
        path : '',
        component : JobSearchComponent
    },
    {
        path : '**',
        component : NullComponent
    }
]
