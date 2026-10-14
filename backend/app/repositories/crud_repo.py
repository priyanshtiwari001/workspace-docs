from sqlalchemy.sql import selectable
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any,Sequence


class CrudRepository:
    def __init__(self, model, db: AsyncSession):
        self.model = model
        self.db = db

    async def create(self, new_record: Any):
        self.db.add(new_record)
        await self.db.flush()
        return new_record

    async def get_all(self,options:Sequence | None,populate_existing:bool | None = None):
        smt = select(self.model)
        if options:
            smt = smt.options(*options).execution_options(populate_existing=populate_existing)
        res = await self.db.execute(smt)
        return res.scalars().all()

    async def get(self, record_id: int, options: Sequence | None = None,populate_existing:bool | None = None):
        smt = select(self.model).where(self.model.id == record_id)

        if options:
            smt = smt.options(*options).execution_options(populate_existing=populate_existing)
            # smt = smt.options(*options)
        result = await self.db.execute(smt)
        return result.scalar_one_or_none()

    async def update(self, record_id: int, data: dict):
        record = await self.db.get(self.model, record_id)
        if not record:
            raise Exception(f"No {self.model.__name__} found with this id {record_id}")
        print("Data",data)
        for key, value in data.items():
            if hasattr(record, key):
                setattr(record, key, value)
        self.db.add(record)
        await self.db.flush()
        return record

    async def delete(self, record_id: int):
        await self.db.execute(delete(self.model).where(self.model.id == record_id))
        await self.db.flush()
        return {"message": "Record deleted successfully."}
