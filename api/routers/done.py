from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import api.schemas.done as done_schema
import api.cruds.done as done_crud
from api.db import get_db
import api.cruds.task as task_crud

router = APIRouter()

@router.put("/tasks/{task_id}/done", response_model=done_schema.DoneResponse)
async def mark_task_as_done(task_id: int, db: AsyncSession = Depends(get_db)):
  done = await done_crud.get_done(db, task_id)
  if done is not None:
    raise HTTPException(status_code=400, detail="Done already exists")
  return await done_crud.create_done(db, task_id)

@router.delete("/tasks/{task_id}/done", response_model=None)
async def unmark_task_as_done(task_id: int, db: AsyncSession = Depends(get_db)):
  done = await done_crud.get_done(db, task_id)
  if done is None:
    raise HTTPException(status_code=404, detail="Done not found")
  return await done_crud.delete_done(db, original=done)

@router.get("/tasks/{task_id}/done")
async def get_done(task_id: int, db: AsyncSession = Depends(get_db)):
    # Doneテーブルに該当IDがあるか確認
    result = await db.execute(
        select(task_crud.task_model.Done).filter(task_crud.task_model.Done.id == task_id)
    )
    done = result.scalar()
    if done:
        return {"done": True}
    else:
        raise HTTPException(status_code=404, detail="Not found")
