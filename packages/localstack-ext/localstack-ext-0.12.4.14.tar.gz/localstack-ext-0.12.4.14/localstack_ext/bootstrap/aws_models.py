from localstack.utils.aws import aws_models
TbzID=super
TbzIn=None
TbzIS=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  TbzID(LambdaLayer,self).__init__(arn)
  self.cwd=TbzIn
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.TbzIS.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,TbzIS,env=TbzIn):
  TbzID(RDSDatabase,self).__init__(TbzIS,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,TbzIS,env=TbzIn):
  TbzID(RDSCluster,self).__init__(TbzIS,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,TbzIS,env=TbzIn):
  TbzID(AppSyncAPI,self).__init__(TbzIS,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,TbzIS,env=TbzIn):
  TbzID(AmplifyApp,self).__init__(TbzIS,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,TbzIS,env=TbzIn):
  TbzID(ElastiCacheCluster,self).__init__(TbzIS,env=env)
class TransferServer(BaseComponent):
 def __init__(self,TbzIS,env=TbzIn):
  TbzID(TransferServer,self).__init__(TbzIS,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,TbzIS,env=TbzIn):
  TbzID(CloudFrontDistribution,self).__init__(TbzIS,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,TbzIS,env=TbzIn):
  TbzID(CodeCommitRepository,self).__init__(TbzIS,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
