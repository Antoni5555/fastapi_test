from sqlalchemy import select
from database import TaskOrm, new_session
from shemas import STask, STaskAdd


class TaskRepository:
    @classmethod
    async def add_one(cls, task: STaskAdd) -> int:
        async with new_session() as session:
            data = task.model_dump()
            new_task = TaskOrm(**data)
            session.add(new_task)
            await session.flush()
            await session.commit()
            return new_task.id

    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_shemas = [STask.model_validate(task_model) for task_model in task_models]
            return task_shemas