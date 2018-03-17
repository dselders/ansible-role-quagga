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
