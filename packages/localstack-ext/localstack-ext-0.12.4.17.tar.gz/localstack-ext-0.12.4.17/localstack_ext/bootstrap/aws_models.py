from localstack.utils.aws import aws_models
QNYzq=super
QNYzP=None
QNYzJ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  QNYzq(LambdaLayer,self).__init__(arn)
  self.cwd=QNYzP
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.QNYzJ.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,QNYzJ,env=QNYzP):
  QNYzq(RDSDatabase,self).__init__(QNYzJ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,QNYzJ,env=QNYzP):
  QNYzq(RDSCluster,self).__init__(QNYzJ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,QNYzJ,env=QNYzP):
  QNYzq(AppSyncAPI,self).__init__(QNYzJ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,QNYzJ,env=QNYzP):
  QNYzq(AmplifyApp,self).__init__(QNYzJ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,QNYzJ,env=QNYzP):
  QNYzq(ElastiCacheCluster,self).__init__(QNYzJ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,QNYzJ,env=QNYzP):
  QNYzq(TransferServer,self).__init__(QNYzJ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,QNYzJ,env=QNYzP):
  QNYzq(CloudFrontDistribution,self).__init__(QNYzJ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,QNYzJ,env=QNYzP):
  QNYzq(CodeCommitRepository,self).__init__(QNYzJ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
