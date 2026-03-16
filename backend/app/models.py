from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlmodel import Field, SQLModel


class Role(str, enum.Enum):
    architect = "architect"
    project_owner = "project_owner"
    supervisor = "supervisor"
    field_manager = "field_manager"


class ProjectStatus(str, enum.Enum):
    active = "active"
    completed = "completed"
    on_hold = "on_hold"


class ProjectType(str, enum.Enum):
    implementation = "implementation"
    maintenance = "maintenance"


class MaintenanceTaskStatus(str, enum.Enum):
    pending = "pending"
    done = "done"
    deferred = "deferred"


class WbsItemType(str, enum.Enum):
    milestone = "milestone"
    sub_milestone = "sub_milestone"
    task = "task"


class WbsStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    pending_approval = "pending_approval"
    completed = "completed"
    rejected = "rejected"


class DefectSeverity(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class DefectStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    pending_approval = "pending_approval"
    resolved = "resolved"
    closed = "closed"
    reopened = "reopened"
    cancelled = "cancelled"
    approved = "approved"


class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    email: str = Field(index=True, unique=True)
    name: str
    role: Role = Field(index=True)
    password_hash: str
    phone: str = ""
    whatsapp_phone: str = ""
    address: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserProject(SQLModel, table=True):
    """Which projects a user is associated with (many-to-many)."""
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(index=True)
    project_id: str = Field(index=True)


class UserLocation(SQLModel, table=True):
    """Locations a user is associated with (e.g. site, block). One user can have many."""
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(index=True)
    location: str = Field(index=True)


class PermissionResource(str, enum.Enum):
    projects = "projects"
    wbs = "wbs"
    boq = "boq"
    defects = "defects"
    materials = "materials"
    users = "users"
    approvals = "approvals"


class RolePermission(SQLModel, table=True):
    """Per-role CRUD access to resources."""
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    role: str = Field(index=True)  # Role.value
    resource: str = Field(index=True)  # PermissionResource.value
    can_create: bool = False
    can_read: bool = True
    can_update: bool = False
    can_delete: bool = False


class Project(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str = Field(index=True)
    description: str = ""
    budget: float = 0.0
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: ProjectStatus = Field(default=ProjectStatus.active, index=True)
    project_type: str = Field(default="implementation", index=True)  # ProjectType.value

    # executive summary fields (editable)
    summary_what_completed: str = ""
    summary_where_we_stand: str = ""
    summary_pain_points: str = ""
    summary_where_heading: str = ""

    created_by_user_id: Optional[str] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class WbsItem(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    project_id: str = Field(index=True)
    parent_id: Optional[str] = Field(default=None, index=True)

    name: str
    item_type: WbsItemType = Field(index=True)
    sort_order: int = Field(default=0, index=True)  # preserve Excel row order
    weight: float = 0.0  # percent relative to parent
    status: WbsStatus = Field(default=WbsStatus.pending, index=True)

    start_date: Optional[str] = None
    end_date: Optional[str] = None

    primary_owner_id: Optional[str] = Field(default=None, index=True)
    secondary_owner_id: Optional[str] = Field(default=None, index=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class WbsPhoto(SQLModel, table=True):
    """Before/after photo for task progress on a WBS item. One before and one after per item."""
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    wbs_item_id: str = Field(index=True)
    phase: str = Field(index=True)  # "before" or "after"
    filename: str = ""
    content_type: str = ""
    content_base64: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class WbsAudio(SQLModel, table=True):
    """Before/after audio note for task progress on a WBS item. One before and one after per item."""
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    wbs_item_id: str = Field(index=True)
    phase: str = Field(index=True)  # "before" or "after"
    filename: str = ""
    content_type: str = ""
    content_base64: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MaterialMaster(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str = Field(index=True, unique=True)
    default_unit: str = "pcs"
    pending_approval: bool = False  # true when create/edit by Supervisor/Field, needs Architect/PO/Supervisor approval
    created_at: datetime = Field(default_factory=datetime.utcnow)


class BoqItem(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    project_id: str = Field(index=True)
    wbs_item_id: Optional[str] = Field(default=None, index=True)  # link to task

    material_name: str  # from MaterialMaster name or free text if not in master
    unit: str = "pcs"
    estimated_quantity: float = 0.0
    unit_price: float = 0.0  # masked for field_manager
    actual_quantity: float = 0.0
    pending_approval: bool = False  # true when actual qty/price changed and needs supervisor approval

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DefectAttachmentType(str, enum.Enum):
    photo = "photo"
    video = "video"
    audio = "audio"


class Defect(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    project_id: str = Field(index=True)
    wbs_item_id: Optional[str] = Field(default=None, index=True)  # optional link to task/subtask

    display_number: Optional[int] = Field(default=None, index=True)  # auto per-project (#1, #2, …)

    location: str
    description: str
    severity: DefectSeverity = Field(default=DefectSeverity.medium, index=True)
    status: DefectStatus = Field(default=DefectStatus.open, index=True)

    reported_by: str = ""  # free-text (public allowed)
    reporter_contact: str = ""
    assigned_to_user_id: Optional[str] = Field(default=None, index=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class MaintenanceMonth(SQLModel, table=True):
    """One month of planning/tracking for a maintenance project."""
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    project_id: str = Field(index=True)
    year: int = Field(index=True)
    month: int = Field(index=True)  # 1-12


class MaintenanceTask(SQLModel, table=True):
    """A single repetitive task within a maintenance month."""
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    maintenance_month_id: str = Field(index=True)
    name: str = ""
    status: str = Field(default="pending", index=True)  # MaintenanceTaskStatus.value
    sort_order: int = 0


class DefectAttachment(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    defect_id: str = Field(index=True)
    file_type: DefectAttachmentType = Field(index=True)  # photo, video, audio
    filename: str = ""
    content_type: str = ""
    content_base64: Optional[str] = Field(default=None)  # base64 for storage
    phase: str = "before"  # "before" = at report/open; "after" = at resolution for comparison
    created_at: datetime = Field(default_factory=datetime.utcnow)

