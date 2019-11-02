from schematics import Model
from schematics.types import ListType, StringType


class Citation(Model):
    
    _id = StringType(serialize_when_none=False)
    content = StringType()
    keywords = ListType(StringType)
