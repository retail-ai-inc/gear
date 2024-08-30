from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .init_db import Base


class ModelMeta(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String)
    description = Column(String)
    name = Column(String)
    version = Column(String)
    framework = Column(String)
    path = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # pipeline_id = Column(Integer, ForeignKey('pipelines.id'))
    # pipelines = relationship("Pipeline", back_populates="models")

# # The relationship between the pipeline and the model
# class PipelineModels:
#     __tablename__ = "pipeline_models"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     pipeline_id = Column(Integer)
#     model_id = Column(Integer)


class PipelineMeta(Base):
    __tablename__ = "pipelines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String)
    description = Column(String)
    name = Column(String)
    version = Column(String)
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # models = relationship("Models", back_populates="model")
