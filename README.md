# Ansible Role: Quagga

A brief description of the role goes here.

## Requirements

None

## Role Variables

Available variables are listed below, with their default values (see `defaults/main.yml`)

    quagga_ospfd_enabled: "False"

Only the zebdra daemon is eanbled by default within the role.  To enable ospfd set `quagga_osfpd_enabled` to `True`.

## Dependencies

None

## Example Playbook

    - hosts: ospf-routers
      roles:
         - { role: dselders.quagga }

## License

BSD

## Author Information

Created by [David Selders](https://github.com/dselders)
