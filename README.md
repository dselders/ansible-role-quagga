# Ansible Role: Quagga

[![Build Status](https://travis-ci.org/dselders/ansible-role-quagga.svg?branch=master)](https://travis-ci.org/dselders/ansible-role-quagga)

A brief description of the role goes here.

## Requirements

None

## Role Variables

Available variables are listed below, with their default values (see
`defaults/main.yml`)

```yaml
quagga_vtysh_password: zebra
quagga_zebra_log: /var/log/quagga/zebra.log
quagga_ospf_log: /var/log/quagga/ospfd.log
quagga_ospf_log_precision: 0
quagga_ospf_enabled: false
quagga_ospf_reference_bw: 100  # in megabits per second
```

Only the Zebra daemon is eanbled by default within the role.  To enable OSPF
set `quagga_osfp_enabled` to `True`.  The default logging locations can be
overriden.  The default precision for both Zebra and OSPF is set to the quagga
default.  The OSPF reference bandwidth is configured to the default of 100mbit.

```yaml
quagga_router_id: 192.168.29.1
```

The `quagga_router_id` is the router-id for the host when using either BGP or
OSPF.

```yaml
quagga_ospf:
  originate_default: true
  networks:
    - prefix: 192.168.29.0/24
      area: 0
  interfaces:
    - name: eth0
      passive: true
    - name: eth1
      bandwidth: 100000  # in kilobits per second
      hello_timer: 5
      dead_timer: 20
      auth:
        - key_id: 1
          md5_key: "Quagga_OSPF"
```

The `quagga_ospf` hash will contain the information needed configure OSPF on a
host.  Optionally OSPF can originate a default route.  When `originate_default`
is defined a default will be originated.  If you want a default even if there is
no default in the route table you may set `originate_default` to always.

The `networks` key contains a list of `prefix` and `area` that will be
advertised via OSPF.  The interfaces matching the given prefix will have OSPF
enabled on them.  OSPF will send out hello packets and form neighbor
relationships over these interfaces.

The `interfaces` key contains optional config items in a list.  The `name` is
required to set either `passive` or `cost`.  The `passive` key is not required
and is to allow the setting of an interface as passive.  The `bandwidth` key
allows for correcting interface bandwidth, in order to have an accurate OSPF
cost calculation.  This number is the interface bandwidth in kilobits per
second.  The hello timer can be changed via the `hello_timer`.  The time is
given in seconds, and the Quagga default is 10 seconds.  The dead timer can be
changed via the `dead_timer`.  The time is given in seconds, and the Quagga
default is 40 seconds.

Authorization contained witin `interfaces` allows for the use of MD5
authentication on interfaces.  The `key_id` allows for the use of multiple keys
to gracefully change the keys in a given network segment.

```yaml
quagga_bgp:
  asn: 65000
  networks:
    - 192.168.0.0/16
  neighbors:
    - peer: 10.10.10.10
      asn: 65001
      peer_group: ebgp-peers
    - peer: ebgp-peers
      ebgp_multihop: true
      is_peer_group: true
      next_hop_self: true
      description: "external peers"
      update_source: 1.1.1.1
```

## Dependencies

None

## Example Playbook

```yaml
- hosts: ospf-routers
  vars:
    quagga_ospf:
      router_id: 1.1.1.1
      networks:
        - prefix: 192.168.29.0/24
          area: 0
  roles:
    - { role: dselders.quagga }
```

## Testing

This role has been developed using
[molecule](https://molecule.readthedocs.io/en/latest/) to drive testing.  To run
the default scenario:

        molecule test

When this is run molecule will lint, syntax check, apply the role, check for
idempotence, and finally verify that all tests pass.  The tests can be found int
`molecule/default/tests`.  Molecule does allow for lint, syntax checking,
applying the role, and verifying individually as well.

## License

BSD

## Author Information

Created by [David Selders](https://github.com/dselders)
