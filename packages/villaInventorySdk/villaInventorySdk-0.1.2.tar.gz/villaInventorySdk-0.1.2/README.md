# villaInventorySdk



full docs here https://thanakijwanavit.github.io/villa-inventory-sdk/

## Install

`pip install villaInventorySdk`

## How to use

Uploading a large amount of data

## sample input

```python
from villaInventorySdk.inventory import InventorySdk
from random import randrange
import boto3, time, json
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime
import pandas as pd
from nicHelper.dictUtil import printDict
```

```python
sampleInput =  [ 
  { 'cprcode': '0000009', 'brcode': '1000', 'ib_cf_qty': '50', 'new_ib_vs_stock_cv': '27' },
  { 'cprcode': '0000004', 'brcode': '1000', 'ib_cf_qty': '35', 'new_ib_vs_stock_cv': '33' },
  { 'cprcode': '0000003', 'brcode': '1003', 'ib_cf_qty': '36', 'new_ib_vs_stock_cv': '33' }
    ]
df = pd.DataFrame(sampleInput)
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cprcode</th>
      <th>brcode</th>
      <th>ib_cf_qty</th>
      <th>new_ib_vs_stock_cv</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0000009</td>
      <td>1000</td>
      <td>50</td>
      <td>27</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0000004</td>
      <td>1000</td>
      <td>35</td>
      <td>33</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0000003</td>
      <td>1003</td>
      <td>36</td>
      <td>33</td>
    </tr>
  </tbody>
</table>
</div>



## Upload data

## init sdk

```python
%%time
USER=None
PW = None
sdk = InventorySdk(user=USER, pw=PW, branchName = branch)
```

    CPU times: user 33.2 ms, sys: 6.92 ms, total: 40.1 ms
    Wall time: 39.2 ms


## Update inventory 

```python
%%time
key = 'test'
r = sdk.uploadDf(df, key = key)
if r.status_code >= 400: raise Exception(r.json())
sdk.ingestData(key = key)
```

    signed url is 
    url : https://in
    fields
     key : test
     AWSAccessKeyId : ASIAVX4Z5T
     x-amz-security-token : IQoJb3JpZ2
     policy : eyJleHBpcm
     signature : bx6qL+1QUg
    CPU times: user 61 ms, sys: 0 ns, total: 61 ms
    Wall time: 520 ms





    {'body': '{}',
     'statusCode': 200,
     'headers': {'Access-Control-Allow-Headers': '*',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': '*'}}



## Query single product

```python
%%time
sdk.querySingleProduct2(cprcode='1234')
```

    succesfully get url, returning pandas
    CPU times: user 19.8 ms, sys: 0 ns, total: 19.8 ms
    Wall time: 332 ms





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cprcode</th>
      <th>brcode</th>
      <th>ib_cf_qty</th>
      <th>new_ib_vs_stock_cv</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1234</td>
      <td>test</td>
      <td>123</td>
      <td>123</td>
    </tr>
  </tbody>
</table>
</div>



## Query Branch

```python
%%time
sdk.branchQuery(brcode='1000', cprcodes = ['0000009'])
```

    CPU times: user 16.5 ms, sys: 70 µs, total: 16.6 ms
    Wall time: 225 ms





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cprcode</th>
      <th>brcode</th>
      <th>ib_cf_qty</th>
      <th>new_ib_vs_stock_cv</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0000009</td>
      <td>1000</td>
      <td>50</td>
      <td>27</td>
    </tr>
  </tbody>
</table>
</div>



## Query All

```python
%%time
sdk.queryAll2()
```

    succesfully get url, returning pandas
    CPU times: user 13.6 ms, sys: 3.08 ms, total: 16.7 ms
    Wall time: 323 ms





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cprcode</th>
      <th>brcode</th>
      <th>ib_cf_qty</th>
      <th>new_ib_vs_stock_cv</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1234</td>
      <td>test</td>
      <td>123</td>
      <td>123</td>
    </tr>
    <tr>
      <th>1</th>
      <td>12345</td>
      <td>test</td>
      <td>345</td>
      <td>345</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0000009</td>
      <td>1000</td>
      <td>50</td>
      <td>27</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0000004</td>
      <td>1000</td>
      <td>35</td>
      <td>33</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0000003</td>
      <td>1003</td>
      <td>36</td>
      <td>33</td>
    </tr>
  </tbody>
</table>
</div>


