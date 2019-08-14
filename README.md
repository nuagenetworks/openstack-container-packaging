# openstack-container-packaging

1) Create a new branch based of master
  Ex: git checkout -b 5.4.1


2) Make sure license file under scripts/licenses is upto date, if not update it.

3) Make sure the RPM-GPG-KEY-Nuage has correct key, if not update it.

4) Configure params in nuage_docker_config.yaml
  Description for values:
    OSRelease: <OpenStack release number>
    OSName: <OpenStack release name>
    NuageMajorRelease: <Nuage major release number>
    NuageMinorRelease:  <Nuage minor release number>
    NuageUpdateRelease: <Nuage update release number>
    NuageRelease: <Nuage dockerfile release number>
    RepoBaseUrl: <Nuage packages repo base url>
    NuageUpgradeScripts: <Nuage upgrade scripts tarball name>

  Example:
    OSRelease: 13 or 14
    OSName: queens or rocky
    NuageMajorRelease: 5 or 6
    NuageMinorRelease: 3 or 4
    NuageUpdateRelease: 2U2 or 3 or 1
    NuageRelease: Starts from 1, if there is a new release in same version, from previously generated dockerfiles get the release number and add 1 to it
    RepoBaseUrl: https://s3-us-west-1.amazonaws.com/nuage-public-mirror/574d63bb0727c27e014d8f27ccc275c3f9641b955e8aa7659d74e4df9cf7847a/5.3.2.U2/queens/ or https://s3-us-west-1.amazonaws.com/nuage-public-mirror/574d63bb0727c27e014d8f27ccc275c3f9641b955e8aa7659d74e4df9cf7847a/5.3.3/queens
    NuageUpgradeScripts: nuage-openstack-upgrade-5.3.3-222.tar.gz

5) Run the script generate.py 
  python generate.py

6) Once the above script completes successfully, then push all files to the new branch
  git add --all
  git commit -m <commit-message>
  git push origin <new-branch-name>
 
