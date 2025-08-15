"""
Bot Loader - Complete Implementation

This module sets up the Telegram bot with environment variables
and role-based routing system.
"""

import os
import asyncio
import traceback
import sys
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import settings
from config import get_admin_regions

# Logger sozlash - batafsil
logging.basicConfig(
    level=settings.numeric_log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Terminal uchun
        logging.FileHandler('testbot_errors.log', encoding='utf-8'),  # Xatoliklar uchun
        logging.FileHandler('testbot_activity.log', encoding='utf-8')  # Faollik uchun
    ]
)
logger = logging.getLogger(__name__)

# Qo'shimcha logger'lar
activity_logger = logging.getLogger('activity')
activity_logger.setLevel(settings.numeric_log_level)
activity_handler = logging.FileHandler('testbot_activity.log', encoding='utf-8')
activity_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
activity_handler.setFormatter(activity_formatter)
activity_logger.addHandler(activity_handler)

# Ensure env is loaded (idempotent) and apply configured logging level
load_dotenv()
logging.getLogger().setLevel(settings.numeric_log_level)
logger.setLevel(settings.numeric_log_level)
activity_logger.setLevel(settings.numeric_log_level)

# Bot configuration (from centralized settings)
BOT_TOKEN = settings.bot_token
ADMIN_IDS = settings.admin_ids
BOT_ID = settings.bot_id
ZAYAVKA_GROUP_ID = settings.zayavka_group_id

# Database configuration (for future use)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 5432))
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'alfaconnect_db')

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Middleware'larni qo'shish
from middlewares.logger_middleware import LoggerMiddleware
from middlewares.error_middleware import ErrorMiddleware

dp.message.middleware(LoggerMiddleware())
dp.callback_query.middleware(LoggerMiddleware())
dp.message.middleware(ErrorMiddleware())
dp.callback_query.middleware(ErrorMiddleware())

async def get_user_role(user_id: int) -> str:
    """Get user role based on database records and admin list.

    A user is considered admin if they are either in global ADMIN_IDS or in any
    region-specific admin list (ADMIN_IDS_<REGION>) defined in the environment.
    """
    try:
        # Global admin or region-scoped admin
        if user_id in ADMIN_IDS:
            return 'admin'
        if get_admin_regions(user_id):
            return 'admin'

        # Try database lookup
        try:
            from utils.user_repository import get_user_role as repo_get_user_role
            role = await repo_get_user_role(user_id)
            if role:
                return role
        except Exception as db_err:
            logger.debug(f"DB role lookup failed for {user_id}: {db_err}")

        # Default role
        return 'client'
    except Exception:
        return 'client'

# Global bot instance for use in handlers
def get_bot():
    return bot

def get_dp():
    return dp

async def setup_bot():
    """Setup bot with all handlers"""
    try:
        # Initialize DB pools (default, clients, regions)
        try:
            from utils.db import init_db_pools
            await init_db_pools()
        except Exception as e:
            logger.warning(f"DB pools init skipped/failed: {e}")

        # Import and setup handlers
        from handlers import setup_handlers
        setup_handlers(dp)
        
        print("✅ Bot setup completed successfully")
        print(f"🤖 Bot ID: {BOT_ID}")
        print(f"👥 Admin IDs: {ADMIN_IDS}")
        print(f"📣 Zayavka group: {ZAYAVKA_GROUP_ID}")
        
    except ImportError as e:
        logger.error(f"Import Error in setup_bot: {e}", exc_info=True)
        print(f"❌ Import Error in setup_bot: {e}")
        print(f"📁 Error location: {e.__traceback__.tb_frame.f_code.co_filename}")
        print(f"🔍 Line number: {e.__traceback__.tb_lineno}")
        traceback.print_exc()
        raise
    except NameError as e:
        logger.error(f"Name Error in setup_bot: {e}", exc_info=True)
        print(f"❌ Name Error in setup_bot: {e}")
        print(f"📁 Error location: {e.__traceback__.tb_frame.f_code.co_filename}")
        print(f"🔍 Line number: {e.__traceback__.tb_lineno}")
        traceback.print_exc()
        raise
    except Exception as e:
        logger.error(f"Error setting up bot: {e}", exc_info=True)
        print(f"❌ Error setting up bot: {e}")
        print(f"📁 Error type: {type(e).__name__}")
        print(f"🔍 Error location: {e.__traceback__.tb_frame.f_code.co_filename}")
        print(f"📄 Line number: {e.__traceback__.tb_lineno}")
        traceback.print_exc()
        raise

async def start_bot():
    """Start the bot"""
    try:
        await setup_bot()
        print("🚀 Starting bot...")
        await dp.start_polling(bot)
    except ImportError as e:
        logger.error(f"Import Error in start_bot: {e}", exc_info=True)
        print(f"❌ Import Error in start_bot: {e}")
        print(f"📁 Error location: {e.__traceback__.tb_frame.f_code.co_filename}")
        print(f"🔍 Line number: {e.__traceback__.tb_lineno}")
        traceback.print_exc()
        raise
    except NameError as e:
        logger.error(f"Name Error in start_bot: {e}", exc_info=True)
        print(f"❌ Name Error in start_bot: {e}")
        print(f"📁 Error location: {e.__traceback__.tb_frame.f_code.co_filename}")
        print(f"🔍 Line number: {e.__traceback__.tb_lineno}")
        traceback.print_exc()
        raise
    except Exception as e:
        logger.error(f"Error starting bot: {e}", exc_info=True)
        print(f"❌ Error starting bot: {e}")
        print(f"📁 Error type: {type(e).__name__}")
        print(f"🔍 Error location: {e.__traceback__.tb_frame.f_code.co_filename}")
        print(f"📄 Line number: {e.__traceback__.tb_lineno}")
        traceback.print_exc()
        raise

if __name__ == "__main__":
    asyncio.run(start_bot())
