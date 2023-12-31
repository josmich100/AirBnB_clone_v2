#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers
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
    if exists(archive_path):
        archived_file = archive_path.split("/")[-1]
        filename_no_ext = splitext(archived_file)[0]
        new_version = "/data/web_static/releases/" + filename_no_ext
        arc_file_remote = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(new_version))
        run("sudo tar -xzf {} -C {}/".format(arc_file_remote, new_version))
        run("sudo rm {}".format(arc_file_remote))
        run("sudo mv {}/web_static/* {}".format(new_version, new_version))
        run("sudo rm -rf {}/web_static".format(new_version))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(new_version))
        print("New version deployed!")
        return True


def deploy():
    """
    Deploys archive to web servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
