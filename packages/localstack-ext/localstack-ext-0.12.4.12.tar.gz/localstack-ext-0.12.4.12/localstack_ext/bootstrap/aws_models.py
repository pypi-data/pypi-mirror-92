from localstack.utils.aws import aws_models
dhtMH=super
dhtMg=None
dhtMF=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  dhtMH(LambdaLayer,self).__init__(arn)
  self.cwd=dhtMg
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.dhtMF.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,dhtMF,env=dhtMg):
  dhtMH(RDSDatabase,self).__init__(dhtMF,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,dhtMF,env=dhtMg):
  dhtMH(RDSCluster,self).__init__(dhtMF,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,dhtMF,env=dhtMg):
  dhtMH(AppSyncAPI,self).__init__(dhtMF,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,dhtMF,env=dhtMg):
  dhtMH(AmplifyApp,self).__init__(dhtMF,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,dhtMF,env=dhtMg):
  dhtMH(ElastiCacheCluster,self).__init__(dhtMF,env=env)
class TransferServer(BaseComponent):
 def __init__(self,dhtMF,env=dhtMg):
  dhtMH(TransferServer,self).__init__(dhtMF,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,dhtMF,env=dhtMg):
  dhtMH(CloudFrontDistribution,self).__init__(dhtMF,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,dhtMF,env=dhtMg):
  dhtMH(CodeCommitRepository,self).__init__(dhtMF,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
