from sqlalchemy import String, Column, Float, Integer

from chat_chart.orm import Base
from chat_chart.pollution.entities import PollutionSubmission


class PollutionSubmissionORM(Base):
    __tablename__ = 'pollution_submissions'

    region = Column(String(50), primary_key=True)
    iso3 = Column(String(50), primary_key=True)
    country = Column(String(50), primary_key=True)
    city = Column(String(50), primary_key=True)
    year = Column(Integer(), primary_key=True)
    pm25 = Column(Float(), primary_key=True)
    pm10 = Column(Float(), primary_key=True)
    no2 = Column(Float(), primary_key=True)

    def to_entity(self) -> PollutionSubmission:
        return PollutionSubmission.model_validate(self)
