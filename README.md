# ExaMon Web

ExaMon is a highly scalable framework for the performance and energy monitoring of HPC servers.

ExaMon Web is the visualizer for data gathered by the ExaMon framework, IPMI and PBS. The data are stored in KairosDB and Cassandra Cluster.

To get a better picture on how it works and what is does a popularistic article was written. The article is present in this repo under `docs/` folder.

## Tools used

* Angular
* Bootstrap 4
* Dygraphs
* Python
* Flask
* pyKairosDB
* and more...


## Galileo

Absolute start of data: 1509580800[000] 11/02/2017 @ 12:00am (UTC)
Absolute end of data: 1511184044[000] 11/20/2017 @ 1:20pm (UTC)


## Jobs
3339871.io01 - no load, only C6 -> suspicious (nothing was done)
3361388.io01 - simply a bad job
3345403.io01 - 50/50 C6 and load core
3357982.io01 - simply a good job

## Possible scenarios
1) uneven load (3345507.io01 - 50/50)
2) no load at all
3) bad memory access
4) delayed start (this is fine: 3355911.io01, this one isn't 3365298.io01)
5) premature program ending (3360167.io01)
6) sudden drop (3345854.io01 - fine because of data loading)

delayed start and uneven load: 3351397.io01

long jobs suffer from environment load: 3401998.io0

drop near the end: 3347613.io01
drop near the start: 3371664.io01

nice case of dependency of metrics on each other: 3350831.io01

loading and storing: 3343636.io01
super long loading: 3419863.io01
great example of suspicious job: 3345824.io01