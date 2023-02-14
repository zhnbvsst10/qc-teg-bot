import asyncio
import logging
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from handlers import common, pvc_1, pvc_3


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    token = '6029120908:AAFSntMGALPmIV7eJPrLbPxXEk_pEEdTRgQ'
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(token=token)

    dp.include_router(common.router)
    dp.include_router(pvc_1.router)
    dp.include_router(pvc_3.router2)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())