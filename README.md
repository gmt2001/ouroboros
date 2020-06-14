
<img width="800" src="https://raw.githubusercontent.com/gmt2001/ouroboros/master/assets/ouroboros_logo_primary_long_cropped.jpg" alt="Ouroboros Logo">

Automatically update your running Docker containers to the latest available image.

The de-facto standard for docker update automation

Forked from the original at https://github.com/pyouroboros/ouroboros/

## Overview

Ouroboros will monitor (all or specified) running docker containers and update them to the (latest or tagged) available image in the remote registry. The updated container uses the same tag and parameters that were used when the container was first created such as volume/bind mounts, docker network connections, environment variables, restart policies, entrypoints, commands, etc.

- Push your image to your registry and simply wait your defined interval for ouroboros to find the new image and redeploy your container autonomously.
- Notify you via many platforms courtesy of [Apprise](https://github.com/caronc/apprise) 
- Serve metrics for trend monitoring (Currently: Prometheus/Influxdb)
- Limit your server ssh access
- `ssh -i key server.domainname "docker pull ... && docker run ..."` is for scrubs
- `docker-compose pull && docker-compose up -d` is for fancier scrubs

## Getting Started

More detailed usage and configuration can be found on [the wiki](https://github.com/pyouroboros/ouroboros/wiki).

### Docker

Ouroboros is deployed via docker image like so:

```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  gmt2001/ouroboros
```

> This is image is compatible for amd64, arm64, and arm/v7 CPU architectures

or via `docker-compose`:

[Official Example](docker-compose.yml)

### Pip

Ouroboros can also be installed via `pip`:

```bash
pip install ouroboros-cli
```

And can then be invoked using the `ouroboros` command:

```bash
$ ouroboros --interval 300 --log-level debug
```

> This can be useful if you would like to create a `systemd` service or similar daemon that doesn't run in a container

## Examples
Per-command and scenario examples can be found in the [wiki](https://github.com/pyouroboros/ouroboros/wiki/Usage)

## Contributing

All contributions are welcome! Contributing guidelines are in the works
