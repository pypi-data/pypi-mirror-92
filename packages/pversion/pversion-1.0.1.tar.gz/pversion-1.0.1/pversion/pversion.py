import os


def get_version(package_name, version_file='_version.py'):
    """
    Retrieve the package version from a version file in the package root.

    :param package_name:
    :param version_file: version file name (inside package root)
    :return: package version
    """
    filename = os.path.join(package_name, version_file)
    with open(filename, 'rb') as fp:
        return fp.read().decode('utf8').split('=')[1].strip(" \n'")

