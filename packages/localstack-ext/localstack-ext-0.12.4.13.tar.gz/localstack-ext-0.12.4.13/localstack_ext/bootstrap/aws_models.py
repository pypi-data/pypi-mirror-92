from localstack.utils.aws import aws_models
GsPih=super
GsPix=None
GsPiT=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  GsPih(LambdaLayer,self).__init__(arn)
  self.cwd=GsPix
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.GsPiT.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,GsPiT,env=GsPix):
  GsPih(RDSDatabase,self).__init__(GsPiT,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,GsPiT,env=GsPix):
  GsPih(RDSCluster,self).__init__(GsPiT,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,GsPiT,env=GsPix):
  GsPih(AppSyncAPI,self).__init__(GsPiT,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,GsPiT,env=GsPix):
  GsPih(AmplifyApp,self).__init__(GsPiT,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,GsPiT,env=GsPix):
  GsPih(ElastiCacheCluster,self).__init__(GsPiT,env=env)
class TransferServer(BaseComponent):
 def __init__(self,GsPiT,env=GsPix):
  GsPih(TransferServer,self).__init__(GsPiT,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,GsPiT,env=GsPix):
  GsPih(CloudFrontDistribution,self).__init__(GsPiT,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,GsPiT,env=GsPix):
  GsPih(CodeCommitRepository,self).__init__(GsPiT,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
