import os
import sys

import pytest

from testlib import clissh

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


@pytest.fixture()
def connection():
    cli = clissh.CLISSH(host='host', username="username", password="pass")
    cli.login()
    return cli


def get_ifconfig_value(inp, name):
    inp = inp.strip().split(' ')
    for i in range(len(inp)):
        if inp[i] == name:
            return inp[i + 1]


def test_file_and_folder(connection):
    dir_name = '~/created_folder'
    fileName = 'created_file'
    connection.exec_command(f'mkdir {dir_name}')
    assert connection.exec_command(f'ls | grep created_folder')[0], 'folder is not exist'
    connection.exec_command(f'echo "I love pytest" > {dir_name}/{fileName}')
    assert connection.exec_command(f'ls {dir_name}/{fileName} | grep {fileName}')[0], 'File is not exist'
    assert connection.exec_command(f'cat {dir_name}/{fileName}')[0].strip() == 'I love pytest', 'Such text not in file'


@pytest.mark.parametrize(
    'value, name, err_text',
    [('1500', 'mtu', 'Incorrect mtu value'),
     ('172.20.8.179', 'inet', 'Incorrect ip address'),
     ('fe80::c051:d3f3:52c8:837c', 'inet6', 'Incorrect ipv6 address')]
)
def test_ifconfig(connection, value, name, err_text):
    interface = 'enp2s0'
    found_str = connection.exec_command(f'ifconfig {interface} | grep {name}')[0]
    assert get_ifconfig_value(found_str, name) == value, err_text
