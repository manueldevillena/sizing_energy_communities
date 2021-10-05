import numpy as np
import pandas as pd

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper



class ParsingException(Exception):
    def __init__(self, indexes: list):
        super().__init__()
        self.indexes = indexes

    def __str__(self):
        return "Invalid values at indexes:\n\t" + '\n\t'.join(map(str, self.indexes))


def read_data(data_path: str) -> pd.DataFrame:
    """
    Reads CSV file returning an object.

    :param data_path: Path to the data to read.
    :return Dataframe with the read data.
    """
    df = pd.read_csv(data_path, header=0, index_col=0, parse_dates=True, infer_datetime_format=True, dtype=float)
    null_loc, _ = np.where(df.isna())
    if len(null_loc) != 0:
        raise ParsingException(indexes=df.index[null_loc])
    return df


def read_inputs(inputs_path: str) -> dict:
    """
    Reads YML file with inputs.
    :param inputs_path: Path to the inputs file.
    :return: Dictionary with the read data.
    """
    with open(inputs_path) as infile:
        data = yaml.load(infile, Loader=Loader)
    return data


def set_file_to_object(target_object, path_to__files, file_to_set):
    """
    Sets a given csv file as an attribute of an object with the same name.
    :param target_object: Object for which the attribute is created.
    :param path_to__files: Path to the csv files.
    :param file_to_set: File to set as an attibute for the given object.
    """
    file_path = '{}/{}.csv'.format(path_to__files, file_to_set)
    setattr(target_object, file_to_set, read_data(file_path))
