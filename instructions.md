## Instructions

### Setup on each proxy host

1. Install Python 3 on host

```
yum install python3
```

1. Install Python3 modules using pip. Requirements can be installed globally, or as part of a virtual environment. If using a virtual environment, edit the systemd definition file to point to the virtualenv binary instead of /usr/local.

python3 -m pip install -r proxy-server/requirements.txt

1. Copy the proxy-server directory to /opt/elastic

1. Create systemd service definition in /etc/systemd/system/proxyserver.service

```
[Unit]
Description=Gunicorn instance to serve proxy server
After=network.target

[Service]
User=root
Group=root

WorkingDirectory=/opt/elastic/proxy-server
ExecStart=/usr/local/bin/gunicorn --bind 0.0.0.0:9990 wsgi:api


[Install]
WantedBy=multi-user.target
```

1. Install Metricbeat on the instance. Configure `elasticsearch.output` to send events to the ECE logging and metrics cluster

1. Copy modules.d configuration files for the `http` and `docker` module to /etc/metricbeat/modules.d/

1. Enable and start proxyserver service

```
systemctl enable proxyserver
systemctl start proxyserver
```

1. Enable and start Metricbeat service

```
systemctl enable metricbeat
systemctl start metricbeat
```