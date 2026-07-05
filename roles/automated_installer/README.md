# Ansible Role: Automated Installer

This role installs Automated Installer as per Oracle's [documentation](https://docs.oracle.com/en/operating-systems/solaris/oracle-solaris/11.4/auto-install/).

## Requirements

None.

## Role Variables

    ai_dhcp_dns_servers: []

The list of DNS servers that Automated Installer clients will use.

    ai_dhcp_domain_search: ""

The search domain that Automated Installer clients will use.

    ai_dhcp_subnets: []

The list of subnets that Automated Installer clients will boot from. Supports the following parameters:

| Parameter   | Type    | Required | Description                                                   |
| :---        | :---    | :---     | :---                                                          |
| `subnet`    | String  | **Yes**  | The DHCP subnet to create (e.g. 10.1.1.0).                    |
| `netmask`   | String  | **Yes**  | The netmask to assign to the subnet (e.g. 255.255.255.0).     |
| `broadcast` | String  | **Yes**  | The broadcast address the subnet will use (e.g. 10.1.1.255).  |
| `router`    | String  | **Yes**  | The router the subnet will use (e.g. 10.1.1.1).               |

    ai_services: []

The list of Automated Installer services to create. Supports the following parameters:

| Parameter  | Type    | Required | Description                                                                   |
| :---       | :---    | :---     | :---                                                                          |
| `name`     | String  | **Yes**  | The name of the Automated Installer service.                                  |
| `file`     | String  | **Yes**  | The name of the Automated Installer ISO file to copy and use for the service. |
| `manifest` | String  | **Yes**  | The name of the manifest to copy and use for the service.                     |
| `profile`  | String  | **Yes**  | The name of the profile to copy and use for the service.                      |

Make sure to store the `file`, `manifest`, and `profile` files inside the `files/` directory adjacent to your playbook.

    ai_clients: []

The list of Automated Installer clients to add. Supports the following parameters:

| Parameter | Type    | Required | Description                                                          |
| :---      | :---    | :---     | :---                                                                 |
| `name`    | String  | **Yes**  | The name of the Automated Installer client.                          |
| `mac`     | String  | **Yes**  | The mac address of the client.                                       |
| `ip`      | String  | **Yes**  | The IP address to assign to the client.                              |
| `service` | String  | **Yes**  | The name of the Automated Installer service to assign the client to. |

# Dependencies

None.

## Example Playbook

    - hosts: all
      become: true
      roles:
        - iambryant.solaris.automated_installer

## License

MIT
