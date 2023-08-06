# ec2-compare
[![PyPI - ec2-compare](https://img.shields.io/pypi/v/ec2-compare.svg?color=blue&label=ec2-compare)](https://pypi.org/project/ec2-compare)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ec2-compare.svg?color=blue)](https://pypi.org/project/ec2-compare)
[![Coverage](https://img.shields.io/codecov/c/github/weldpua2008/ec2-compare)](https://codecov.io/gh/weldpua2008/ec2-compare)
[![PyPI - Downloads](https://img.shields.io/pypi/dw/ec2-compare?color=blue)](https://pypistats.org/packages/ec2-compare)

Compare EC2 instances families without querying AWS API


## Example:

* Getting on instances by parameters
```python
import ec2_compare.mixin
req = ec2_compare.mixin.EmrRequestMixin().ec3__get_machines(
    max_instances=5, # maximum number of machines
    # reuest parameters
    **{
        'cpu': 40, 'ram': 786432, 'min_cpu': 8, 'min_ram': 65536,
        'InstanceType': ['c4', 'c5.', 'r4', 'r5.', 'm4', 'm5.'],
        'SupportedArchitectures': ['x86_64'], 'SupportedUsageClasses': 'spot'
    })
```

* Getting on instances suitable for on-demand

```python

>>> import ec2_compare.internal.on_demand
>>> ec2_compare.internal.on_demand.get_instances_dict()[0]['InstanceType']
'm5d.xlarge'

```

## Why it's more memory & CPU efficient

1). ec2-compare
* Memory (penalty 8.1 Mb - 8175616 bytes)
```python
>>>
def getCurrentMemoryUsage():
    ''' Memory usage in Bytes '''
    import psutil
    import os
    process = psutil.Process(os.getpid())
    return process.memory_info().rss
>>> getCurrentMemoryUsage()
9535488
>>> import ec2_compare.ec2data
>>> getCurrentMemoryUsage()
17641472
>>> len(ec2_compare.ec2data.get_instances_dict())
341
>>> getCurrentMemoryUsage()
17711104
```
*  Load time:
```python
>>> import timeit
>>> timeit.timeit('import ec2_compare.ec2data;len(ec2_compare.ec2data.get_instances_dict())', number=1)
0.0028156930000000635
>>> timeit.timeit('import ec2_compare.ec2data;len(ec2_compare.ec2data.get_instances_dict())', number=1)
0.001711632000002794
>>> timeit.timeit('import ec2_compare.ec2data;len(ec2_compare.ec2data.get_instances_dict())', number=1000)
0.8330168470000032
>>> timeit.timeit('import ec2_compare.ec2data;len(ec2_compare.ec2data.get_instances_dict())', number=1000)
0.8174298469999997
```

2). Reading from json file:

* Memory (penalty 2.5 Mb - 2592768 bytes)

```python
>>> getCurrentMemoryUsage()
9379840
>>> import json
>>> with open("./helpers/aws_ec2.json") as json_file:
...     json.load(json_file)
...
>>> getCurrentMemoryUsage()
11972608
```

* Load time:

```python
>>> import timeit
>>>
s= '''
import json
with open("./helpers/aws_ec2.json") as json_file:
    json.load(json_file)
'''
timeit.timeit(s, number=1000)
>>
4.628850890999999
```

## Versioning

`ec2_compare` follows
[PEP 440](https://www.python.org/dev/peps/pep-0440/).


## How to build

```bash
python -m pip install -e ./[devel]
# or pip install -e ./[devel]

# Running tests
scripts/tests.sh
```

## Update data Locally
1. Downland the latest info
````bash
aws ec2 describe-instance-types | jq '.InstanceTypes' > aws_ec2.json
````
2. repack
```bash
python3 repack.py
```

## Thank you
- https://github.com/actions/ for an awesome github actions
- [mypy](https://github.com/python/mypy) for doing all dirty work for us
