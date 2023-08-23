import pytest
from sshcheckers import ssh_checkout

folder_out = "/home/edan/tst/badarx"
folder_ext = "/home/edan/tst/ext"

host = "ubuntutest"
user = "edan"
passwd = "qwerty12345"
port = 22


def test_step_1():
    #Test 1
    cmd = "cd {}; 7z e badarx.7z -o{} -y".format(folder_out, folder_ext)
    text = "ERROR"
    assert ssh_checkout(host, user, passwd, cmd, text, port), "Test 1 failed"


def test_step2():
    # Test 2
    cmd = "cd {}; 7z t badarx.7z".format(folder_out)
    text = "ERROR"
    assert ssh_checkout(host, user, passwd, cmd, text, port), "Test 2 failed"


if __name__ == '__main__':
    pytest.main()