# Ansible Role: Firewall

This role configures the Packet Filter firewall as per Oracle's
[documentation](https://docs.oracle.com/cd/E37838_01/html/E60993/pftask-conf.html).

## Requirements

None.

## Role Variables

    firewall_conf_name: base.conf

The name of the drop-in firewall config that PF will use. Defaults to `base.conf`.

    firewall_rules:  []

The list of rules to add to the drop-in firewall config. Supports the following parameters:

| Parameter   | Type     | Required | Description                                                         |
| :---        | :---     | :---     | :---                                                                |
| `action`    | String   | **Yes**  | The action to take for the rule.                                    |
| `family`    | String   | No       | The address family to use for the rule (e.g. `inet`, `inet6`).      |
| `proto`     | String   | No       | The protocol to use for the rule (e.g. `tcp`, `udp`).               |
| `from_ip`   | String   | No       | The source IP/subnet to allow for the rule.                         |
| `from_port` | String   | No       | The source port to allow for the rule.                              |
| `to_ip`     | String   | No       | The destination IP/subnet to allow for the rule.                    |
| `to_port`   | String   | No       | The destination port to allow for the rule.                         |
| `options`   | String   | No       | Options to add to the end of the rule (e.g. icmp-type, icmp6-type). |
| `comment`   | String   | No       | A short description of what the rule does.                          |

    firewall_rules_raw: ""

Custom rules to write that aren't supported by the role. Must be written in PF syntax.

## Dependencies

None.

## Example Playbook

    - hosts: all
      become: true
      roles:
        - iambryant.solaris.firewall

## TODO

Fix issue where defining `block in all` instead of just `block in` breaks the template since
`from any to any` is appended when `from_ip`/`to_ip` aren't defined.

## License

MIT
