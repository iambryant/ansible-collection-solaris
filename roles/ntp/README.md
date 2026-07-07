# Ansible Role: NTP

This role configures NTP as per Oracle's
[documentation](https://docs.oracle.com/cd/E37838_01/html/E61003/time-4.html#scrolltoc).

## Requirements

None.

## Role Variables

    ntp_servers:
      - pool 0.pool.ntp.org iburst
      - pool 1.pool.ntp.org iburst

The list of NTP servers and burst modes to use. Defaults to `0.pool.ntp.org` and `1.pool.ntp.org` with the burst mode
`iburst` set for both.

## Dependencies

None.

## Example Playbook

    - hosts: all
      become: true
      roles:
        - iambryant.solaris.ntp

## License

MIT
