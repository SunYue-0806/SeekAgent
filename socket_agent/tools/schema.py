from typing import Union, Dict, Any, Type

from pydantic import BaseModel


class ToolInfo(BaseModel):
    name: str
    type: str
    description: str
    arguments: Union[Dict[str, Any], Type[BaseModel]]
