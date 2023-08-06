from typing import Union

import numpy as np
import pandas as pd


def _condition_mask(s: pd.Series, cond: Union[dict, str]):
    if isinstance(cond, dict):
        lo, hi = cond["lo"], cond["hi"]
        return (s >= lo) & (s <= hi)

    return s == cond


def conditions_mask(df: pd.DataFrame, rule: dict):
    """ Get a mask based on a dictionary of conditions
    """
    masks = []
    for key, cond in rule.items():
        masks.append(_condition_mask(df[key], cond))

    return np.all(np.array(masks), axis=0)


def apply_rule(df: pd.DataFrame, rule: dict) -> pd.DataFrame:
    """ Applies the rule to the population df to obtain a sample

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to apply the rule to

    rule : dict
        A set of conditions to apply to the dataframe

    Returns
    -------
    sample: pd.DataFrame
        The sample of the original dataframe based on rule conditions
    """
    mask = conditions_mask(df, rule)
    return df[mask]
