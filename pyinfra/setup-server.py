from pyinfra.operations import apt, server, files, init
from pyinfra import host
from pyinfra.facts.files import File
from pyinfra.api import FactBase
import time

base_apt_packages = [
    "curl",
    "fish",
    "nginx",
    "software-properties-common",
    "sudo",
    "supervisor",
    "vim",
]

python_apt_packages = ["python3.9", "python3.9-distutils", "python3.9-venv"]

files.put(
    name="Copy wait-apt-get",
    src="templates/wait-apt-get",
    dest=f"/bin/apt-get",
    user="root",
    group="root",
    mode=600,
)

# Install openssh only if running inside docker.
if host.get_fact(File, path='/.dockerenv'):
    base_apt_packages.append('openssh-server')

class HasAptRunning(FactBase):
    def command(self, key):
        self.key = key # sorry
        return 'ps aux'

    def process(self, output):
        pos = ''.join(output).find(self.key)
        if pos == -1:
            print(pos, output);
        else:
            print(pos);
        return pos != -1

while host.get_fact(HasAptRunning, key='apt'):
    time.sleep(5);
    pass

while host.get_fact(HasAptRunning, key='snap wait'):
    time.sleep(5);
    pass


apt.update()
apt.packages(packages=base_apt_packages, present=True)

ppa_added = apt.ppa(name="Add python ppa.", src="ppa:deadsnakes/ppa")

if ppa_added.changed:
    apt.packages(packages=python_apt_packages, present=True)

server.group(name="Web team group", group="webteam")

server.user(name="Create user amjith", user="amjith", shell="/usr/bin/fish", groups=["sudo", "webteam"])

server.user(name="Create user baylee", user="baylee", groups=["sudo", "webteam"])

server.user(name="Create user web-runner", user="web-runner", shell="/usr/bin/false", groups=["webteam"])

files.line(
    name="Ensure amjith can run sudo without password",
    path="/etc/sudoers",
    line=r"amjith .*",
    replace="amjith ALL=(ALL) NOPASSWD: ALL",
)

files.line(
    name="Ensure baylee can run sudo without password",
    path="/etc/sudoers",
    line=r"baylee .*",
    replace="baylee ALL=(ALL) NOPASSWD: ALL",
)

server.shell(name="Check that sudoers file is ok", commands="visudo -c")

files.line(
    name="Disable password login",
    path="/etc/ssh/sshd_config",
    line=r"^[#\s]*PasswordAuthentication .*$",
    replace="PasswordAuthentication no",
)

"""
files.line(
    name="Disable password login",
    path="/etc/ssh/sshd_config",
    line=r"^[#\s]*ChallengeResponseAuthentication .*$",
    replace="ChallengeResponseAuthentication no",
)

files.line(
    name="Disable password login",
    path="/etc/ssh/sshd_config",
    line=r"^[#\s]*UsePAM .*$",
    replace="UsePAM yes",
)
"""

files.line(
    name="Enable pubkey login",
    path="/etc/ssh/sshd_config",
    line=r"^[#\s]*PubkeyAuthentication .*$",
    replace="PubkeyAuthentication yes",
)

files.line(
    name="Disable root login",
    path="/etc/ssh/sshd_config",
    line=r"^[#\s]*PermitRootLogin .*$",
    replace="PermitRootLogin no",
)

files.template(
    name="Create app specific nginx config file.",
    src="templates/nginx_app.conf",
    dest=f"/etc/nginx/sites-available/{host.data.app_name}",
    hostname=host.data.hostname,
    app_static_file_location=host.data.static_folder,
)

files.put(
    name="Create authorized_keys for amjith",
    src="templates/amjith_authorized_keys",
    dest=f"/home/amjith/.ssh/authorized_keys",
    user="amjith",
    group="amjith",
    mode=600,
)

files.put(
    name="Create authorized_keys for baylee",
    src="templates/baylee_authorized_keys",
    dest=f"/home/baylee/.ssh/authorized_keys",
    user="baylee",
    group="baylee",
    mode=600,
)

init.systemd(
    name='Restart and enable sshd',
    service='sshd',
    running=True,
    restarted=True,
    enabled=True,
    daemon_reload=True,
)

files.directory(
    name='Ensure application directory exists.',
    path=f'/var/www/{host.data.app_name}',
    user="web-runner",
    group="webteam",
    mode="775",
)

files.directory(
    name='Ensure nginx config directory for app exists.',
    path=f'/etc/nginx/sites-available',
)

files.template(
    name="Create app specific nginx config file.",
    src="templates/nginx_app.conf",
    dest=f"/etc/nginx/sites-available/{host.data.app_name}",
    hostname=host.data.hostname,
    app_static_file_location=host.data.static_folder,
)

files.link(
    name="Create a symlink from sites-available to sites-enabled.",
    target=f"/etc/nginx/sites-available/{host.data.app_name}",
    path=f"/etc/nginx/sites-enabled/{host.data.app_name}",
)

files.template(
    name="Create supervisord config file.",
    src="templates/supervisord.conf",
    dest="/etc/supervisor/supervisord.conf",
    app_name=host.data.app_name,
)

