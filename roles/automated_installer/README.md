# Ansible Role: Automated Installer

This role installs Automated Installer as per Oracle's [documentation](https://docs.oracle.com/en/operating-systems/solaris/oracle-solaris/11.4/auto-install/).

## Requirements

None.

## Role Variables

    automated_installer_dhcp_subnets: []

The list of subnets that Automated Installer clients will boot from. Supports the following parameters:

| Parameter             | Type    | Required | Description                                                   |
| :---                  | :---    | :---     | :---                                                          |
| `subnet`              | String  | **Yes**  | The DHCP subnet to create (e.g. 10.1.1.0).                    |
| `netmask`             | String  | **Yes**  | The netmask to assign to the subnet (e.g. 255.255.255.0).     |
| `router`              | String  | **Yes**  | The router the subnet will use (e.g. 10.1.1.1).               |
| `broadcast_address`   | String  | **Yes**  | The broadcast address the subnet will use (e.g. 10.1.1.255).  |
| `domain_name_servers` | List    | **Yes**  | The DNS servers the subnet will use.                          |
| `domain_name`         | String  | **Yes**  | The domain name the subnet will use.                          |
| `domain_search`       | List    | **Yes**  | The search domains the subnet will use.                       |

    automated_installer_services: []

The list of Automated Installer services to create. Supports the following parameters:

| Parameter  | Type    | Required | Description                                                                   |
| :---       | :---    | :---     | :---                                                                          |
| `name`     | String  | **Yes**  | The name of the Automated Installer service.                                  |
| `iso_file` | String  | **Yes**  | The name of the Automated Installer ISO file to copy and use for the service. |
| `uar_file` | String  | No       | The name of the UAR file to copy and use for the service.                     |
| `manifest` | String  | **Yes**  | The name of the manifest to copy and use for the service.                     |
| `profile`  | String  | **Yes**  | The name of the profile to copy and use for the service.                      |

Make sure to store the `iso_file`, `uar_file`,  `manifest`, and `profile` files inside the `files/` directory adjacent
to your playbook.

    automated_installer_clients: []

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
