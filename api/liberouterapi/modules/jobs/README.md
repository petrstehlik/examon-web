# Job events structures and lifecycles
Each job lifecycle is as follows:
    jobs_runjob -> jobs_exc_begin -> jobs_exc_end

There is always only one `jobs_runjob` event followed by `jobs_exc_begin` event for each node allocated by the node, the latter goes for `jobs_exc_end` events as well.

`backup_qtime` and `start_time` are string which need to be parsed with following strptime string: `%Y-%m-%d %H:%M:%S`. All other times are in UNIX timestamp format.

## jobs\_runjob

```JSON
{
    "project": "_pbs_project_default",
    "vnode_list": ["node239"],
    "job_id": "2913848.io01",
    "ngpus": 0,
    "qtime": 1502791171,
    "req_mem": "102400",
    "node_list": ["None"],
    "job_name": "griffin-cost",
    "queue": "xagiparallel",
    "req_cpus": 16,
    "nmics": 0,
    "req_time": 86400,
    "variable_list ": {
        "PBS_O_SYSTEM": "Linux",
        "PBS_O_SHELL": "/bin/bash",
        ...
    },
    "job_owner": "a06crs02",
    "backup_qtime": "2017-08-15 12:03:19",
    "mpiprocs": 16,
    "Qlist": "xagiprod",
    "account_name": "None",
    "ctime": 1502791171
}
```

## jobs\_exc\_begin
```JSON
{
    "vnode_list": ["node341"],
    "job_id": "2913849.io01",
    "job_cores": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    "start_time": "2017-08-15 12:03:20",
    "node_list": ["node341"],
    "node_id": "node341",
    "job_owner": "a06crs02",
    "job_name": "griffin-cost"
}
```

## jobs\_exc\_end
```JSON
{
    "vnode_list": ["node239"],
    "cpupercent": 3091,
    "job_id": "2913835.io01",
    "job_cores": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    "used_vmem": "22579",
    "cputime": 10216,
    "used_mem": "22579",
    "node_id": "node239",
    "end_time": "2017-08-15 12:03:06",
    "node_list": ["node239"],
    "job_owner": "a06crs02",
    "job_name": "griffin-formdeltag",
    "real_walltime": 652
}
```

# Job Manager

To trigger a Job Manager's `on_store` event the manager must hold all 3 types of events where the `jobs_exc_begin` and `jobs_exc_end` must have the same number of entries as is in `vnode_list` of each record.

`on_receive` event is triggered every time an event is received, processed and stored into internal dictionary.
