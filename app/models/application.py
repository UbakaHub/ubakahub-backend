from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from db import Base
import enum

class PermitType(enum.Enum):
    NEW_BUILDING = "new_building"
    RENOVATION_STRUCTURAL = "renovation_structural"
    RENOVATION_NON_STRUCTURAL = "renovation_non_structural"
    OCCUPANCY = "occupancy"
    DEMOLITION = "demolition"
    FENCE = "fence"
    MODIFICATION = "modification"
    RENEWAL = "renewal"

class BuildingCategory(enum.Enum):
    CATEGORY_2 = "category_2"
    CATEGORY_3 = "category_3"
    CATEGORY_4 = "category_4"
    CATEGORY_5 = "category_5"

class ApplicationStatus(enum.Enum):
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    AWAITING_VERIFICATION = "awaiting_verification"
    APPROVED = "approved"
    REJECTED = "rejected"

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    applicant_id = Column(Integer, ForeignKey("users.id"))
    permit_type = Column(Enum(PermitType), nullable=False)
    building_category = Column(Enum(BuildingCategory), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING)
    location = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    documents = relationship("Document", back_populates="application")
    status_history = relationship("StatusHistory", back_populates="application")

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    name = Column(String(255))
    file_path = Column(String(255))
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application", back_populates="documents")

class StatusHistory(Base):
    __tablename__ = "status_history"

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    new_status = Column(Enum(ApplicationStatus))
    changed_at = Column(DateTime, default=datetime.utcnow)
    changed_by = Column(Integer)  # user id of admin

    application = relationship("Application", back_populates="status_history")