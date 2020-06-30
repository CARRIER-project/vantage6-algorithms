""" methods.py

This file contains all algorithm pieces that are executed on the nodes.
It is important to note that the master method is also triggered on a
node just the same as any other method.

When a return statement is reached the result is send to the central
server after encryption.
"""
import time
from functools import reduce
from itertools import chain
from typing import List

import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from vantage6.tools.container_client import ClientContainerProtocol
from vantage6.tools.util import info
import traceback

NUM_TRIES = 40
TOKEN_FILE = 'TOKEN_FILE'
RANDOM_SEED = 5


def _dispatch_tasks(client: ClientContainerProtocol, data, method, *args, exclude_orgs=(), **kwargs):
    """
    Generic master algorithm
    """
    tries = kwargs.get('tries', NUM_TRIES)

    # Get all organizations (ids) that are within the collaboration
    # FlaskIO knows the collaboration to which the container belongs
    # as this is encoded in the JWT (Bearer token)
    organizations = client.get_organizations_in_my_collaboration()

    info(f'Organizations in my collaboration: {organizations}')

    ids = map(lambda x: x['id'], organizations)
    ids = filter(lambda x: x not in exclude_orgs, ids)
    ids = list(ids)

    info(f'Dispatching task to organizations with ids {ids}.\n{exclude_orgs} will be excluded.')

    # The input for the algorithm is the same for all organizations
    # in this case
    info("Defining input parameters")
    input_ = {
        "method": method,
    }

    # create a new task for all organizations in the collaboration.
    info("Dispatching node-tasks")
    task = client.create_new_task(
        input_=input_,
        organization_ids=list(ids)
    )

    return _get_results(client, tries, task)


def _get_results(client, tries, task):
    """
    Check up to n times if a task has completed, return the results if possible. Otherwise, raise an exception.
    """
    # Wait for node to return results. Instead of polling it is also
    # possible to subscribe to a websocket channel to get status
    # updates
    info("Waiting for results")
    task_id = task.get("id")
    for r in range(tries):
        task = client.get_task(task_id)
        if task.get('complete'):
            break

        info("Waiting for results")
        time.sleep(1)
    # Raise Exception if task has still not completed
    if not task.get('complete'):
        raise Exception(f'Task timeout for master function column names\ntask id: {task_id}')
    info("Obtaining results")
    results = client.get_results(task_id=task.get("id"))
    return results


def column_names(client: ClientContainerProtocol, data, *args, exclude_orgs=(), **kwargs):
    """Master algoritm.

    Ask all nodes for their column names and combines them in one set.
    """

    results = _dispatch_tasks(client, data, *args, method='column_names', exclude_orgs=exclude_orgs, **kwargs)

    # Create generator that lists all columns and turn it into a set to remove duplicates
    column_set = set(chain.from_iterable(results))

    info("master algorithm complete")

    # return all the messages from the nodes
    return column_set


def correlation_matrix(client: ClientContainerProtocol, data, keys=None, *args, **kwargs):
    """
    Compute a correlation matrix over all datasets together. Data will be joined using the specified key. Right now
    the datasets are merged using outer join, which means that keys without matches will get empty values for the
    missing columns.

    If multiple keys are specified records are merged when all keys match.

    If no keys are specified the datasets are joined on all columns with the same name.
    TODO: What if different datasets use different keys to mean the same thing? How do we specify this?
    """
    combined_df = _combine_all_node_data(client, data, keys, *args, **kwargs)

    return combined_df.corr()


def fit_pipeline(client: ClientContainerProtocol, data, pipeline: Pipeline, features: List[str], target: str,
                 identifying_columns=None, *args, **kwargs):
    """
    Retrieve data from nodes and train data analysis pipeline on it. Returns the performance of the resulting model.
    TODO: How and where do we save our model?

    :param client: Client for accessing Vantage6 proxy server. Is a parameter for all master algorithms
    :param data: Data from datastation as Pandas DataFrame. Is handled by wrapper
    :param pipeline: A sklearn pipeline containing one or multiple data transformations. Should have a `fit` and
                        `predict` method.
    :param features: The features that should be used in the fitting of the pipeline.
    :param target: The field that should be used as target for the machine learning algorithm.
    :param identifying_columns: The identifying fields for joining datasets.
    :param args:
    :param kwargs:
    :return:
    """
    try:
        info(f'Training pipeline with the following steps: {pipeline.named_steps}')
        results = _combine_all_node_data(client, data, identifying_columns, *args, **kwargs)

        X = results[features].values
        y = results[target].values

        # Split data
        # TODO: Make splitting of dataset controllable from client-side
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=RANDOM_SEED)

        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)

        # TODO: Make metrics configurable
        score = metrics.mean_absolute_error(y_test, predictions)

        return score
    except Exception as e:
        # Log stacktrace
        traceback.print_exc()


def _combine_all_node_data(client, data, identifying_columns, *args, **kwargs) -> pd.DataFrame:
    results = _dispatch_tasks(client, data, method='get_data', *args, **kwargs)

    for r in results:
        info(f'Retrieved node data with columns {r.columns}')

    combined_df = _merge_multiple_dfs(results, on=identifying_columns)

    print(combined_df.columns)

    return combined_df


def _merge_multiple_dfs(df_list, on):
    # TODO: How should we handle DataFrames with overlapping when those are not part of the join keys?
    # TODO: Decide what type of join to use. We should keep the maximum amount of records possible
    return reduce(lambda left, right: pd.merge(left, right, on=on, how='inner', suffixes=(False, False)), df_list)
