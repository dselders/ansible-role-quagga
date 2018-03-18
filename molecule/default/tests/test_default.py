import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_quagga_is_installed(host):
    quagga = host.package("quagga")
    daemons = host.file("/etc/quagga/daemons")

    assert quagga.is_installed
    assert daemons.is_file


def test_zebra_is_enabled(host):
    daemons = host.file("/etc/quagga/daemons")

    assert daemons.is_file
    assert daemons.contains("^zebra=yes$")


def test_ospfd_is_enabled(host):
    daemons = host.file("/etc/quagga/daemons")

    assert daemons.is_file
    assert daemons.contains("^ospfd=yes$")


def test_quagga_is_running(host):
    quagga = host.service("quagga")

    assert quagga.is_running
    assert quagga.is_enabled


def test_zebra_is_listening(host):
    zebra_socket = host.socket("tcp://127.0.0.1:2601")

    assert zebra_socket.is_listening


def test_ospfd_is_listening(host):
    ospfd_socket = host.socket("tcp://127.0.0.1:2604")

    assert ospfd_socket.is_listening


def test_ospfd_router_id_is_set(host):
    router_id = host.run("vtysh -c 'sh run' | grep 'ospf router-id'")

    assert router_id.stdout == " ospf router-id 1.1.1.1"


def test_ospfd_network_is_advertised(host):
    network = host.run("vtysh -c 'sh run' | grep 'network 192.168.29.0'")

    assert network.stdout == " network 192.168.29.0/24 area 0.0.0.0"


def test_ospfd_lo0_is_passive(host):
    passive_intf = host.run("vtysh -c 'sh run' | grep 'passive-interface lo0'")

    assert passive_intf.stdout == " passive-interface lo0"


def test_ospfd_eth1_bw_is_set(host):
    eth1_bw = host.run("vtysh -c 'sh int eth1' | grep bandwidth")

    assert eth1_bw.stdout == "  bandwidth 1000000 kbps"


def test_ospfd_hello_timer_is_set(host):
    hello_timer = host.run("vtysh -c 'sh ip ospf int eth1' |\
            grep 'Timer intervals configured' | awk -F, '{print $2}'")

    assert hello_timer.stdout == " Hello 5s"
