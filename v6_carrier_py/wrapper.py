import pickle
from typing import BinaryIO

from vantage6.client import serialization
from vantage6.tools import docker_wrapper
from vantage6.tools.data_format import DataFormat
from vantage6.tools.dispatch_rpc import dispact_rpc
from vantage6.tools.util import info
import os
import pandas as pd


def triplestore_wrapper(module: str):
    info(f"wrapper for {module}")

    # read input from the mounted inputfile.
    input_file = os.environ["INPUT_FILE"]
    info(f"Reading input file {input_file}")

    # TODO: _load_data handles input deserialization. It should be a public function
    input_data = docker_wrapper._load_data(input_file)

    query = input_data['query']

    # all containers receive a token, however this is usually only
    # used by the master method. But can be used by regular containers also
    # for example to find out the node_id.
    token_file = os.environ["TOKEN_FILE"]
    info(f"Reading token file '{token_file}'")
    with open(token_file) as fp:
        token = fp.read().strip()

    endpoint = os.environ["DATABASE_URI"]
    info(f"Using '{endpoint}' as triplestore endpoint")

    data = query_triplestore(endpoint, query)

    # make the actual call to the method/function
    info("Dispatching ...")
    output = dispact_rpc(data, input_data, module, token)

    # write output from the method to mounted output file. Which will be
    # transfered back to the server by the node-instance.
    output_file = os.environ["OUTPUT_FILE"]
    info(f"Writing output to {output_file}")
    with open(output_file, 'wb') as fp:
        if 'output_format' in input_data:
            output_format = input_data['output_format']

            # Indicate output format
            fp.write(output_format.encode() + b'.')

            # Write actual data
            output_format = DataFormat(output_format.lower())
            serialized = serialization.serialize(output, output_format)
            fp.write(serialized)
        else:
            # No output format specified, use legacy method
            fp.write(pickle.dumps(output))


def query_triplestore(endpoint: str, query: str):
    return pd.DataFrame()
