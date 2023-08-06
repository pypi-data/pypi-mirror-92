"""
A collection of random utils
"""

__title__ = "vcoutils"
__author__ = "vcokltfre"

from .leakybucket import LeakyBucket, LeakyBucketManager
from .extrachecks import has_any_permissions, has_any_guild_permissions
from .intents import Intents
from .genid import generate_id_solid, generate_id_split