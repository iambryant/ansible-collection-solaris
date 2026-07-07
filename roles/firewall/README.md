# Ansible Role: Firewall

This role configures the Packet Filter firewall as per Oracle's
[documentation](https://docs.oracle.com/cd/E37838_01/html/E60993/pftask-conf.html).

## Requirements

None.

## Role Variables

None.

## Dependencies

None.

## Example Playbook

    - hosts: all
      become: true
      roles:
        - iambryant.solaris.firewall

## License

MIT
