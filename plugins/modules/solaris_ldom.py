#!/usr/bin/python

# Copyright (c) 2026, iambryant
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
# SPDX-License-Identifier: MIT

from __future__ import annotations

DOCUMENTATION = r"""
module: solaris_ldom
short_description: Manage Solaris LDOMs (Logical Domains)
description:
  - Create, start, stop, and destroy Solaris LDOMs.
  This module does not currently allow changing of options for a LDOM that is already been created.
author:
  - Your Name (@iambryant)
requirements:
  - Solaris 10 or 11 on SPARC
attributes:
  check_mode:
    support: full
  diff_mode:
    support: none
options:
  name:
    description:
      - The name of the Logical Domain.
    type: str
    required: true
  state:
    description:
      - V(present): Configure the LDOM, set CPU/Memory, and bind resources.
      - V(running): Ensure the LDOM is created, bound, and started.
      - V(stopped): Stop/halt a running LDOM.
      - V(absent): Stop, unbind, and destroy the LDOM.
    type: str
    choices: [absent, present, running, stopped]
    default: present
  vcpu:
    description:
      - Number of virtual CPUs to assign to the LDOM.
    type: int
    default: 8
  memory:
    description:
      - Memory allocation for the LDOM (e.g., "4G", "16G").
    type: str
    default: "4G"
"""

EXAMPLES = r"""
- name: Ensure LDOM exists and is configured
  solaris_ldom:
    name: ldom-web1
    state: present
    vcpu: 16
    memory: 8G

- name: Start an LDOM
  solaris_ldom:
    name: ldom-web1
    state: running

- name: Stop an LDOM
  solaris_ldom:
    name: ldom-web1
    state: stopped

- name: Destroy an LDOM entirely
  solaris_ldom:
    name: ldom-web1
    state: absent
"""

import os
import platform
import re
from ansible.module_utils.basic import AnsibleModule


class Ldom:
    def __init__(self, module):
        self.module = module
        self.changed = False
        self.msg = []

        self.name = self.module.params["name"]
        self.state = self.module.params["state"]
        self.vcpu = self.module.params["vcpu"]
        self.memory = self.module.params["memory"]

        # Find the path to the ldm binary
        self.ldm_cmd = self.module.get_bin_path("ldm", True)

        # Validate OS
        if platform.system() != "SunOS":
            self.module.fail_json(msg="This module requires Solaris (SunOS).")

        if self.module.check_mode:
            self.msg.append("Running in check mode")

    def run_ldm_cmd(self, args, error_msg):
        """Helper to run ldm commands safely."""
        cmd = [self.ldm_cmd] + args
        rc, out, err = self.module.run_command(cmd)
        if rc != 0:
            self.module.fail_json(msg=f"{error_msg}. Command: {' '.join(cmd)}. Error: {out + err}")
        return out

    def get_info(self):
        """
        Runs 'ldm list -p <name>' and parses out state/config details.
        Returns a dict of info, or None if the LDOM doesn't exist.
        """
        cmd = [self.ldm_cmd, "list", "-p", self.name]
        rc, out, err = self.module.run_command(cmd)

        if rc != 0:
            return None  # LDOM does not exist

        info = {}
        # Parse parseable output format: "DOMAIN|name=ldom1|state=active|flags=-n---..."
        for line in out.splitlines():
            if line.startswith("DOMAIN|"):
                fields = line.split("|")
                for field in fields:
                    if "=" in field:
                        key, val = field.split("=", 1)
                        info[key] = val
            elif line.startswith("VCPU|"):
                # Track current vcpu count if needed
                fields = line.split("|")
                for field in fields:
                    if field.startswith("count="):
                        info["vcpu"] = int(field.split("=")[1])
            elif line.startswith("MEMORY|"):
                # Track current memory if needed
                fields = line.split("|")
                for field in fields:
                    if field.startswith("size="):
                        info["memory"] = field.split("=")[1]
        return info

    def create(self):
        """Creates the LDOM and configures resources."""
        if not self.module.check_mode:
            # 1. Add domain
            self.run_ldm_cmd(["add-domain", self.name], "Failed to add domain")
            # 2. Add vcpus
            self.run_ldm_cmd(["add-vcpu", str(self.vcpu), self.name], "Failed to add vcpus")
            # 3. Add memory
            self.run_ldm_cmd(["add-memory", self.memory, self.name], "Failed to add memory")
            # --- MODIFICATION AREA ---
            # This is where you would add your default network (vnet) and virtual disk (vdisk) configurations.
            # Example:
            # self.run_ldm_cmd(["add-vnet", "vnet1", "primary-vsw0", self.name], "Failed to add vnet")
            # -------------------------

        self.changed = True
        self.msg.append(f"LDOM {self.name} created")

    def bind(self):
        """Binds resources to the domain."""
        if not self.module.check_mode:
            self.run_ldm_cmd(["bind", self.name], "Failed to bind LDOM")
        self.changed = True
        self.msg.append(f"LDOM {self.name} bound")

    def start(self):
        """Starts the domain."""
        if not self.module.check_mode:
            self.run_ldm_cmd(["start", self.name], "Failed to start LDOM")
        self.changed = True
        self.msg.append(f"LDOM {self.name} started")

    def stop(self):
        """Gracefully stops the domain."""
        if not self.module.check_mode:
            self.run_ldm_cmd(["stop", self.name], "Failed to stop LDOM")
        self.changed = True
        self.msg.append(f"LDOM {self.name} stopped")

    def unbind(self):
        """Unbinds the resources of the domain."""
        if not self.module.check_mode:
            self.run_ldm_cmd(["unbind", self.name], "Failed to unbind LDOM")
        self.changed = True
        self.msg.append(f"LDOM {self.name} unbound")

    def destroy(self):
        """Destroys the domain."""
        if not self.module.check_mode:
            self.run_ldm_cmd(["destroy-domain", self.name], "Failed to destroy LDOM")
        self.changed = True
        self.msg.append(f"LDOM {self.name} destroyed")

    # State machine logic
    def enforce_state(self):
        info = self.get_info()

        if self.state == "absent":
            if not info:
                self.msg.append("LDOM already absent")
                return

            # If it's active (running), we must stop it first
            if info.get("state") == "active":
                self.stop()

            # If it's bound, we must unbind it
            info = self.get_info()  # Refresh status
            if info and info.get("state") == "bound":
                self.unbind()

            # Now we can destroy
            self.destroy()

        elif self.state in ["present", "running", "stopped"]:
            if not info:
                self.create()
                info = self.get_info()  # Re-query after creation

            current_status = info.get("state") if info else "inactive"

            if self.state == "present":
                # We want it to exist and be bound (but not necessarily running)
                if current_status == "inactive":
                    self.bind()
                elif current_status == "active":
                    self.msg.append("LDOM already present (and running)")
                else:
                    self.msg.append("LDOM already present and bound")

            elif self.state == "running":
                if current_status == "inactive":
                    self.bind()
                    self.start()
                elif current_status == "bound":
                    self.start()
                elif current_status == "active":
                    self.msg.append("LDOM already running")

            elif self.state == "stopped":
                if current_status == "active":
                    self.stop()
                elif current_status in ["inactive", "bound"]:
                    self.msg.append("LDOM already stopped")


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="str", required=True),
            state=dict(
                type="str",
                default="present",
                choices=["absent", "present", "running", "stopped"],
            ),
            vcpu=dict(type="int", default=8),
            memory=dict(type="str", default="4G"),
        ),
        supports_check_mode=True,
    )

    ldom = Ldom(module)
    ldom.enforce_state()

    module.exit_json(changed=ldom.changed, msg=", ".join(ldom.msg))


if __name__ == "__main__":
    main()
