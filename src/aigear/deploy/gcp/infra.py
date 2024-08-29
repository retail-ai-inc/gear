from .function import CloudFunction
from .pub_sub import Publish, Subscriptions
from ...common.logger import logger
from .iam import check_iam
from .project import get_project_id


class Infra:
    def __init__(
        self,
        topic_name,
        function_name,
        region,
    ):
        sub_name = f"{topic_name}_sub"
        _entry_point = "helloPubSub"
        
        self.pub = Publish(topic_name)
        self.sub = Subscriptions(sub_name, topic_name)
        self.cf = CloudFunction(
            function_name,
            region,
            _entry_point,
            topic_name,
        )
    
    def create(self):
        pub_exist, sub_exist, cf_exist = self._check_infra(self.pub, self.sub, self.cf)
        if not pub_exist:
            self.pub.create()
        
        if not sub_exist:
            self.sub.create()
        
        if not cf_exist:
            self.cf.deploy()
    
    def clear(self):
        project_id = get_project_id()
        owner_pm = check_iam(project_id)
        if owner_pm:
            self.pub.delete()
            self.sub.delete()
            self.cf.delete()
        else:
            logger.info("You are not the owner and cannot delete aigear infrastructure.")
    
    @staticmethod
    def _check_infra(pub, sub, cf):
        pub_exist = pub.describe()
        if not pub_exist:
            logger.info("Pub(pubsub) not created.")
        sub_exist = sub.describe()
        if not sub_exist:
            logger.info("Sub(pubsub) not created.")
        cf_exist = cf.describe()
        if not cf_exist:
            logger.info("Cloud function not created.")
        return pub_exist, sub_exist, cf_exist
