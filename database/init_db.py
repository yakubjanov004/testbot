"""
Database Initialization Script

This script initializes the database, creates tables, and optionally seeds with sample data.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
import logging

from database.base import Base, init_db, engine
from database.models import User, UserRole
from database.crud import UserCRUD
from database.base import async_session_maker

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_tables():
    """Create all database tables"""
    try:
        logger.info("Creating database tables...")
        async with engine.begin() as conn:
            # Drop all tables (for development only)
            if os.getenv('DROP_TABLES', 'false').lower() == 'true':
                logger.warning("Dropping existing tables...")
                await conn.run_sync(Base.metadata.drop_all)
            
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")
        raise


async def seed_users():
    """Seed initial users for testing"""
    try:
        async with async_session_maker() as db:
            logger.info("Seeding initial users...")
            
            # Admin user
            admin_id = int(os.getenv('ADMIN_IDS', '123456789').split(',')[0])
            admin = await UserCRUD.get_by_telegram_id(db, admin_id)
            if not admin:
                admin = await UserCRUD.create(
                    db,
                    telegram_id=admin_id,
                    username="admin",
                    full_name="System Administrator",
                    role=UserRole.ADMIN,
                    language="uz",
                    is_active=True,
                    is_verified=True
                )
                logger.info(f"Created admin user: {admin.username}")
            
            # Manager user
            manager_id = int(os.getenv('MANAGER_ID', '0')) if os.getenv('MANAGER_ID') else None
            if manager_id:
                manager = await UserCRUD.get_by_telegram_id(db, manager_id)
                if not manager:
                    manager = await UserCRUD.create(
                        db,
                        telegram_id=manager_id,
                        username="manager",
                        full_name="Manager User",
                        role=UserRole.MANAGER,
                        language="uz",
                        is_active=True,
                        is_verified=True
                    )
                    logger.info(f"Created manager user: {manager.username}")
            
            # Junior Manager user
            junior_manager_id = int(os.getenv('JUNIOR_MANAGER_ID', '0')) if os.getenv('JUNIOR_MANAGER_ID') else None
            if junior_manager_id:
                junior_manager = await UserCRUD.get_by_telegram_id(db, junior_manager_id)
                if not junior_manager:
                    junior_manager = await UserCRUD.create(
                        db,
                        telegram_id=junior_manager_id,
                        username="junior_manager",
                        full_name="Junior Manager User",
                        role=UserRole.JUNIOR_MANAGER,
                        language="uz",
                        is_active=True,
                        is_verified=True
                    )
                    logger.info(f"Created junior manager user: {junior_manager.username}")
            
            # Controller user
            controller_id = int(os.getenv('CONTROLLER_ID', '0')) if os.getenv('CONTROLLER_ID') else None
            if controller_id:
                controller = await UserCRUD.get_by_telegram_id(db, controller_id)
                if not controller:
                    controller = await UserCRUD.create(
                        db,
                        telegram_id=controller_id,
                        username="controller",
                        full_name="Controller User",
                        role=UserRole.CONTROLLER,
                        language="uz",
                        is_active=True,
                        is_verified=True
                    )
                    logger.info(f"Created controller user: {controller.username}")
            
            # Technician user
            technician_id = int(os.getenv('TECHNICIAN_ID', '0')) if os.getenv('TECHNICIAN_ID') else None
            if technician_id:
                technician = await UserCRUD.get_by_telegram_id(db, technician_id)
                if not technician:
                    technician = await UserCRUD.create(
                        db,
                        telegram_id=technician_id,
                        username="technician",
                        full_name="Technician User",
                        role=UserRole.TECHNICIAN,
                        language="uz",
                        is_active=True,
                        is_verified=True
                    )
                    logger.info(f"Created technician user: {technician.username}")
            
            # Call Center user
            call_center_id = int(os.getenv('CALL_CENTER_ID', '0')) if os.getenv('CALL_CENTER_ID') else None
            if call_center_id:
                call_center = await UserCRUD.get_by_telegram_id(db, call_center_id)
                if not call_center:
                    call_center = await UserCRUD.create(
                        db,
                        telegram_id=call_center_id,
                        username="call_center",
                        full_name="Call Center User",
                        role=UserRole.CALL_CENTER,
                        language="uz",
                        is_active=True,
                        is_verified=True
                    )
                    logger.info(f"Created call center user: {call_center.username}")
            
            # Call Center Supervisor user
            supervisor_id = int(os.getenv('CALL_CENTER_SUPERVISOR_ID', '0')) if os.getenv('CALL_CENTER_SUPERVISOR_ID') else None
            if supervisor_id:
                supervisor = await UserCRUD.get_by_telegram_id(db, supervisor_id)
                if not supervisor:
                    supervisor = await UserCRUD.create(
                        db,
                        telegram_id=supervisor_id,
                        username="call_center_supervisor",
                        full_name="Call Center Supervisor",
                        role=UserRole.CALL_CENTER_SUPERVISOR,
                        language="uz",
                        is_active=True,
                        is_verified=True
                    )
                    logger.info(f"Created call center supervisor user: {supervisor.username}")
            
            # Client user (for testing)
            client_id = int(os.getenv('CLIENT_ID', '0')) if os.getenv('CLIENT_ID') else None
            if client_id:
                client = await UserCRUD.get_by_telegram_id(db, client_id)
                if not client:
                    client = await UserCRUD.create(
                        db,
                        telegram_id=client_id,
                        username="test_client",
                        full_name="Test Client",
                        phone_number="+998901234567",
                        role=UserRole.CLIENT,
                        language="uz",
                        is_active=True,
                        is_verified=False
                    )
                    logger.info(f"Created test client user: {client.username}")
            
            logger.info("✅ Initial users seeded successfully")
            
    except Exception as e:
        logger.error(f"❌ Error seeding users: {e}")
        raise


async def main():
    """Main initialization function"""
    try:
        # Create tables
        await create_tables()
        
        # Seed initial data if requested
        if os.getenv('SEED_DATA', 'true').lower() == 'true':
            await seed_users()
        
        logger.info("✅ Database initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        sys.exit(1)
    finally:
        # Close database connections
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())