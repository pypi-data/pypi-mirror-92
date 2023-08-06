import numpy as np
import pandas as pd
from IPython.display import display


def drop_missing(dataset, threshold=0.45, drop_cols=[]):
    """
    Process missing columns

  Returns
    ----------
    Dataset with the columns dropped
    Dropped columns name as a list

  Parameters
    ----------
    dataset : DataSet


    threshold : default=0.45
    amount of missing value in columns required to drop the column

    drop_cols : default=[]
    list of columns to be dropped. If not given, function will drop column based on amount of missing values

    """

    if not drop_cols:
        rows = len(dataset)
        num_of_nones = round((1 - threshold) * rows, 0)
        for k, v in (dataset.isnull().sum() / rows).items(): #for loop for appending the keys of dropped columns
            if v > threshold:
                drop_cols.append(k)

        d = dataset.dropna(axis=1, thresh=num_of_nones) #axis = 1 : remove coloumn , thresh : no. of nons to ramove column
    else:
        d = dataset.drop(drop_cols, axis=1)

    return d, drop_cols



def fill_numeric(dataset, missing_val):
    """
 Helper function that replace NAs numeric values with the median of the column

     Returns
        ----------
        missing_val with columns as key and median of the respective column as values

      Parameters
        ----------
        dataset :  Dataset
        missing_val: Dictionary with column name as key and nan values

    """
    for col in dataset.columns:
        if pd.api.types.is_numeric_dtype(dataset[col].dtypes):
            if dataset[col].isnull().sum():
                dataset[col].fillna(dataset[col].median(), inplace=True)
                missing_val[col] = dataset[col].median()
    return missing_val


def process_missing(dataset, missing_val={}):
    """
 Process missing values


    Returns
    ----------
      Dataset with missing values filled
      missing_val with columns as key and median of the respective column as values

    Parameters
    ----------
      dataset : DataSet
      missing_val : default={}
      Dictionary with column names as keys, value to replace NAs as values. If not given, function will replace numeric missing
      values with median of the respective column

    """
    d = dataset.copy()
    if not missing_val:
        missing_val = fill_numeric(d, missing_val)

    else:
        for k, v in missing_val.items():
            if d[k].isnull().sum():
                d[k].fillna(v, inplace=True)

        if d.isnull().sum().sum():
            for col in d.columns:
                missing_val = fill_numeric(d, missing_val)

    return d, missing_val


def convert_cat(dataset, category_cols=[]):
    """
    Helper method to convert column type to category

    :param dataset: Dateset
    :param category_cols: list of categorical columns needed to be encoded by default loop all
    :return: dataset and dictionary of cols which is category type
    """
    if category_cols:
        for col in category_cols:
            dataset[col] = dataset[col].astype("category")
    else:
        obj_columns = dataset.select_dtypes(['object']).columns
        for obj in obj_columns:
            dataset[obj] = dataset[obj].astype('category')
            category_cols.append(obj)
    return dataset, category_cols


def set_cat(dataset, cat_dict={}):
    """
Helper method to convert column type to category

    :param dataset: Dataset
    :param cat_dict: dictionary of categorical columns: list of cols needed to encoded as categories. by default loop
    all columns
    :return: dictionary of categorical columns
    """
    if cat_dict:
        for k, v in cat_dict.items():
            dataset[k] = dataset[k].cat.set_categories(v)
    else:
        for col in dataset.columns:
            if dataset[col].dtypes.name == "category":
                cat_dict[col] = dataset[col].cat.categories
    return cat_dict


def gen_dummies(dataset, cat_cols, max_cardi):
    """
    Helper method to Convert categorical variable into dummy/indicator variables.

    
    :param dataset: Dataset
    :param cat_cols: list of categorical columns
    :param max_cardi: max number of categories in column
    :return: dataset and list of cardinality clumns
    """
    cardi_cols = []
    for col in cat_cols:
        if len(dataset[col].cat.categories) <= max_cardi:
            cardi_cols.append(col)

    dataset = pd.get_dummies(dataset, columns=cardi_cols, prefix=cardi_cols, drop_first=True)

    return dataset, cardi_cols


def cat_codes(dataset, cat_cols):
    """
Helper method to encode categories
    :param dataset: Dataset
    :param cat_cols:list of categorical columns (categorical features)
    :return: none
    """
    for col in cat_cols:
        dataset[col] = dataset[col].cat.codes + 1  # series of codes from 1 to max cardinality


def process_cat(dataset, cat_cols=[], cat_dict={}, max_cardi=None):
    """
    Process categorical variables

    Returns
    ----------
    Dataset with categorical variables processed
    cat_dict with categorical columns as key and respective pandas.Series.cat.categories as values

    Parameters
    ----------
    dataset: Dataset

    cat_cols : default=[]
    list of pre-determined categorical variables

    cat_dict : default={}
    Dict with categorical variables as keys and pandas.Series.cat.categories as values. If not given, cat_dict is
    generated with for every categorical columns

    max_cardi : default=None
    maximum cardinality of the categorical variables. Which is the number of class in the categorical features.
    Categories variables with cardinality less or equal to max_cardi will be onehotencoded to produce dummies variables
    """
    d = dataset.copy()

    d, cat_cols = convert_cat(d, cat_cols)

    cat_dict = set_cat(d, cat_dict)

    if max_cardi:
        d, cardi_cols = gen_dummies(d, cat_cols, max_cardi)
        cat_cols = list(set(cat_cols) - set(cardi_cols))

    cat_codes(d, cat_cols)

    return d, cat_dict


def train_valid_split(dataset, num_valid, shuffle=False):
    """
    Split dataset into training and validation set

    Returns
    ----------
    Training and validation set respectively

    Parameters
    ----------
      dataset : Dataset

      num_valid : number of samples needed in validation set

    shuffle : default=False
    Shuffle the rows to randomly sample training and validation sets

    """
    if shuffle:
        dataset = dataset.sample(frac=1).reset_index(drop=True)

    n_trn = len(dataset) - num_valid
    n_train = dataset[:n_trn]
    n_valid = dataset[n_trn:]

    return n_train, n_valid

def display_all(dataset):
    """
    display all data
    Set max rows and columns to display
    Return: None
    """
    with pd.option_context("display.max_rows",1200):
        with pd.option_context("display.max_columns",1200):
            display(dataset)
