# Ansible Role: Firewall

This role configures the Packet Filter firewall as per Oracle's
[documentation](https://docs.oracle.com/cd/E37838_01/html/E60993/pftask-conf.html).

## Requirements

None.

## Role Variables

    firewall_conf_name: base.conf

The name of the drop-in firewall config that PF will use. Defaults to `base.conf`.

## Dependencies

None.

## Example Playbook

    - hosts: all
      become: true
      roles:
        - iambryant.solaris.firewall

## License

MIT
