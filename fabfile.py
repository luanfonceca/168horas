from fabric.api import env, local, run, require, cd
from fabric.contrib.files import exists
from fabric.operations import _prefix_commands, _prefix_env_vars

from datetime import datetime


env.disable_known_hosts = True  # always fails for me without this
env.hosts = ['168h.com.br']
env.user = 'root'
env.use_ssh_config = True
env.root = '/home'
env.virtualenv = 'virtualenv'
env.project_name = '168horas'
env.project_path = env.root + '/' + env.project_name
env.virtualenv_path = env.root + '/' + env.virtualenv
env.proj_repo = 'git@github.com:luanfonceca/168horas.git'
env.pip_file = env.project_path + '/requirements.txt'
env.nginx_file = env.project_path + '/nginx'
env.uwsgi_file = env.project_path + '/uwsgi'


def install():
    """Install a setup a server for the 168horas"""
    require('root')
    install_prereqs()

    if not exists(env.virtualenv_path):
        create_virtualenv()

    if not exists(env.project_path):
        clone()

    nginx_config()
    uwsgi_config()

    deploy()


def create_virtualenv():
    with cd(env.root):
        run('virtualenv %s' % env.virtualenv)


def install_prereqs():
    run('apt-get install {} -y'.format(' '.join([
        'python',
        'python-pip',
        'python-virtualenv',
        'nginx',
        'uwsgi',
        'supervisor',
    ])))


def nginx_config():
    default_config = '/etc/nginx/sites-enabled/default'
    if exists(default_config):
        run('rm {}'.format(default_config))

    run('touch /etc/nginx/sites-available/{}'.format(env.project_name))

    linked_file = '/etc/nginx/sites-available/{0}'.format(env.project_name)
    if not exists(linked_file):
        run('ln -s {0} /etc/nginx/sites-enabled/{1}'.format(
            linked_file, env.project_name))
    run('cp {0} /etc/nginx/sites-enabled/{1}'.format(
        env.nginx_file, env.project_name))

    nginx_restart()


def nginx_restart():
    run('/etc/init.d/nginx restart')


def uwsgi_config():
    uwsgi_path = '/etc/init/uwsgi.conf'
    if not exists(uwsgi_path):
        run('cp {0} {1}'.format(env.uwsgi_file, uwsgi_path))

    uwsgi_restart()


def uwsgi_restart():
    run('ps ax | grep uwsgi')

    run('pkill -9 uwsgi')

    with cd(env.project_path):
        run('uwsgi conf/uwsgi.ini')


def deploy(migrate=True, static=True, messages=True):
    """Update source, update pip requirements, syncdb, restart server"""

    backup_db()

    update()
    update_reqs()

    with cd(env.project_path):
        manage('clean_pyc')
        manage('migrate --noinput')
        manage('collectstatic --noinput --verbosity=0')
        manage('compilemessages')

    uwsgi_restart()


def switch(branch):
    """Switch the repo branch which the server is using"""
    with cd(env.project_path):
        ve_run('git checkout %s' % branch)
    restart()


def version():
    """Show last commit to repo on server"""
    with cd(env.project_path):
        sshagent_run('git log -1')


def restart():
    """Restart Apache process"""
    nginx_restart()
    uwsgi_restart()


def update_reqs():
    """Update pip requirements"""
    ve_run('yes w | pip install -r %s' % env.pip_file)


def update():
    """Updates project source"""
    with cd(env.project_path):
        sshagent_run('git pull')


def migrate():
    """Run syncdb (along with any pending south migrations)"""
    ve_run('python manage.py migrate --noinput')


def clean_pyc():
    """Run syncdb (along with any pending south migrations)"""
    ve_run('python manage.py clean_pyc')


def manage(cmd):
    ve_run('python manage.py {}'.format(cmd))


def clone():
    """Clone the repository for the first time"""
    with cd('%s' % env.root):
        sshagent_run('git clone %s' % env.proj_repo)


def ve_run(cmd):
    """
    Helper function.
    Runs a command using the virtualenv environment
    """
    require('root')
    sshagent_run('source %s/bin/activate' % (env.virtualenv_path))
    with cd(env.project_path):
        run(cmd)


def backup_db():
    now = datetime.now()
    ve_run('python manage.py dumpdata > /tmp/168horas-%s-backup.dump' % (
        now.strftime("%Y-%m-%d_%H:%M:%S")))


def sshagent_run(cmd):
    """
    Helper function.
    Runs a command with SSH agent forwarding enabled.

    Note:: Fabric (and paramiko) can't forward your SSH agent.
    This helper uses your system's ssh to do so.
    """
    # Handle context manager modifications
    wrapped_cmd = _prefix_commands(_prefix_env_vars(cmd), 'remote')
    try:
        host, port = env.host_string.split(':')
        return local(
            "ssh -p %s -A %s@%s '%s'" % (port, env.user, host, wrapped_cmd)
        )
    except ValueError:
        return local(
            "ssh -A %s@%s '%s'" % (env.user, env.host_string, wrapped_cmd)
        )
