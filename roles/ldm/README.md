# Ansible Role: LDM

This role configures LDM/Oracle VM Server for SPARC as per Oracle's
[documentation](https://docs.oracle.com/en/virtualization/oracle-vm-server-sparc/ldoms-admin/).

## Requirements

None.

## Role Variables

    ldm_primary_cores: 2

The amount of CPU cores to set for the primary/control domain. Defaults to `2`.

    ldm_primary_mem: 16

The amount of RAM (in gigabytes) to set for the primary/control domain. Defaults to `16`.

> [!NOTE]
> Changes are done in delayed reconfiguration mode. It is your reponsibility to reboot the machine after
> changes are made.

    ldm_spconfig_name: "base-config"

The name to assign to the SP profile after CPU cores and RAM have been assigned. Defaults to `base-config`.

## Dependencies

None.

## Example Playbook

    - hosts: all
      become: true
      roles:
        - iambryant.solaris.ldm

## License

MIT
