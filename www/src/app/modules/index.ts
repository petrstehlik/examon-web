import { JobModule } from './job/job.module';
import { SystemModule} from "./system/system.module";
import { ClusterModule } from './cluster/cluster.module';
import { UsersModule } from './users/users.module';

export { AppPipesModule } from "./app-pipes/app-pipes.module";
export { GraphModule } from './graph/graph.module';

export const modules: Array<Object> = [UsersModule, JobModule];
