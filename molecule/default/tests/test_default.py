import os

import testinfra.utils.ansible_runner
from pytest import fixture

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@fixture()
def AnsibleVars(host):
    return host.ansible.get_variables()


def test_quagga_is_installed(host):
    quagga = host.package("quagga")
    daemons = host.file("/etc/quagga/daemons")

    assert quagga.is_installed
    assert daemons.is_file


def test_zebra_is_enabled(host):
    daemons = host.file("/etc/quagga/daemons")

    assert daemons.is_file
    assert daemons.contains("^zebra=yes$")


def test_ospf_is_enabled(host):
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


def test_ospf_is_listening(host):
    ospf_socket = host.socket("tcp://127.0.0.1:2604")

    assert ospf_socket.is_listening


def test_ospf_router_id_is_set(host, AnsibleVars):
    router_id = host.run("vtysh -c 'sh run' | grep 'ospf router-id'")
    given_router_id = AnsibleVars['quagga_ospf']['router_id']

    assert router_id.stdout == " ospf router-id " + str(given_router_id)


def test_ospf_network_is_advertised(host, AnsibleVars):
    for item in AnsibleVars['quagga_ospf']['networks']:
        network_addr = item['prefix']
        area = str(item['area'])
        run_cmd = "vtysh -c 'sh run' | grep 'network " + network_addr + "'"
        network = host.run(run_cmd)

        assert network.stdout == " network " + network_addr + " area 0.0.0." +\
            area


def test_ospf_lo0_is_passive(host, AnsibleVars):
    for item in AnsibleVars['quagga_ospf']['interfaces']:
        if 'passive' in item.keys():
            intf = item['name']
            run_cmd = "vtysh -c 'sh run' | grep 'passive-interface " +\
                intf + "'"
            passive_intf = host.run(run_cmd)

            assert passive_intf.stdout == " passive-interface " + intf


def test_ospf_eth0_bw_is_set(host, AnsibleVars):
    for item in AnsibleVars['quagga_ospf']['interfaces']:
        if 'bandwidth' in item.keys():
            intf = item['name']
            bandwidth = str(item['bandwidth'])
            run_cmd = "vtysh -c 'sh int " + intf + "' | grep bandwidth"
            reported_bw = host.run(run_cmd)

            assert reported_bw.stdout == "  bandwidth " + bandwidth + " kbps"


def test_ospf_hello_timer_is_set(host, AnsibleVars):
    for item in AnsibleVars['quagga_ospf']['interfaces']:
        if 'hello_timer' in item.keys():
            intf = item['name']
            hello = str(item['hello_timer'])
            run_cmd = "vtysh -c 'sh ip ospf int " + intf + "' |\
                grep 'Timer intervals configured' | awk -F, '{print $2}'"
            reported_hello = host.run(run_cmd)

            assert reported_hello.stdout == " Hello " + hello + "s"


def test_ospf_dead_timer_is_set(host, AnsibleVars):
    for item in AnsibleVars['quagga_ospf']['interfaces']:
        if 'dead_timer' in item.keys():
            intf = item['name']
            dead = str(item['dead_timer'])
            run_cmd = "vtysh -c 'sh ip ospf int " + intf + "' |\
                grep 'Timer intervals configured' | awk -F, '{print $3}'"
            reported_dead = host.run(run_cmd)

            assert reported_dead.stdout == " Dead " + dead + "s"


def test_osfpd_default_information_originate_is_set(host):
    default_information = host.run("vtysh -c 'sh run' |\
            grep 'default-information originate'")

    assert default_information.stdout == ' default-information originate'
