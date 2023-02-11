from fastapi import APIRouter, Query, Body, Path
from pydantic import BaseModel
from typing import Optional, List, Dict

router = APIRouter(
    prefix='/blog',
    tags=['blog']
)


class Image(BaseModel):
    url: str
    alias: Optional[str]


class BlogModel(BaseModel):
    title: str
    content: str
    nb_comments: int
    published: Optional[bool]
    tags: List[str] = []
    metadata: Dict[str, str] = {'key1': 'val1'}
    image: Optional[Image] = None


@router.post('/new/{id}')
def create_blog(id: int, blog: BlogModel, version: int = 1):
    return {
        'id': id,
        'data': blog,
        'version': version
    }


@router.post('/new/{id}/comment/{comment_id}')
def create_comment(
        blog: BlogModel,
        id: int,
        comment_title: str = Query(
            None,
            title="Title of comment",
            description="Some description for comment title",
            alias='commentTitle',
            deprecated=False
        ),
        content: str = Body(
            ...,
            min_length=10,
            max_length=5000,
            regex='^[a-z\s]*$'
        ),
        comment_id: int = Path(None, gt=5, le=10),
        v: Optional[List[str]] = Query(['1.0', '1.1', '1.2'])
):
    return {
        'blog': blog,
        "id": id,
        "comment_id": comment_id,
        'comment_title': comment_title,
        'content': content,
        "version": v
    }


def required_functionality():
    return {'message': 'Learning Fast API is important'}
