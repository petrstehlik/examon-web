## How to use API as WSGI (example configuration for Apache)

This example is for Apache VirtualHost instance on https. You can of course use it without the virtualhost but remeber to include the whole Liberouter GUI part and if required, change paths accordingly.

```
<VirtualHost *:443>
    DocumentRoot "/var/www/html"
    ServerName example.com
    SSLEngine on
    SSLCertificateFile "/etc/apache2/server.crt"
    SSLCertificateKeyFile "/etc/apache2/server.key"

    ErrorLog "/var/log/apache2/secure-error\_log"
    CustomLog "/var/log/apache2/secure-access\_log" common

	# Liberouter GUI WSGI
    WSGIDaemonProcess libapi user=liberouter group=liberouter threads=5
	WSGIScriptAlias "/libapi" "/var/www/html/liberouter-gui/api/wsgi.py"
	WSGIPassAuthorization on

	<directory "/var/www/html/liberouter-gui/api">
        WSGIProcessGroup libapi
        WSGIApplicationGroup %{GLOBAL}
        WSGIScriptReloading On
        Order deny,allow
        Allow from all
    </directory>
	# END Liberouter GUI WSGI
</VirtualHost>
```
CREATE TABLE galileo\_jobs\_complexkey (
  user\_id text,
  start\_time timestamp,
  job\_id text,
  account\_name text,
  backup\_qtime timestamp,
  ctime timestamp,
  end\_time timestamp,
  job\_name text,
  mean\_power decimal,
  mem\_req bigint,
  mpiprocs int,
  ncpus\_req int,
  ngpus\_req int,
  nmics\_req int,
  nnodes\_req int,
  node\_list text,
  project text,
  qlist text,
  qtime timestamp,
  queue text,
  req\_time int,
  used\_cores text,
  used\_nodes text,
  var\_list text,
  vnode\_list text,
  PRIMARY KEY ((user\_id), start\_time, job\_id)
)
```


```
CREATE TABLE jobs\_measures\_aggregate (
  job\_id text,
  ipmi\_ambient\_temp\_list text,
  ipmi\_avg\_cpu\_util decimal,
  ipmi\_avg\_cpu\_util\_pernode text,
  ipmi\_avg\_io\_util decimal,
  ipmi\_avg\_io\_util\_pernode text,
  ipmi\_avg\_mem\_util decimal,
  ipmi\_avg\_mem\_util\_pernode text,
  ipmi\_avg\_sys\_util decimal,
  ipmi\_avg\_sys\_util\_pernode text,
  ipmi\_cpu\_utils text,
  ipmi\_io\_utils text,
  ipmi\_job\_avg\_power decimal,
  ipmi\_job\_avg\_power\_pernode text,
  ipmi\_job\_powers text,
  ipmi\_mem\_utils text,
  ipmi\_pib\_ambient\_temp\_list text,
  ipmi\_sys\_utils text,
  job\_node\_avg\_loadlist text,
  job\_node\_avg\_powerlist text,
  job\_node\_avg\_templist text,
  job\_node\_avgload\_percore text,
  job\_node\_avgtemp\_percore text,
  job\_node\_loadlist\_percore text,
  job\_node\_powers text,
  job\_node\_templist\_percore text,
  job\_tot\_avg\_load decimal,
  job\_tot\_avg\_power decimal,
  job\_tot\_avg\_temp decimal,
  PRIMARY KEY ((job\_id))
)
```

## How to run API as uwsgi
Must have installed uwsgi with ssl support and gevent

`uwsgi --http :5555 --gevent 1000 --http-websockets --wsgi-file wsgi.py  `
