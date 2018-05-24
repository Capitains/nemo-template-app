import os


def relative_folder(configuration_file, directory):
    """ Compute the absolute folder of a directory based on the configuration_file path

    :param configuration_file: Configuration file path
    :param directory: Directory to set as absolute path
    :return: Absolute path of directory
    """
    return os.path.abspath(
            os.path.join(
                os.path.abspath(os.path.dirname(configuration_file)),
                directory
            )
    )
