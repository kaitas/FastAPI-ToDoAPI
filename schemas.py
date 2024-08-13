from typing import List, Optional
from pydantic import BaseModel


class PostTodo(BaseModel):
    title: str
