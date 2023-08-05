# AUTOGENERATED! DO NOT EDIT! File to edit: inventory.ipynb (unless otherwise specified).

__all__ = ['union', 'Endpoints', 'InventorySdk', 'uploadDf']

# Cell
from json.decoder import JSONDecodeError
from botocore.config import Config
from s3bz.s3bz import S3, Requests
from lambdasdk.lambdasdk import Lambda
from awsSchema.apigateway import Event, Response
import pandas as pd
from nicHelper.wrappers import add_class_method, add_method
from nicHelper.dictUtil import printDict
from io import BytesIO
import bz2, json, boto3, base64, logging, itertools , requests

# Cell
def union(*dicts):
    return dict(itertools.chain.from_iterable(dct.items() for dct in dicts))
class Endpoints:
  '''get endpoint names from branch name'''
  def __init__(self, branchName='manual-dev'):
    self.branchName = branchName
  updateWithS3 = lambda self: f'update-inventory-s3-{self.branchName}'
  inputS3 = lambda self: f'input-bucket-{self.branchName}'
  querySingleProduct = lambda self: f'single-product-query-inventory-{self.branchName}'
  queryAll = lambda self: f'query-all-inventory-{self.branchName}'
  queryBranch = lambda self: f'query-branch-inventory-{self.branchName}'
  queryAll2 = lambda self: f'query-all-inventory2-{self.branchName}'


class InventorySdk:
  ''' interact with villa inventory database '''
  def __init__(self, branchName = 'dev', user = None, pw = None,
               region = 'ap-southeast-1'):
    self.branchName = branchName
    self.lambdaClient = Lambda(user =user, pw=pw, region = region)
    self.user = user; self.pw = pw; self.region = region
    self.endpoint = Endpoints(branchName=branchName)


  def updateWithS3(self, data:dict,
                   key:str = 'allProducts',
                   invocationType:str = 'Event'):

    # save to s3
    S3.save(key = key,
            objectToSave = data ,
            bucket = self.endpoint.inputS3(),
            user=self.user, pw=self.pw)
    logging.info(f'saving to s3 completed')

    lambdaPayload = {
        'inputBucketName': self.endpoint.inputS3(),
        'inputKeyName': key
    }
    logging.info(f'input to lambda is {lambdaPayload}')
    try:
      result = self.lambdaClient.invoke(functionName= self.endpoint.updateWithS3()
                                        ,input=lambdaPayload,
                                        invocationType= invocationType )
      if result: return Response.getReturn(result)
    except JSONDecodeError:
      logging.warning('no return from function')
      return True

  def querySingleProduct(self, ib_prcode= None, functionName=None,
                         user=None, pw=None):
    '''query a single product'''
    functionName = functionName or self.endpoint.querySingleProduct()
    input = { "body": json.dumps({'ib_prcode': ib_prcode })}
    response =  self.lambdaClient.invoke(
        functionName = functionName, input = input )
    try:
      inventory = json.loads(Response.from_dict(response).body)
      return {k:union(v,{'ib_prcode':ib_prcode,'ib_brcode':k}) \
              if k.isdigit() else v for k,v in inventory.items()}
    except:
      return response

  def queryAll(self, functionName = None):
    '''get the whole database'''
    functionName = functionName or self.endpoint.queryAll()
    response =  self.lambdaClient.invoke(
        functionName = functionName, input = {} )
    responseBody = json.loads(Response.from_dict(response).body)
    ### return body
    if 'url' in responseBody:
      inventory =  Requests.getContentFromUrl(responseBody['url'])
      return {k:{k2: union(v2, {'ib_prcode':k,'ib_brcode': k2}) if k2.isdigit()
    else v2 for k2,v2 in v.items()} if k.isdigit() else v for k,v in inventory.items()}
#       return {k:{k2: union(json.loads(v2), {'ib_prcode':k,'ib_brcode': k2})for k2,v2 in v.items()} for k,v in inventory.items()}
    else :
      logging.error(responseBody)
      return responseBody

  def queryBranch(self, branch = '1000', functionName = None):
    '''get the branch database'''
    functionName = functionName or self.endpoint.queryBranch()
    response =  self.lambdaClient.invoke(
        functionName = functionName, input = {'body':json.dumps({'branch':branch})} )
    responseBody = json.loads(Response.from_dict(response).body)
    ### return body
    if 'url' in responseBody:
      inventory = Requests.getContentFromUrl(responseBody['url'])
      return {k:union(v,{'ib_prcode':k,'ib_brcode':branch}) for k,v in inventory.items()}
    else :
      logging.error(responseBody)
      return responseBody

# Cell
@add_method(InventorySdk)
def uploadDf(self, df:pd.DataFrame, key:str ='1000', invApi:str = '2y9nzxkuyk')->bin:
  def getPresignedUrl(invApi = invApi, key = key):
    url = f'https://{invApi}.execute-api.ap-southeast-1.amazonaws.com/Prod/presign'
    r:requests.Response = requests.post(url, json = { "key": key } )
    return r.json()
  def dfToByte(df:pd.DataFrame):
    tempIo = BytesIO()
    inputByte = df.to_feather(tempIo)
    return tempIo.getvalue()
  def uploadFile(inputByte:bin, key=key):
    presigned = getPresignedUrl(key=key)
    print('signed url is ')
    printDict(presigned)
    files = {'file': (key , BytesIO(inputByte))}
    r = requests.post(url = presigned['url'], data = presigned['fields'] , files = files)
    return r

  ##### main
  inputByte = dfToByte(df)
  r = uploadFile(inputByte, key = key)
  return r