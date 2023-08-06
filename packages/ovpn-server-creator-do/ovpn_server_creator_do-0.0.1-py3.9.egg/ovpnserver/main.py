import argparse
import datetime
import time
import digitalocean

from datetime import timedelta
from loguru import logger
from .utils import PATH_TO_SAVE_FILE, get_file, get_token

TAG_NAME = 'OpenVPNScriptCreated'
REMOTE_PATH_OVPN_FILE = '/root/client.ovpn'


def get_manager(token):
    return digitalocean.Manager(token=token)


def get_ssh_keys(token):
    return get_manager(token).get_all_sshkeys()


def get_exists_active_droplet(token, tag=TAG_NAME, delete_other=True):
    droplets = get_manager(token).get_all_droplets(tag_name=tag)
    if not droplets:
        logger.info('Exists droplet with tag name: {} not found'.format(tag))
        return None
    for i in droplets:
        if not datetime.datetime.now()-timedelta(days=90) <= datetime.datetime.strptime(i.created_at, '%Y-%m-%dT%H:%M:%SZ'):
            i.destroy()
    droplets = get_manager(token).get_all_droplets(tag_name=tag)

    if delete_other and len(droplets) > 1:
        logger.info('Found {} droplets with tag name: {}'.format(len(droplets), tag))
        logger.info('Deleting droplets... Save only one of them')
        [droplet.destroy() for droplet in droplets[1:]]
    logger.success('Find active droplet')
    return droplets[0]


def create_droplet(token, tags):
    droplet = digitalocean.Droplet(
        token=token,
        name='OpenVpn',
        region='tor1',
        image='pihole-18-04',
        size_slug='1gb',
        disk=25,
        backups=False,
        tags=tags,
        ssh_keys=get_ssh_keys(token),
    )
    droplet.create()
    logger.info('Droplet is creating...')
    while True:
        droplet = get_manager(token).get_droplet(droplet.id)
        if droplet.status == 'active':
            logger.success('Droplet created!')
            break
        time.sleep(20)
        logger.info('Wait to created droplet...')
    return droplet


def run(token, openvpn_file_path=PATH_TO_SAVE_FILE, tag=TAG_NAME):
    droplet = get_exists_active_droplet(token)
    if droplet is None:
        logger.success('Start!')
        droplet = create_droplet(token, tags=[tag])
        get_file(droplet.ip_address, REMOTE_PATH_OVPN_FILE, openvpn_file_path)
    else:
        get_file(droplet.ip_address, REMOTE_PATH_OVPN_FILE, PATH_TO_SAVE_FILE, sleep_wait_file=1)


def main():
    parser = argparse.ArgumentParser(description='OpenVPN creator')
    user_token = get_token()
    parser.add_argument('--token', type=str, nargs='+',
                        default=user_token,
                        help='token from Digital Ocean with permission create droplet')
    parser.add_argument('--tag', type=str, nargs='+',
                        help='Droplet tags')
    parser.add_argument('--local-path', type=str, nargs='+', default=PATH_TO_SAVE_FILE,
                        help='local path where file will save: /home/username/Documents/')

    args = parser.parse_args()
    if args.token is None:
        logger.error('Set token: --token <YOUR TOKEN>')
    else:
        run(args.token, args.local_path, args.tag)


if __name__ == '__main__':
    main()
