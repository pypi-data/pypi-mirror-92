import glob
import os
import re
from os.path import sep
import geopandas as gpd

import pandas as pd
from zipfile import ZipFile
from fiona.errors import DriverError


def export_csv(output, path):
    """
    Exports the dataset in chucks. This allows a more efficient and fast export of the dataset.
    """

    n = 50000
    output = [output[i:i + n] for i in range(0, output.shape[0], n)]

    header = True
    for chunk in output:
        chunk.to_csv(path, header=header, mode='a', sep=';', index=False)
        header = False

    return True


def define_output_names(outputs, destination_path, component_slug):
    """
    Analyze the output and generates a list of object to save paired with the file name.

    @param component_slug: slug of the component currently running
    @param destination_path: destination path for the output
    @param outputs: list of components output
    @return: list of outputs and list of outputs names
    """

    output_list = []
    tuple_case = False

    # Case 1: (string, obj)
    if isinstance(outputs, tuple) and len(outputs) == 2 and isinstance(outputs[0], str):
        output_list.append(outputs)
        tuple_case = True

    # Case 2: list of tuples -> [(string, obj)]
    elif isinstance(outputs, list) and len(outputs) > 0 and isinstance(outputs[0], tuple) and len(
            outputs[0]) == 2 and isinstance(outputs[0][0], str):
        output_list = outputs
        tuple_case = True

    # Case 3: list of objs -> [obj]
    elif isinstance(outputs, list) and len(outputs) > 0 and isinstance(outputs[0], object):
        output_list = outputs

    # Case 4: obj
    else:
        output_list.append(outputs)

    # Initialize the list of output names with a default name that is the name of the component followed by the index
    # of the parameters in the list. In this way the user can understand easily the content of the file.
    names = [os.path.join(destination_path, component_slug + f'_out{i}') for i in range(0, len(outputs))]

    output_list_cleaned = output_list

    # If we fall in the case of tuple or list of tuples we extract the filename from the first element of the tuple.
    if tuple_case:

        # Iterate over all outputs
        for i, output in enumerate(output_list):
            if len(output[0]) > 0:
                names[i] = os.path.join(destination_path, output[0])
                output_list_cleaned[i] = output[1]

    # Return the list of outputs and names
    return output_list_cleaned, names


def read_file(folder, filename, version):
    """
    Search in the folder the file and retrieve the specified version.
    """

    latest_version_filter = find_last_version(folder=folder, filename=filename)

    fixed_filename = filename

    if latest_version_filter is not None:
        fixed_filename = os.path.join(sep.join(filename.split(sep)[:-1]),
                                      filename.split(sep)[-1].split('.')[0] + '_v{}.'.format(
                                          latest_version_filter) + filename.split(sep)[-1].split('.')[1])

    path = os.path.join(folder, fixed_filename)
    if filename.endswith('.csv'):
        return pd.read_csv(path, sep=';')
    elif filename.endswith('.xlsx') or filename.endswith('.xls'):
        return pd.read_excel(path)
    elif filename.endswith('.shp'):
        return gpd.read_file(path)
    elif filename.endswith('.zip'):
        return ZipFile(path, 'r')

    return None


def find_last_version(folder, filename):
    """
    Retrieve the latest version of the filename in the folder.

    :param folder: where the file is searched
    :param filename: filename to find the version
    :return: latest version
    """

    filename_without_extension = filename.split(sep)[-1].split('.')[0]
    path_appendix = sep.join(filename.split(sep)[:-1])

    # Use a regex to find the files that are compatible with the filename
    file_list = glob.glob(rf'{os.path.join(folder, path_appendix, filename_without_extension)}_v*')

    # Extract from the name of the file the version and create an array of versions
    versions = [int(re.search('_v(\d+).', file).group(1)) for file in file_list]

    # Sort the array version
    versions = sorted(versions)

    # The last version is the last item in the array of versions otherwise None
    last_version = versions[-1] if versions else None

    return last_version


class StorageManager:
    """
    Class that manages the output. It handles the local storage.
    """

    def __init__(self, local_source, local_destination, logger):
        """
        Class constructor.

        @param local_source: source folder in the local device
        @param local_destination: destination folder in the local devide
        @param logger: logger manager
        """

        self.logger = logger

        # Validate local source
        self.local_source = self.validate_and_create_path(folder=local_source, force=True)

        # Validate local destination
        self.local_destination = self.validate_and_create_path(folder=local_destination, force=True)

        self.logger.info('Local source folder: {}'.format(local_source))
        self.logger.info('Local destination folder: {}'.format(local_destination))

        # Maps the slug of the component with the destination path
        self.destination_map = {}

    def get_file(self, filename, version='latest'):
        """
        Return (if exists) the file corresponding to the filename in input. Zoe selects
        automatically the version you need, otherwise return the latest one.

        :param filename: name of the file to be loaded
        :param version: version of the file to be loaded
        :return: file content
        """

        try:
            return read_file(folder=self.local_source, filename=filename, version=version)
        except FileNotFoundError:
            return read_file(folder=self.local_destination, filename=filename, version=version)
        except DriverError:
            return read_file(folder=self.local_destination, filename=filename, version=version)

    def export(self, outputs, slug):

        # For each output find or create the output name
        outputs, output_names = define_output_names(outputs, self.destination_map[slug], slug)

        # Iterate over all outputs and exports each one
        for i, output in enumerate(outputs):
            self.export_output(output, output_names[i])

        return True

    def export_output(self, output, output_name):
        """
        Export the output from the function of the component.
        """

        # Check if the file already exists and find the last version
        latest_version_filter = find_last_version(folder='', filename=output_name)

        if latest_version_filter is not None and latest_version_filter >= 0:
            latest_version_filter += 1
            fixed_filename = output_name.split('.')[0] + '_v{}.csv'.format(latest_version_filter)
        else:
            fixed_filename = output_name.split('.')[0] + '_v0.csv'

        path = fixed_filename
        # DataFrame case
        if isinstance(output, pd.DataFrame):
            export_csv(output, path)
            self.logger.success('Exported dataset \'{}\' in \'{}\'.'.format(fixed_filename, self.local_destination))

        # All other cases
        else:
            self.logger.info('Output format not supported yet!')

    def validate_and_create_path(self, folder, prefix=None, force=True):
        """
        Check if the path points to a folder and validates it.
        """

        path = folder if not prefix else os.path.join(prefix, folder)

        # Check if the path is a folder path or a file path.
        if '.' in path.split(os.sep)[-1]:
            self.logger.log("'{}' is file path, please provide a folder path.".format(path), terminate=True)

        # Check if the path exists.
        if not os.path.isdir(path):

            # If the force flag is not set, the execution terminates.
            if not force:
                self.logger.log("'{}' is not a valid path.".format(path), terminate=True)

            # The folder is created.
            os.mkdir(path=path)

        return path

    def create_sub_destination_folder(self, folder, id):
        """
        Create the root folder for the pipeline outputs.

        @param folder: path
        @return: path validated
        """

        self.destination_map[id] = self.validate_and_create_path(folder, self.local_destination)

        return self.destination_map[id]