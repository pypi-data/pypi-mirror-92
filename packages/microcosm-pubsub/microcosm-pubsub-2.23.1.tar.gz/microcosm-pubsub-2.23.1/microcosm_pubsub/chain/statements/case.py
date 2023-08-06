"""
case("value").then(...)

"""
from microcosm_pubsub.chain import Chain


class CaseStatement:
    def __init__(self, switch, key):
        self.switch = switch
        self.key = key

    def then(self, *args, **kwargs):
        self.switch._add_action_for_key(self.key, Chain.make(*args, **kwargs))
        return self.switch
