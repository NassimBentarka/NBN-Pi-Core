## NBN-Pi-Core

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

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/nassimosaz/NBN-Pi-Core/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
