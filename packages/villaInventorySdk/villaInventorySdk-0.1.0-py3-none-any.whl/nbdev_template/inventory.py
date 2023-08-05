# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['S3', 'InventorySdk']

# Cell
class S3:
  @staticmethod
  def s3(region = 'ap-southeast-1', user = None, pw = None):
    '''
    create and return s3 client
    '''
    config = Config(s3={"use_accelerate_endpoint": True,
                        "addressing_style": "virtual"})
    s3 = boto3.client(
        's3',
        aws_access_key_id= user,
        aws_secret_access_key= pw,
        region_name = region,
        config = config
      )
    return s3
  @classmethod
  def save(cls,  key, objectToSave, bucket = '', user=None, pw=None):
    '''
    save an object to s3
    '''
    s3 = cls.s3(user=user, pw=pw)
    compressedData = bz2.compress(json.dumps(objectToSave).encode())
    result = s3.put_object(Body=compressedData, Bucket=bucket, Key=key)
    success = result['ResponseMetadata']['HTTPStatusCode'] ==  200
    print('data was saved to s3')
    if not success: raise Error(success)
    else: return True
  @classmethod
  def exist(cls, key, bucket):
    return 'Contents' in cls.s3().list_objects(
        Bucket=bucket , Prefix=key )
  @classmethod
  def load(cls, key, bucket=''):
    if not cls.exist(key, bucket):
      return {}
    s3 = cls.s3()
    requestResult =  s3.get_object(
                  Bucket = bucket,
                  Key = key
                )
    allItemsByte = next(requestResult.get('Body',None))
    if not allItemsByte: raise ValueError('all data does not exist in the database')
    allItems = json.loads(bz2.decompress(allItemsByte).decode())
    return allItems

  @classmethod
  def presign(cls, key, expiry = 1000, bucket = ''):
    if not cls.checkIfExist(key,bucket=bucket): return 'object doesnt exist'
    s3 = cls.s3()
    result = s3.generate_presigned_url(
        'get_object',
          Params={'Bucket': bucket,
                  'Key': key},
        ExpiresIn=expiry)
    return result

  @classmethod
  def checkIfExist(cls, key, bucket = ''):
    results = cls.s3().list_objects(Bucket=bucket , Prefix= key)
    return 'Contents' in results

# Cell
class InventorySdk:
  class Lambda:
    '''
      for invoking lambda functions
    '''
    def __init__(self, user=None, pw=None, region = 'ap-southeast-1'):
      self.lambdaClient = boto3.client(
          'lambda',
          aws_access_key_id=user,
          aws_secret_access_key=pw,
          region_name = region
        )
    def invoke(self, functionName, input, invocationType= 'RequestResponse'):
      return self.lambdaClient.invoke(
        FunctionName = functionName,
        InvocationType= invocationType,
        LogType='Tail',
        ClientContext= base64.b64encode(json.dumps({'caller': 'sdk'}).encode()).decode(),
        Payload= json.dumps(input)
      )
  class S3:
    '''
      for uploading and downloading files from s3
    '''

    def __init__(self, user=None, pw = None, region = 'ap-southeast-1'):
      '''
      create and return s3 client
      '''
      config = Config(s3={"use_accelerate_endpoint": True,
                          "addressing_style": "virtual"})
      self.s3 = boto3.client(
          's3',
          aws_access_key_id= user,
          aws_secret_access_key= pw,
          region_name = region,
          config = config
        )

    @classmethod
    def save(cls,  key, objectToSave, bucket):
      '''
      save an object to s3
      '''
      compressedData = bz2.compress(json.dumps(objectToSave).encode())
      result = self.s3.put_object(Body=compressedData, Bucket=bucket, Key=key)
      success = result['ResponseMetadata']['HTTPStatusCode'] ==  200
      if not success: raise Error(success)
      else: return True

  class Requests:
    '''
      for uploading and downloading contents from url
    '''
    @staticmethod
    def getContentFromUrl( url):
      result = requests.get(url)
      if not result.ok:
        print('error downloading')
        return result.content
      content = result.content
      decompressedContent = bz2.decompress(content)
      contentDict = json.loads(decompressedContent)
      return contentDict

  def __init__(self, stackName = 'dev', user = None, pw = None, region = 'ap-southeast-1'):
    self.stackName = stackName
    self.lambdaClient = self.Lambda(user =user, pw=pw, region = region)
    self.s3 = self.S3(user =user, pw = pw, region = region)
    self.user = user
    self.pw = pw
  def update(self, data):
    '''
      for updating the database with a large amount of data
    '''
    self.s3.upload(data)
  def updateWithS3(self, data,
                   inputKeyName = 'input-data-name',
                   inputBucketName = 'input-bucket-name',
                   functionName='update-inventory-s3-dev-manual',
                   user= None,
                   pw= None,
                   invocationType = 'Event'):
    if not user and not pw:
      user = self.user
      pw = self.pw
    S3.save(inputKeyName, data , bucket = inputBucketName,
            user=user, pw=pw)
    print(f'data is saved to s3, invoking ingestion function')
    input = {
        'inputBucketName': inputBucketName,
        'inputKeyName': inputKeyName
    }
    print(f'input to lambda is {input}')
    return self.lambdaClient.invoke(functionName= functionName ,input=input,
                                    invocationType= invocationType )
