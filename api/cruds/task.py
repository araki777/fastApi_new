from typing import List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.task as task_model
import api.schemas.task as task_schema

async def create_task(
    db: AsyncSession, task_create: task_schema.TaskCreate
) -> task_model.Task:
  task = task_model.Task(**task_create.model_dump())
  db.add(task)
  await db.commit()
  await db.refresh(task)
  return task

async def get_tasks_with_done(db: AsyncSession) -> list[task_schema.Task]:
    result: Result = await (
        db.execute(
            select(
                task_model.Task.id,
                task_model.Task.title,
                task_model.Done.id.isnot(None).label("done"),
            ).outerjoin(task_model.Done)
        )
    )
    tasks = []
    for id, title, done in result.all():
        tasks.append(task_schema.Task(id=id, title=title, done=done))
    return tasks

async def get_task(db: AsyncSession, task_id: int) -> Optional[task_model.Task]:
  result: Result = await db.execute(
    select(task_model.Task).filter(task_model.Task.id == task_id)
  )
  task: Optional[Tuple[task_model.Task]] = result.first()
  return task[0] if task is not None else None

async def update_task(
    db: AsyncSession, task_create: task_schema.TaskCreate, original: task_model.Task
) -> task_model.Task:
  original.title = task_create.title
  db.add(original)
  await db.commit()
  await db.refresh(original)
  return original

async def delete_task(db: AsyncSession, original: task_model.Task):
  await db.delete(original)
  await db.commit()