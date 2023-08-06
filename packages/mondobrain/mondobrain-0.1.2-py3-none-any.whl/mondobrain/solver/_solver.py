import io

import numpy as np
import pandas as pd

from mondobrain.api import solve_result, solve_start_file
import mondobrain.datautils as datautils
from mondobrain.dd_transformer import DDTransformer
from mondobrain.error import NotEnoughPointsError
from mondobrain.utils import constants, utilities
from mondobrain.utils.data import is_discrete


def solve(
    df: pd.DataFrame,
    outcome: str = None,
    target: str = None,
    encode=True,
    sample=True,
    random_state=None,
    **kwargs
):
    """Run a solve without worrying about API requests.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to use for the solve

    outcome : str, default=None
        Which column to use as the outcome for the solve (sometimes referred to as a
        target feature). If None, then the first column is selected

    target: str, default=None
        The class in the outcome column to target. For a continuous outcome this should
        either be `min` or `max`. If None, then the first class or `max` is selected.

    encode: bool, default=True
        Whether or not the data should be encoded before being sent to the MB API.
        Encoding can result in additional time on client side. Disable if your data is
        largely non-sensitive.

    sample: bool, default=True
        Whether or not the data should be sampled before being sent to the MB API.
        Not pre-sampling the data can cause size limits to be reached and excessive
        solve times

    random_state : int or np.random.RandomStateInstance, default: 0
        Pseudo-random number generator to control the sampling state.
        Use an int for reproducible results across function calls.
        See the sklearn for more details.

    kwargs: any
        Remaining kwargs are sent so solve_start_file

    Returns
    -------
    rule: dict
        The conditions that the MB API found
    """
    if outcome is None:
        outcome = df.columns[0]

    if target is None:
        if df[outcome].dtype == np.object:
            target = df[outcome].iloc[0]
        else:
            target = "max"

    if encode:
        # Some utilities require original values
        df_orig = df.copy()
        outcome_orig = outcome
        target_orig = target

        encoder = DDTransformer(df)
        df = utilities.encode_dataframe(df, encoder)
        outcome = encoder.original_to_encoded_column(outcome)
        target = utilities.encode_value(df_orig, outcome_orig, target_orig, encoder)

    if sample:
        df = datautils.sample(
            df,
            2500,
            outcome=outcome,
            target=target,
            floor=3500,
            random_state=random_state,
        )

    _dimensionality_check(df, outcome, target)

    data = io.BytesIO()
    df.to_parquet(data)
    data.seek(0)  # Reset the pointer as `to_parquet` leaves it at the end

    task = solve_start_file(outcome=outcome, target=target, data=data, **kwargs)
    result = solve_result(id=task["id"])

    rule = result["rule"]

    if encode:
        # We need to decode the rule if we encoded
        rule = utilities.decode_rule(rule, encoder)

    return rule


def _dimensionality_check(df: pd.DataFrame, outcome: str, target: str):
    col = df[outcome]

    if is_discrete(col):
        size = col[col == target].shape[0]
    else:
        if col.std() == 0:
            raise NotEnoughPointsError("Outcome column has no variance")

        size = col.shape[0]

    if size <= constants.MIN_SOLVER_SIZE:
        raise NotEnoughPointsError("Not enough points")
