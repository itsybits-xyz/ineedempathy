import digitalocean
import os
import time
import paramiko
import paramiko.client

token = os.getenv('DIGITAL_OCEAN_KEY')

def create_droplet():
    manager = digitalocean.Manager(token=token)
    # inventory
    size_slug = None
    region_slug = None
    my_droplets = manager.get_all_droplets()
    for droplet in my_droplets:
        size_slug = droplet.size['slug']
        region_slug = droplet.region['slug']
        print(droplet.name, droplet.status, droplet.ip_address)
    # create
    keys = manager.get_all_sshkeys()
    droplet = digitalocean.Droplet(token=token,
        name='pr.1',
        region=region_slug,
        image='ubuntu-20-04-x64',
        size_slug=size_slug,
        ssh_keys=keys,
        private_networking='',
        backups=False)
    droplet.create()
    setup_complete = False
    # wait for ip
    while not setup_complete:
        actions = droplet.get_actions()
        setup_complete = all([action.status.lower() == 'completed' for action in actions])
        print('Waiting for ip address...')
        time.sleep(5);
    droplet.load()
    # wait for ssh
    stdout = ""
    while len(stdout) == 0:
        print('Waiting to ssh...')
        time.sleep(5)
        try:
            client = paramiko.client.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            private_key = paramiko.Ed25519Key.from_private_key_file("/home/runner/.ssh/id_ed25519")
            client.connect(droplet.ip_address, username="root", pkey=private_key)
            stdin, stdout, stderr = client.exec_command('ps aux')
            stdout = stdout.readlines()[0]
        except Exception as e:
            print(e)
    print(stdout)
    return droplet.ip_address

ip_address = create_droplet()
print(f"::set-output name=pull_request_host::{ip_address}")
app_servers = [ip_address]
