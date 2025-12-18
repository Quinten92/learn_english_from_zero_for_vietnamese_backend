from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
def read_items():
    return [{"name": "Item Foo"}, {"name": "Item Bar"}]

@router.get("/hello")
def read_hello():
    return {"message": "Hello from learnenglishzero API!"}
