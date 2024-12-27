from aiogram import Router
from .start import start_router
from .review_dialog import review_router
from .other_massages import echo_router

private_router = Router()


private_router.include_router(start_router)
private_router.include_router(review_router)
private_router.include_router(echo_router)
