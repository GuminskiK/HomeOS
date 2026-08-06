from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from AD_Files.app.core.exceptions import PoolWithInvalidMountPrefixException
from common.CurrentUserContext import CurrentUserContext
from app.schemas.files import StoragePoolCreate, StoragePoolRead
from AD_Files.app.models.StoragePool import StoragePool

async def list_pools(
    session: AsyncSession,
    user: CurrentUserContext
):
    statement = select(StoragePool).where(StoragePool.is_active == True)
    results = await session.exec(statement)
    return results.all()

async def create_pool(
    pool_in: StoragePoolCreate,
    session: AsyncSession,
    user: CurrentUserContext
):
    existing = await session.exec(select(StoragePool).where(StoragePool.mount_prefix == pool_in.mount_prefix))
    if existing.first():
        raise PoolWithInvalidMountPrefixException()

    db_pool = StoragePool(**pool_in.model_dump())
    session.add(db_pool)
    await session.commit()
    await session.refresh(db_pool)
    return db_pool