from rasa.core.policies import FallbackPolicy
from recipe import DefaultV1Recipe

@DefaultV1Recipe.register(FallbackPolicy)
class MyFallbackPolicy(FallbackPolicy):
    pass