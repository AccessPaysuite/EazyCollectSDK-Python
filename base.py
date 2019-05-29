from __future__ import unicode_literals
from __future__ import absolute_import
from get import Get
from post import Post
from patch import Patch
import settings

class EazyAPI:
    """
    Creates a new instance of the EazyAPI
    """
    def __init__(self):
        self.get = Get()
        self.post = Post()
        self.patch = Patch()