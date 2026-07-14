# Ansible Role: LDM

This role configures Logical Domains Manager/Oracle VM Server for SPARC as per Oracle's
[documentation](https://docs.oracle.com/en/virtualization/oracle-vm-server-sparc/ldoms-admin/).

## Requirements

None.

## Role Variables

    ldm_primary_cores: 2

The amount of CPU cores to set for the primary/control domain. Defaults to `2`.

    ldm_primary_mem: 16

The amount of RAM (in gigabytes) to set for the primary/control domain. Defaults to `16`.

> [!NOTE]
> Changes are done in delayed reconfiguration mode. It is your reponsibility to power-cycle the machine after
> changes are made.

    ldm_spconfig_name: "base-config"

The name to assign to the SP profile after CPU cores and RAM have been assigned. Defaults to `base-config`.

    ldm_vcc_name: "primary-vcc0"

The name of the default Virtual Console Concentrator service that LDOMs will use. Defaults to `primary-vcc0`.

    ldm_vds_name: "primary-vds0"

The name of the default Virtual Disk Server service that LDOMs will use. Defaults to `primary-vds0`.

    ldm_vsw_name: "primary-vsw0"

The name of the default Virtual Switch service that LDOMs will use. Defaults to `primary-vsw0`.

    ldm_vsw_lan: "net0"

The interface to bind the Virtual Switch service to. Defaults to `net0`.

    ldm_guests: []

The list of guests to be created. Supports the following parameters:

## Dependencies

None.

## Example Playbook

    - hosts: all
      become: true
      roles:
        - iambryant.solaris.ldm

## License

MIT
