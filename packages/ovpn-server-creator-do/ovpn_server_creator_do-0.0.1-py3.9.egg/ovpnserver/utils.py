import os
import time
from os.path import expanduser

from loguru import logger
from paramiko import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import NoValidConnectionsError
from scp import SCPClient, SCPException


def _get_home_dir():
    return expanduser("~")


def _path_to_save():
    return _get_home_dir() + '/vpns/'


def _ssh_connect(ssh, ip4, user):
    count_try = 0
    while True:
        if count_try > 5:
            logger.error('Long Unable to connect')
            raise Exception('Unable to connect')
        try:
            ssh.connect(hostname=ip4, username=user)
            return
        except NoValidConnectionsError:
            time.sleep(5)
            count_try += 1
            logger.info('Try again connect')


def _get_file(scp, remote_path, local_path, sleep_wait_file):
    time.sleep(sleep_wait_file)
    count_try = 0
    sleep_time = 20
    while True:
        if count_try > 30:
            logger.error('Long time spend to wait creating file!')
            raise Exception('Did not create file')
        try:
            logger.info('Wait to creating client.ovpn file...')
            scp.get(remote_path, local_path)
            return
        except SCPException:
            logger.info('Fail... Try again after {0} seconds'.format(sleep_time))
            time.sleep(sleep_time)


def get_file(ip4, remote_path, local_path, sleep_wait_file=300, user='root'):
    logger.info('SSH is connecting...')
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.load_system_host_keys()
    _ssh_connect(ssh, ip4, user)
    logger.success('SSH connected!')
    scp = SCPClient(ssh.get_transport())

    logger.info('Try get file... First time It takes ˜5 minutes')
    _get_file(scp, remote_path, local_path, sleep_wait_file=sleep_wait_file)
    logger.success('File got!')
    logger.success('File {} saved to: {}'.format(remote_path, local_path))


PATH_TO_SAVE_FILE = _path_to_save()


def get_token():
    token_file = _get_home_dir() + '/.do_token'
    if os.path.isfile(token_file):
        with open(token_file) as f:
            return f.read().strip()
