import os
import shutil
import yaml
from jinja2 import Environment, FileSystemLoader


def get_dirpath_and_scriptpath():
    """
    Using this function user can get the current working directory
    and the directory to which the generated nuage-dockerfiles,
    licenses and gpgkey to be copied.
    """
    scriptspath = os.path.dirname(os.path.abspath(__file__))
    dirpath = scriptspath.split('/scripts')[0]
    return scriptspath, dirpath


def generate_dockerfiles(nuage_docker_config):
    """
    This function is responsible to generate nuage-dockerfiles and
    nuage.repo in their respective project directories.
    For ex:
      All heat dockerfiles will be created under project-heat
     horizon dockerfile will be created under project-horizon
      neutron-server dockerfile will be created under project-neutron
      nova-compute dockerfile will be created under project-compute
    """
    scriptspath, dirpath = get_dirpath_and_scriptpath()
    env = Environment(loader=FileSystemLoader('%s/nuage-dockerfiles-j2/' 
                                              % scriptspath))
    docker_images = nuage_docker_config['DockerImages'].split(',')
    for image in docker_images:
        nuage_dockerfiles = dirpath + '/' + nuage_docker_config['OSName']\
                            + '/project-' + image.split('-')[0]
        if not os.path.exists(nuage_dockerfiles):
            os.makedirs(nuage_dockerfiles)
        dockerfile_name = 'nuage-' + image + '-dockerfile'
        j2_dockerfile = dockerfile_name + '.j2'
        print "Generating ", dockerfile_name
        dockerfile = env.get_template(j2_dockerfile)
        with open('%s/%s' % (nuage_dockerfiles, dockerfile_name), 'w') as \
                dockerfile_file:
            dockerfile_file.write(dockerfile.render(
                nuage_config=nuage_docker_config))

    nuage_repo = env.get_template("nuage.repo.j2")
    print "Generating nuage repo file"
    with open('%s/%s/nuage.repo' % (dirpath, nuage_docker_config['OSName']),
              'w') as dockerfile_file:
        dockerfile_file.write(nuage_repo.render(
            nuage_config=nuage_docker_config))


def copy_licenses(version):
    # This function will copy licenses directory
    scriptspath, dirpath = get_dirpath_and_scriptpath()
    source = scriptspath + '/licenses/'
    destination = dirpath + '/' + version + '/licenses'
    shutil.copytree(source, destination)


def copy_gpgkey(version):
    # This function will copy gpgkey
    scriptspath, dirpath = get_dirpath_and_scriptpath()
    source = scriptspath + '/RPM-GPG-KEY-Nuage'
    destination = dirpath + '/' + version + '/RPM-GPG-KEY-Nuage'
    shutil.copyfile(source, destination)


def main():
    """
    This is the main function reads all the required configs from
    nuage_docker_config.yaml and calls the functions in an order.
    """
    with open("nuage_docker_config.yaml") as ndc:
        nuage_docker_config = yaml.load(ndc)
    nuage_docker_config['DockerImages'] = 'heat-api-cfn,heat-api,heat-eng' \
                                          'ine,horizon,neutron-server,' \
                                          'nova-compute'
    generate_dockerfiles(nuage_docker_config)
    copy_licenses(nuage_docker_config['OSName'])
    copy_gpgkey(nuage_docker_config['OSName'])
    print "Done"


if __name__ == "__main__":
    main()

