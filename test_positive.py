import pytest
from sshcheckers import ssh_checkout, upload_file, getout
import yaml

with open('config.yml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)
folder_tst = data['folder_tst']
folder_out = data['folder_out']
FOLDER_folder1 = data['FOLDER_folder1']
FOLDER_folder2 = data['FOLDER_folder2']

def save_log(starttime, name):
    with open(name, 'w') as f:
        f.write(getout("journalctl --since '{}'".format(starttime)))

def test_step_1(start_time):
    res = []
    upload_file(data["ip"], data["user"], data["passwd"], 'p7zip-full.deb', '/home/user2/p7zip-full.deb')
    res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], 'echo "qwerty12345" | sudo -S dpkg -i /home/user2/p7zip-full.deb',
                     'Настраивается пакет'))
    res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], 'echo "qwerty12345" | sudo -S dpkg -s p7zip-full',
                            'Status: installed'))
    save_log(start_time, 'log_test_1')
    assert all(res), 'Test 1 failed'

def test_step_2(start_time, clear_dir, get_dir, make_file):
    #Test 2: Добавление файлов в архив (a)
    res1 = ssh_checkout(data["ip"], data["user"], data["passwd"], f"cd {folder_tst}; 7z a {folder_out}/arx2", "All is ok")
    res2 = ssh_checkout(data["ip"], data["user"], data["passwd"], f"ls {folder_out}", "arx2.7z")
    save_log(start_time, 'log_test2')
    assert res1 and res2, "Test 2 failed"

def test_step_3(start_time, clear_dir, get_dir, make_file):
    #Test 3: Извлечение файлов из архива (e)
    res = []
    res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],f"cd {folder_tst}; 7z a {folder_out}/arx2", "All is ok"))
    res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],f"cd {folder_out}; 7z e arx2.7z -o{FOLDER_folder1} -y", "All is ok"))
    for i in make_file:
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],f"ls {FOLDER_folder1}", i))
    save_log(start_time, 'log_test_3')
    assert all(res), "Test 3 failed"

def test_step_4(start_time):
    #Test 4: Проверка целостности архива (t)
    save_log(start_time, 'log_test_4')
    assert ssh_checkout(data["ip"], data["user"], data["passwd"],f"cd {folder_out}; 7z t arx2.7z", "All is ok"), "Test 4 failed"

def test_step_5(start_time):
    #Test 5: Удаление файлов из архива (d)
    save_log(start_time, 'log_test_5')
    assert ssh_checkout(data["ip"], data["user"], data["passwd"],f"cd {folder_out}; 7z d arx2.7z", "All is ok"), "Test 5 failed"

def test_step_6(start_time):
    #Test 6: Обновление файлов в архиве (u)
    save_log(start_time, 'log_test_6')
    assert ssh_checkout(data["ip"], data["user"], data["passwd"],f"cd {folder_out}; 7z u arx2.7z", "All is ok"), "Test 6 failed"

def test_step_7(start_time):
    #Test 7: Показать содержимое архива (l)
    res1 = ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z l arx2.7z".format(folder_out, FOLDER_folder1), "arx2.7z")
    res2 = ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z l arx2.7z".format(folder_out, FOLDER_folder2), "arx2.7z")
    save_log(start_time, 'log_test_7')
    assert res1 and res2, "Test 7 failed"

def test_step_8(start_time):
    #Test 8: Извлечь файлы с полными путями (x)
    res1 = ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z x arx2.7z -o{} -y".format(folder_out, FOLDER_folder2), "All is ok")
    res2 = ssh_checkout(data["ip"], data["user"], data["passwd"], f"ls {FOLDER_folder2}", "arx2.7z")
    save_log(start_time, 'log_test_8')
    assert res1 and res2, "Test 8 failed"


if __name__ == '__main__':
    pytest.main()