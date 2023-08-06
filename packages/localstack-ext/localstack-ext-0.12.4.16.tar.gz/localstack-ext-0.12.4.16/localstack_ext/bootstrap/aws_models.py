from localstack.utils.aws import aws_models
xLWfb=super
xLWfF=None
xLWfr=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  xLWfb(LambdaLayer,self).__init__(arn)
  self.cwd=xLWfF
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.xLWfr.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,xLWfr,env=xLWfF):
  xLWfb(RDSDatabase,self).__init__(xLWfr,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,xLWfr,env=xLWfF):
  xLWfb(RDSCluster,self).__init__(xLWfr,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,xLWfr,env=xLWfF):
  xLWfb(AppSyncAPI,self).__init__(xLWfr,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,xLWfr,env=xLWfF):
  xLWfb(AmplifyApp,self).__init__(xLWfr,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,xLWfr,env=xLWfF):
  xLWfb(ElastiCacheCluster,self).__init__(xLWfr,env=env)
class TransferServer(BaseComponent):
 def __init__(self,xLWfr,env=xLWfF):
  xLWfb(TransferServer,self).__init__(xLWfr,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,xLWfr,env=xLWfF):
  xLWfb(CloudFrontDistribution,self).__init__(xLWfr,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,xLWfr,env=xLWfF):
  xLWfb(CodeCommitRepository,self).__init__(xLWfr,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
