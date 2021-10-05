import os
import pandas as pd


def read_join_datfiles(path_datfiles: str, output_path: str, name: str = 'production'):
    """
    Creates a dataframe with columns from independent datfiles (highly customised).
    """
    os.makedirs(output_path, exist_ok=True)
    files = os.listdir(path_datfiles)
    profiles = pd.DataFrame(index=pd.date_range(start='2020-12-31 23:00:00', periods=8760, freq='H'))
    counter = 1
    for file in files:
        profiles['member_{}'.format(counter)] = pd.read_csv(os.path.join(path_datfiles, file), header=None, sep=' ')[2].values
        counter += 1

    filled_df = fill_nan(profiles)
    dropped_df = filled_df.loc[:, (filled_df != 0).any(axis=0)]
    dropped_df.to_csv(os.path.join(output_path, '{}.csv'.format(name)))


def join_data(path_csv: str, output_path: str, name: str = 'demand'):
    """
    Creates a dataframe with columns from independent csv files.
    """
    os.makedirs(output_path, exist_ok=True)
    files = os.listdir(path_csv)
    profiles = pd.DataFrame(index=pd.date_range(start='2020-12-31 23:00:00', periods=35040, freq='15T'))
    counter = 1
    for file in files:
        profiles['member_{}'.format(counter)] = pd.read_csv(os.path.join(path_csv, file), header=None).values
        counter += 1

    filled_df = fill_nan(profiles)
    resampled_df = resample_data(filled_df, new_freq='H')
    dropped_df = resampled_df.loc[:, (resampled_df != 0).any(axis=0)]
    dropped_df.to_csv(os.path.join(output_path, '{}.csv'.format(name)))


def concatenate_data(iterable_path: list([str]), sheet_to_read: str, columns_to_read: list([str]),
                     columns_names_new: list([str])) -> pd.DataFrame:
    """
    Concatenates the data stored in different files.
    :param iterable_path: list with the paths to the data files.
    :param sheet_to_read: sheet to read.
    :param columns_to_read: columns of the final dataframe.
    :param columns_names_new: new column names.
    :return: dataframe with concatenated data.
    """
    concatenated_df = pd.DataFrame(columns=columns_to_read)
    for path in iterable_path:
        df_temp = pd.read_excel(path, sheet_name=sheet_to_read, usecols=columns_to_read)
        concatenated_df = pd.concat([concatenated_df, df_temp])

    concatenated_df.columns = columns_names_new

    return concatenated_df


def index_data(original_df: pd.DataFrame) -> pd.DataFrame:
    """
    Sets the index to the dataframe
    :param original_df: dataframe with the data.
    :return: indexed dataframe.
    """
    new_date_range = pd.date_range(start='2020-12-31 23:00:00', periods=len(original_df), freq='15T')

    return original_df.set_index(new_date_range)


def fill_nan(df_to_fill: pd.DataFrame) -> pd.DataFrame:
    """
    Fills data naively (back fill and forward fill).
    :param df_to_fill: original dataframe with nan to fill.
    :return: dataframe with filled information.
    """
    b_filled_df = df_to_fill.fillna(method='bfill')
    f_filled_df = b_filled_df.fillna(method='ffill')

    return f_filled_df


def resample_data(df_to_resample: pd.DataFrame, new_freq: str = 'H') -> pd.DataFrame:
    """
    Resamples the given dataframe.
    :param df_to_resample: original dataframe.
    :param new_freq: frequency in which to resample.
    :return: resampled dataframe containing only the desired dates.
    """
    return df_to_resample.resample(axis=0, rule=new_freq).apply('mean')


def pipeline(original_df: pd.DataFrame, fill_data_columns: list = []) -> pd.DataFrame:
    """
    Processes a dataframe according to the desired steps.
    :param original_df: original dataframe to be processed.
    :param fill_data_columns: list to determine whether to fill data when the original data is 0.
    :return:
    """
    # Fil NaN
    filled_df = fill_nan(original_df)
    if fill_data_columns:
        for column in fill_data_columns:
            if fill_data_columns == list(original_df.columns):
                filled_df[column] = 0.07
            else:
                filled_df[column] = filled_df['MeryTherm'].values * 0.95

    # Resampling to 1 hour resolution
    resampled_df = resample_data(filled_df, new_freq='H')

    return resampled_df


def process_data(iterable_path: list([str]), sheet_to_read: str, columns_to_read: list([str]),
                 columns_names_new: list([str]), output_path: str, fill_data_columns: list = []) -> pd.DataFrame:
    """
    Reads and processes dataframes.
    :param iterable_path: list with the paths to the data files.
    :param sheet_to_read: sheet to read.
    :param columns_to_read: columns of the final dataframe.
    :param columns_names_new: new column names.
    :param output_path: path and name of the csv to be saved.
    :return: processed dataframe.
    """
    concatenated_df = concatenate_data(iterable_path,
                                       sheet_to_read,
                                       columns_to_read,
                                       columns_names_new)
    indexed_df = index_data(concatenated_df)
    processed_df = pipeline(indexed_df, fill_data_columns)
    processed_df.to_csv(output_path)

    return processed_df


if __name__ == "__main__":

    path_files = './hauts_sarts/demand_raw'
    output_path = './hauts_sarts/input'
    join_data(path_files, output_path)

    path_files = './hauts_sarts/datfiles'
    output_path = './hauts_sarts/input'
    read_join_datfiles(path_files, output_path)

    # output_path = './example_merygrid/input'
    # path_constant = './data_merygrid/2021-'
    # path_variable = ['01.xlsx', '02.xlsx', '03.xlsx', '04.xlsx', '05.xlsx', '06.xlsx', '07.xlsx', '08.xlsx', '09.xlsx',
    #                  '10.xlsx', '11.xlsx', '12.xlsx']
    # list_paths = ['{}{}'.format(path_constant, path) for path in path_variable]
    #
    # # Demand and generation
    # sheet = 'power'
    # columns_demand_read = ['CBV [load][clean]', 'MeryBois [load][clean]', 'MeryTherm [load][clean]']
    # columns_demand_new = ['CBV', 'MeryBois', 'MeryTherm']
    # demand = process_data(iterable_path=list_paths,
    #                       sheet_to_read=sheet,
    #                       columns_to_read=columns_demand_read,
    #                       columns_names_new=columns_demand_new,
    #                       output_path='{}/demand.csv'.format(output_path))
    # columns_production_read = ['CBV [prod][clean]', 'MeryBois [prod][clean]', 'MeryTherm [prod][clean]']
    # columns_production_new = ['CBV', 'MeryBois', 'MeryTherm']
    # production = process_data(iterable_path=list_paths,
    #                           sheet_to_read=sheet,
    #                           columns_to_read=columns_production_read,
    #                           columns_names_new=columns_production_new,
    #                           output_path='{}/generation.csv'.format(output_path))
    #
    # # Grid prices
    # sheet = 'grid'
    # columns_price_import = ['CBV Entity: GRID_PURCHASE_PRICE', 'MeryBois Entity: GRID_PURCHASE_PRICE',
    #                         'MeryTherm Entity: GRID_PURCHASE_PRICE']
    # columns_price_import_new = ['CBV', 'MeryBois', 'MeryTherm']
    # price_global_import = process_data(iterable_path=list_paths,
    #                                    sheet_to_read=sheet,
    #                                    columns_to_read=columns_price_import,
    #                                    columns_names_new=columns_price_import_new,
    #                                    output_path='{}/prices_global_import.csv'.format(output_path))
    # columns_price_export = ['CBV Entity: GRID_SALE_PRICE', 'MeryBois Entity: GRID_SALE_PRICE',
    #                         'MeryTherm Entity: GRID_SALE_PRICE']
    # columns_price_export_new = ['CBV', 'MeryBois', 'MeryTherm']
    # fill_data_columns = ['CBV', 'MeryBois']
    # price_global_export = process_data(iterable_path=list_paths,
    #                                    sheet_to_read=sheet,
    #                                    columns_to_read=columns_price_export,
    #                                    columns_names_new=columns_price_export_new,
    #                                    output_path='{}/prices_global_export.csv'.format(output_path),
    #                                    fill_data_columns=fill_data_columns)
    #
    # # REC prices
    # sheet = 'community'
    # columns_price_import = ['CBV Entity: COMMUNITY_PURCHASE_PRICE', 'MeryBois Entity: COMMUNITY_PURCHASE_PRICE',
    #                         'MeryTherm Entity: COMMUNITY_PURCHASE_PRICE']
    # columns_price_import_new = ['CBV', 'MeryBois', 'MeryTherm']
    # fill_data_columns = ['CBV', 'MeryBois', 'MeryTherm']
    # price_local_import = process_data(iterable_path=list_paths,
    #                                    sheet_to_read=sheet,
    #                                    columns_to_read=columns_price_import,
    #                                    columns_names_new=columns_price_import_new,
    #                                    output_path='{}/prices_local_import.csv'.format(output_path),
    #                                    fill_data_columns=fill_data_columns)
    # columns_price_export = ['CBV Entity: COMMUNITY_SALE_PRICE', 'MeryBois Entity: COMMUNITY_SALE_PRICE',
    #                         'MeryTherm Entity: COMMUNITY_SALE_PRICE']
    # columns_price_export_new = ['CBV', 'MeryBois', 'MeryTherm']
    # fill_data_columns = ['CBV', 'MeryBois', 'MeryTherm']
    # price_local_export = process_data(iterable_path=list_paths,
    #                                    sheet_to_read=sheet,
    #                                    columns_to_read=columns_price_export,
    #                                    columns_names_new=columns_price_export_new,
    #                                    output_path='{}/prices_local_export.csv'.format(output_path),
    #                                    fill_data_columns=fill_data_columns)
