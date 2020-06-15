""" methods.py

This file contains all algorithm pieces that are executed on the nodes.
It is important to note that the master method is also triggered on a
node just the same as any other method.

When a return statement is reached the result is send to the central
server after encryption.
"""

import time

from vantage6.tools.container_client import ClientContainerProtocol
from vantage6.tools.util import info
from itertools import chain

NUM_TRIES = 40


def column_names(client: ClientContainerProtocol, data, *args, **kwargs):
    """Master algoritm.

    Ask all nodes for their column names and combines them in one set.
    """
    retries = kwargs.get('tries', NUM_TRIES)


    # Get all organizations (ids) that are within the collaboration
    # FlaskIO knows the collaboration to which the container belongs
    # as this is encoded in the JWT (Bearer token)
    organizations = client.get_organizations_in_my_collaboration()
    ids = [organization.get("id") for organization in organizations]

    # The input for the algorithm is the same for all organizations
    # in this case
    info("Defining input parameters")
    input_ = {
        "method": "column_names",
    }

    # create a new task for all organizations in the collaboration.
    info("Dispatching node-tasks")
    task = client.create_new_task(
        input_=input_,
        organization_ids=ids
    )

    # Wait for node to return results. Instead of polling it is also
    # possible to subscribe to a websocket channel to get status
    # updates
    info("Waiting for results")
    task_id = task.get("id")

    for r in range(retries):
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

    # Create generator that lists all columns and turn it into a set to remove duplicates
    column_set = set(chain.from_iterable(results))

    info("master algorithm complete")

    # return all the messages from the nodes
    return column_set
