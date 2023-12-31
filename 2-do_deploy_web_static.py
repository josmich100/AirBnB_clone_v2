#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""
from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime
env.hosts = ['100.27.2.172', '100.25.158.175']
env.user = 'ubuntu'


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    try:
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        file_name = "versions/web_static_{}.tgz".format(current_time)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        path_no_ext = "/data/web_static/releases/{}/".format(no_ext)
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(path_no_ext))
        run("tar -xzf /tmp/{} -C {}".format(file_name, path_no_ext))
        run("rm /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(path_no_ext, path_no_ext))
        run("rm -rf {}web_static".format(path_no_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(path_no_ext))
        return True
    except Exception as e:
        return False
