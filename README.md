# NBN-Pi-Core
A highly resilient Zero-Conf (Plug & Play) solution to remotely manage any LAN using failproof SSH tunnels.
NBN-Pi maintains an persistent SSH tunnel to a host (Eg: Raspberry Pi) using a set of resilient/failproof mechanisms.

![NBN-Pi Tunneling](https://github.com/NassimBentarka/NBN-Pi-Core/raw/main/docs/assets/NBN-Pi-Core%20Diagram.png)

The primary use case is maintaining a persistent reverse SSH tunnel to a proxy SSH server. Thus, the local device can be accessed without using incoming connections that may be blocked by a NAT or firewall or otherwise impractical with mobile/cellular networks.

SSH clients can connect to the device via the proxy SSH server that NBN-Pi tunnels to. This proxy server does not have to be trusted as long as it will not have access the SSH identities of hosts.

NBN-Pi enables SSH keepalives and retries SSH with exponential backoff. In order to reconnect as soon as possible, it resets the backoff when a network interface is brought up (or changed) using SIGUSR1. It also uses a daemon as an external agent to constantly check for loss of internet connection, reconnect, and kills any "zombie" SSH sessions.

#### Practical use cases/ideas

 * Access a web application behind a NAT by remote forwarding the local web server (e.g., port 80). A remote server can host a reverse proxy to the web application and handle SSL/TLS termination and even enforce SSL on the Edge using Cloudflare.
 * Remotely control a Drone, UAV, RV, or any network over cellular or satellite connectivity in a fully resilient way.
 * For IT support companies: remotely access clients' networks by plugging a RPi and leaving site without having to deal with time consuming firewalls and router configurations.
 * Stay connected to office network services behind an SSH [bastion host](https://en.wikipedia.org/wiki/Bastion_host) by local forwarding them.

#### Evil use cases/ideas (not recommended)
 * [Melt Evil Corp's tape backups][mrrobot] by remotely controlling a Raspberry Pi.
 * Open a persistent SSH access backdoor to any network and bypass firewalls.
 * Run on-demand MITM attacks and compromising any network using a Plug&Play Raspberry Pi.

## Getting started

### Prerequisites
  * SSH Server: acting as a "proxy" SSH server with a static IP or DDNS domain accessible from internet.
  * Bastion host: any linux device/VM - hardware: Raspberry Pi is preferred.

### Installation

  1. Configure the parameters in config.py

```
## PARAMETERS -- EDIT BEFORE USE ##
controller_ip="suncoastsewing.ddns.net"
server_user="administrator"
pi_user="ubuntu"
conn_check="cloudflare.com" # Used by the RPi to periodically check DNS and Internet connectivity. Use any reliable/fast-resolvable domain name.
hport=22000 # The first port in the series to be used as a seed (hport stands for "host port")
```
  2. Run:
```
$ ./nbn-pi.sh [raspberry_ip]
```

## Recommendations

Section coming soon!

## Alternatives

NBN-Pi is intended as a highly reliable solution to tunneling ports with minimal dependencies, but there are some alternatives with more features.

### Tor hidden service

Tor provides anonymity to servers run as [hidden services][hidden-service], but also handles NAT traversal.

Advantages:

 * Metadata, including the IP address of the local device and its connection state (on/off), is less exposed to an intermediary like the reverse SSH proxy.

Disadvantages:

 * Tor must be installed and running on both the local device and clients.
 * Tor has higher latency so terminal feedback (input echo) is slow.

On both the device and clients, install Tor.

    sudo apt install tor

On the device that is being exposed, edit [`/etc/tor/torrc`][torrc] to create a hidden service on port 22.

    HiddenServiceDir /var/lib/tor/sshd/
    HiddenServicePort 22 127.0.0.1:22
    HiddenServiceAuthorizeClient stealth client

Replace "client" with a comma-separated list of client names to generate multiple authorization secrets.

Then reload Tor and get the onion hostname and authorization data.

    sudo service tor reload
    sudo cat /var/lib/tor/sshd/hostname

On clients, edit [`/etc/tor/torrc`][torrc] to add the onion hostname and authorization data seen in the `hostname` file.

    HidServAuth <hostname>.onion <secret>

Then reload Tor and run `torsocks ssh <hostname>.onion` or set `ProxyCommand` in the `~/.ssh/config` file.

    ProxyCommand torsocks nc <hostname>.onion 22

### autossh

[autossh](http://www.harding.motd.ca/autossh/), like NBN-Pi, starts `ssh` and restarts it as needed.

Some differences include:

 * NBN-Pi enables SSH keepalives
   (`ServerAliveInterval` and `ServerAliveCountMax`),
   which are available in modern versions of OpenSSH.
   autossh monitors `ssh` by sending data through
   a loop of port forwards (this feature predates SSH keepalives),
   though this can be disabled with the `-M 0` option.

 * NBN-Pi is intended to run automatically as a set of services,
   so the package includes init/systemd scripts and config files.
   autossh does not include an init/systemd script
   (Debian bug [#698390](https://bugs.debian.org/698390)).

 * NBN-Pi always retries if `ssh` exits with a non-zero exit status and include 2 resilience enforcement mechanisms.
   autossh does not retry if `ssh` exits too quickly on the first attempt,
   which can happen when network connectivity or DNS resolution
   is broken, particularly on mobile devices.
   Both sidedoor and autossh have retry backoff logic.

 * NBN-Pi resets retry backoff when a network interface is brought up,
   to attempt to reconnect as soon as possible, by receiving SIGUSR1
   from an `if-up.d` script. autossh does not have network state hooks.

### Other alternatives

 * [OpenVPN](https://en.wikipedia.org/wiki/OpenVPN)
 * [PageKite](https://github.com/pagekite/PyPagekite/)
 * [ssh_tunnel](http://sshtunnel.sourceforge.net/)


## Contributing

**Are you using NBN-Pi?**

Please open an issue!
Bugs reports, feature requests.
Pull requests are highly welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT License

Copyright (c) 2021 Nassim Bentarka

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Copyright 2015-2017 Dara Adib for [Sidedoor](https://github.com/daradib/sidedoor) licensed under GPL-3.0.

[mrrobot]: https://www.forbes.com/sites/abigailtracy/2015/07/15/hacking-the-hacks-mr-robot-episode-four-sam-esmail/
[edgeos]: https://help.ubnt.com/hc/en-us/articles/205202560-EdgeMAX-Add-other-Debian-packages-to-EdgeOS
[portforwarding]: https://blog.trackets.com/2014/05/17/ssh-tunnel-local-and-remote-port-forwarding-explained-with-examples.html
[hidden-service]: https://www.torproject.org/docs/tor-hidden-service.html.en
[torrc]: https://www.torproject.org/docs/tor-manual.html.en
