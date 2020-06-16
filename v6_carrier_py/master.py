""" methods.py

This file contains all algorithm pieces that are executed on the nodes.
It is important to note that the master method is also triggered on a
node just the same as any other method.

When a return statement is reached the result is send to the central
server after encryption.
"""

import time
from itertools import chain

from vantage6.tools.container_client import ClientContainerProtocol
from vantage6.tools.util import info

NUM_TRIES = 40


def dispatch_tasks(client: ClientContainerProtocol, data, *args, method=None, **kwargs):
    """
    Generic master algoritm
    """
    if not method:
        raise Exception('You have to specify a method.')

    tries = kwargs.get('tries', NUM_TRIES)

    my_organization = client.whoami.organization_id

    # Get all organizations (ids) that are within the collaboration
    # FlaskIO knows the collaboration to which the container belongs
    # as this is encoded in the JWT (Bearer token)
    organizations = client.get_organizations_in_my_collaboration()
    ids = map(lambda x: x['id'], organizations)
    ids = filter(lambda x: x != my_organization, ids)

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


def column_names(client: ClientContainerProtocol, data, *args, **kwargs):
    """Master algoritm.

    Ask all nodes for their column names and combines them in one set.
    """

    results = dispatch_tasks(client, data, method='column_names')

    # Create generator that lists all columns and turn it into a set to remove duplicates
    column_set = set(chain.from_iterable(results))

    info("master algorithm complete")

    # return all the messages from the nodes
    return column_set
