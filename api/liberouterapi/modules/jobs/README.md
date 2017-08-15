# Job events structures and lifecycles
Each job lifecycle is as follows:
    jobs_runjob -> jobs_exc_begin -> jobs_exc_end

There is always only one `jobs\_runjob` event followed by `jobs\_exc\_begin` event for each node allocated by the node, the latter goes for `jobs\_exc\_end` events as well.

`backup_qtime` and `start_time` are string which need to be parsed with following strptime string: `%Y-%m-%d %H:%M:%S`. All other times are in UNIX timestamp format.

## jobs\_runjob

```JSON
{
    "project": "\_pbs\_project\_default",
    "vnode\_list": ["node239"],
    "job\_id": "2913848.io01",
    "ngpus": 0,
    "qtime": 1502791171,
    "req\_mem": "102400",
    "node\_list": ["None"],
    "job\_name": "griffin-cost",
    "queue": "xagiparallel",
    "req\_cpus": 16,
    "nmics": 0,
    "req\_time": 86400,
    "variable\_list ": {
        "PBS\_O\_SYSTEM": "Linux",
        "PBS\_O\_SHELL": "/bin/bash",
        ...
    },
    "job\_owner": "a06crs02",
    "backup\_qtime": "2017-08-15 12:03:19",
    "mpiprocs": 16,
    "Qlist": "xagiprod",
    "account\_name": "None",
    "ctime": 1502791171
}
```

## jobs\_exc\_begin
```JSON
{
    "vnode\_list": ["node341"],
    "job\_id": "2913849.io01",
    "job\_cores": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    "start\_time": "2017-08-15 12:03:20",
    "node\_list": ["node341"],
    "node\_id": "node341",
    "job\_owner": "a06crs02",
    "job\_name": "griffin-cost"
}
```

## jobs\_exc\_end
```JSON
{
    "vnode\_list": ["node239"],
    "cpupercent": 3091,
    "job\_id": "2913835.io01",
    "job\_cores": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    "used\_vmem": "22579",
    "cputime": 10216,
    "used\_mem": "22579",
    "node\_id": "node239",
    "end\_time": "2017-08-15 12:03:06",
    "node\_list": ["node239"],
    "job\_owner": "a06crs02",
    "job\_name": "griffin-formdeltag",
    "real\_walltime": 652
}
```

# Job Manager

To trigger a Job Manager's `on\_store` event the manager must hold all 3 types of events where the `jobs\_exc\_begin` and `jobs\_exc\_end` must have the same number of entries as is in `vnode\_list` of each record.

`on\_receive` event is triggered every time an event is received, processed and stored into internal dictionary.
