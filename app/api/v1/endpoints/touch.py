from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

@router.get("/")
def _touch():
    return {"hello": "world"}

