from localstack.utils.aws import aws_models
bKpNS=super
bKpNH=None
bKpNB=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  bKpNS(LambdaLayer,self).__init__(arn)
  self.cwd=bKpNH
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.bKpNB.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,bKpNB,env=bKpNH):
  bKpNS(RDSDatabase,self).__init__(bKpNB,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,bKpNB,env=bKpNH):
  bKpNS(RDSCluster,self).__init__(bKpNB,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,bKpNB,env=bKpNH):
  bKpNS(AppSyncAPI,self).__init__(bKpNB,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,bKpNB,env=bKpNH):
  bKpNS(AmplifyApp,self).__init__(bKpNB,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,bKpNB,env=bKpNH):
  bKpNS(ElastiCacheCluster,self).__init__(bKpNB,env=env)
class TransferServer(BaseComponent):
 def __init__(self,bKpNB,env=bKpNH):
  bKpNS(TransferServer,self).__init__(bKpNB,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,bKpNB,env=bKpNH):
  bKpNS(CloudFrontDistribution,self).__init__(bKpNB,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,bKpNB,env=bKpNH):
  bKpNS(CodeCommitRepository,self).__init__(bKpNB,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
