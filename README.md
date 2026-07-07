# Ansible Collection: Solaris

[![CI](https://github.com/iambryant/ansible-collection-solaris/actions/workflows/ci.yml/badge.svg)](https://github.com/iambryant/ansible-collection-solaris/actions/workflows/ci.yml)

This collection includes roles for automating common tasks in Solaris.

## Installation

You can include this collection in your `requirements.yml` like this:

```
collections:
  - name: iambryant.solaris
    source: https://github.com/iambryant/ansible-collection-solaris
    type: git
```

## Requirements

None.

## Included Roles

  - `iambryant.solaris.ntp` ([documentation](https://github.com/iambryant/ansible-collection-solaris/blob/main/roles/ntp/README.md))
  - `iambryant.solaris.automated_installer` ([documentation](https://github.com/iambryant/ansible-collection-solaris/blob/main/roles/automated_installer/README.md))
  - `iambryant.solaris.firewall` ([documentation](https://github.com/iambryant/ansible-collection-solaris/blob/main/roles/firewall/README.md))
## Usage

To see an example of this collection's usage, see: https://github.com/iambryant/solaris-dev-playbook.

## License

MIT
