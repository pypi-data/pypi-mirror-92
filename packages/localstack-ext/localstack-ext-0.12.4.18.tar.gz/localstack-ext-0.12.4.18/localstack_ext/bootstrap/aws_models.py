from localstack.utils.aws import aws_models
ksRQK=super
ksRQP=None
ksRQw=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  ksRQK(LambdaLayer,self).__init__(arn)
  self.cwd=ksRQP
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.ksRQw.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,ksRQw,env=ksRQP):
  ksRQK(RDSDatabase,self).__init__(ksRQw,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,ksRQw,env=ksRQP):
  ksRQK(RDSCluster,self).__init__(ksRQw,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,ksRQw,env=ksRQP):
  ksRQK(AppSyncAPI,self).__init__(ksRQw,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,ksRQw,env=ksRQP):
  ksRQK(AmplifyApp,self).__init__(ksRQw,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,ksRQw,env=ksRQP):
  ksRQK(ElastiCacheCluster,self).__init__(ksRQw,env=env)
class TransferServer(BaseComponent):
 def __init__(self,ksRQw,env=ksRQP):
  ksRQK(TransferServer,self).__init__(ksRQw,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,ksRQw,env=ksRQP):
  ksRQK(CloudFrontDistribution,self).__init__(ksRQw,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,ksRQw,env=ksRQP):
  ksRQK(CodeCommitRepository,self).__init__(ksRQw,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
