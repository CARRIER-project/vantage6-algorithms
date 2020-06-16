![Build](https://github.com/CARRIER-project/vantage6-algorithms/workflows/Build/badge.svg)
<h1 align="center">
  <br>
[![Coverage Status](https://coveralls.io/repos/github/CARRIER-project/vantage6-algorithms/badge.svg?branch=master)](https://coveralls.io/github/CARRIER-project/vantage6-algorithms?branch=master)  
  
  
  <a href="https://vantage6.ai"><img src="https://github.com/IKNL/guidelines/blob/master/resources/logos/vantage6.png?raw=true" alt="vantage6" width="400"></a>
</h1>

<h3 align=center> A privacy preserving federated learning solution</h3>

--------------------

# v6-CARRIER-py
This algorithm is part of the [vantage6](https://vantage6.ai) solution. Vantage6 allows to execute computations on federated datasets. This repository provides a boilerplate for new algorithms.

### {algorithm_name}/__init__.py
Contains all the methods that can be called at the nodes. All __regular__ definitions in this file that have the prefix `RPC_` are callable by an external party. If you define a __master__ method, it should *not* contain the prefix! The __master__ and __regular__ definitions both have there own signature. __Master__ definitions have a __client__ and __data__ argument (and possible some other arguments), while the __regular__ definition only has the __data__ argument. The data argument is a [pandas dataframe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html?highlight=dataframe#pandas.DataFrame) and the client argument is a `ClientContainerProtocol` or `ClientMockProtocol` from the [vantage6-toolkit](https://github.com/IKNL/vantage6-toolkit). The master and regular definitions signatures should look like:
```python
def some_master_name(client, data, *args, **kwargs):
    # do something
    pass

def RPC_some_regular_method(data, *args, **kwargs):
    # do something
    pass
```

### setup.py
In order for the Docker image to find the methods the algorithm needs to be installable. Make sure the *name* matches the `ARG PKG_NAME` in the Dockerfile.

## Read more
See the [documentation](https://docs.vantage6.ai/) for detailed instructions on how to install and use the server and nodes.

------------------------------------
> [vantage6](https://vantage6.ai)
