#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers
"""
from fabric.api import env, put, run, local
from datetime import datetime
from os.path import exists
from fabric.context_managers import lcd
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
        file_name = archive_path.split('/')[-1]
        new_folder = "/data/web_static/releases/{}".format(
            file_name.split('.')[0]
            )
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(new_folder))
        run("tar -xzf /tmp/{} -C {}".format(file_name, new_folder))
        run("rm /tmp/{}".format(file_name))
        run("mv {}/web_static/* {}".format(new_folder, new_folder))
        run("rm -rf {}/web_static".format(new_folder))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(new_folder))
        return True
    except Exception as e:
        return False


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


def do_clean(number=0):
    """
    Deletes unnecessary archives
    """
    try:
        number = int(number)
        if number < 1:
            number = 1

        with lcd('versions'):
            local(
                "ls -t | tail -n +{} | xargs -I {{}} rm -- {{}}"
                .format(number + 1)
                )

        releases = run("ls -t /data/web_static/releases").split()
        keep = releases[:number]

        for release in releases:
            if release not in keep:
                run("rm -rf /data/web_static/releases/{}".format(release))

        return True
    except Exception as e:
        return False
