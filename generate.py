import os
import argparse
import shutil
import yaml
from jinja2 import Environment, FileSystemLoader


def get_wrkdir():
    wrkdir = os.path.dirname(os.path.abspath(__file__))
    return wrkdir


def generate_dockerfiles(output_path, nuage_docker_config):
    """
    This function is responsible to generate nuage-dockerfiles and
    nuage.repo in their respective project directories.
    For ex:
      All heat dockerfiles will be created under project-heat
     horizon dockerfile will be created under project-horizon
      neutron-server dockerfile will be created under project-neutron
      nova-compute dockerfile will be created under project-compute
    """
    wrkdir = get_wrkdir()
    env = Environment(loader=FileSystemLoader('%s/nuage-dockerfiles-j2/'
                                              % wrkdir))
    docker_images = nuage_docker_config['DockerImages']
    for image in docker_images:
        nuage_dockerfiles = output_path + '/project-' + image.split('-')[0]
        if not os.path.exists(nuage_dockerfiles):
            os.makedirs(nuage_dockerfiles)
        dockerfile_name = 'nuage-' + image + '-dockerfile'
        j2_dockerfile = dockerfile_name + '.j2'
        print("Generating ", dockerfile_name)
        dockerfile = env.get_template(j2_dockerfile)
        with open('%s/%s' % (nuage_dockerfiles, dockerfile_name), 'w') as \
                dockerfile_file:
            dockerfile_file.write(dockerfile.render(
                nuage_config=nuage_docker_config))

    nuage_repo = env.get_template("nuage.repo.j2")
    print("Generating nuage repo file")
    with open('%s/nuage.repo' % output_path,
              'w') as dockerfile_file:
        dockerfile_file.write(nuage_repo.render(
            nuage_config=nuage_docker_config))


def copy_licenses(output_path):
    # This function will copy licenses directory
    wrkdir = get_wrkdir()
    source = wrkdir + '/licenses/'
    destination = output_path + '/licenses'
    shutil.copytree(source, destination)


def copy_gpgkey(output_path):
    # This function will copy gpgkey
    wrkdir = get_wrkdir()
    source = wrkdir + '/RPM-GPG-KEY-Nuage'
    destination = output_path + '/RPM-GPG-KEY-Nuage'
    shutil.copyfile(source, destination)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config')
    parser.add_argument('output')
    argument = parser.parse_args()
    with open(argument.config) as ndc:
        nuage_docker_config = yaml.load(ndc)
        generate_dockerfiles(argument.output, nuage_docker_config)
        copy_licenses(argument.output)
        copy_gpgkey(argument.output)
    print("Done")


if __name__ == "__main__":
    main()
