from fastapi import HTTPException
from sqlalchemy import select, update, delete, insert, and_
from src.publishers.models import PublishersModel
from src.publishers.schemas import Publisher, PublisherAdd, PublisherInfo
from src.publishers.validations import is_publisher_unique
from datetime import date


class PublisherCrud:

    @staticmethod
    async def create_publisher(publisher_details, session):

        await is_publisher_unique(publisher_details.name.lower(), session)

        try:
            stmt = insert(PublishersModel).values(name=publisher_details.name.lower(),
                                                  established_year=publisher_details.established_year)
            await session.execute(stmt)
            await session.commit()

            query = select(PublishersModel).where(PublishersModel.name == publisher_details.name.lower())
            publisher = await session.execute(query)
            result = publisher.scalar_one_or_none()

            return PublisherInfo(id=result.id, name=result.name, established_year=result.established_year)

        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Something went wrong in add publisher api service. Details:\n{e}")

    @staticmethod
    async def get_all_publishers(skip, limit, session):

        try:
            query = select(PublishersModel).limit(limit).offset(skip)
            publishers_list = await session.execute(query)
            result_list = publishers_list.scalars().all()

            return [PublisherInfo(id=result.id,
                                  name=result.name,
                                  established_year=result.established_year) for result in result_list]

        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Something went wrong in get all publishers api service. Details:\n{e}")
