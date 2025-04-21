from fastapi import APIRouter, HTTPException, Depends


router = APIRouter(
    prefix="/",
    tags=["auth"],
)

