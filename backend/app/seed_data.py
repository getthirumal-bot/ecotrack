"""
Rich demo data: 10 projects at different phases, multi-level WBS, BOQ/BOM, defects.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from sqlmodel import Session, select

from .models import (
    BoqItem,
    Defect,
    DefectSeverity,
    DefectStatus,
    MaterialMaster,
    Project,
    ProjectStatus,
    Role,
    User,
    WbsItem,
    WbsItemType,
    WbsStatus,
)


def _now() -> datetime:
    return datetime.utcnow()


# ---------------------------------------------------------------------------
# 10 projects: different phases, budgets, statuses
# ---------------------------------------------------------------------------
PROJECTS: List[Dict[str, Any]] = [
    {
        "name": "Mundra Port Landscaping Phase 2",
        "description": "Green belt and avenue plantation along port approach roads; irrigation and hardscape.",
        "budget": 24_500_000,
        "status": ProjectStatus.active,
        "summary_what_completed": "Site clearance and grading completed. 40% of avenue plantation done. Main irrigation line laid.",
        "summary_where_we_stand": "Currently in plantation and drip installation. Slight delay in hardscape due to material availability.",
        "summary_pain_points": "Steel railing delivery delayed by 3 weeks. Labour shortage in peak season.",
        "summary_where_heading": "Complete Zone A plantation by month-end. Start water feature and plaza hardscape.",
    },
    {
        "name": "Central Park Renovation",
        "description": "Revamp of 12-acre urban park: lawns, flower beds, irrigation, walking tracks, and lighting.",
        "budget": 8_750_000,
        "status": ProjectStatus.active,
        "summary_what_completed": "Old fencing removed. Soil testing and design finalised. Irrigation design approved.",
        "summary_where_we_stand": "WBS and BOQ baseline locked. Procurement for irrigation and plants in progress.",
        "summary_pain_points": "Municipal NOC for tree felling pending. Budget approval for lighting package delayed.",
        "summary_where_heading": "Award irrigation and plantation contracts. Begin lawn preparation in North block.",
    },
    {
        "name": "Highway Green Belt Project NH-48",
        "description": "Median and roadside plantation along 45 km stretch; drip irrigation and maintenance for 2 years.",
        "budget": 18_200_000,
        "status": ProjectStatus.active,
        "summary_what_completed": "Survey and species selection done. First 15 km median plantation completed. Pump houses commissioned.",
        "summary_where_we_stand": "Remaining 30 km in progress. Some mortality replacement and weed control ongoing.",
        "summary_pain_points": "Vandalism and theft of drip lines in 2 sections. Water supply irregular in one zone.",
        "summary_where_heading": "Complete full stretch plantation. Hand over to maintenance contractor by Q2.",
    },
    {
        "name": "Corporate Campus Greens – Tech Hub",
        "description": "Landscaping for 8-acre corporate campus: lawns, trees, water body, outdoor seating, and signage.",
        "budget": 12_000_000,
        "status": ProjectStatus.active,
        "summary_what_completed": "Master plan and BOQ approved. Earthwork and drainage completed. 60% of softscape done.",
        "summary_where_we_stand": "Lawn laying and shrubbery in progress. Water body lining and pump installation next.",
        "summary_pain_points": "Client requested design change for amphitheatre – cost impact under review.",
        "summary_where_heading": "Complete softscape and water feature. Start hardscape and outdoor furniture.",
    },
    {
        "name": "Residential Township Parks & Gardens",
        "description": "Three neighbourhood parks, central garden, and street plantation for 1200-unit township.",
        "budget": 6_500_000,
        "status": ProjectStatus.active,
        "summary_what_completed": "Park 1 and Park 2 completed and handed over. Central garden 80% complete.",
        "summary_where_we_stand": "Park 3 and street plantation in execution. Some snag list items from Park 1 pending.",
        "summary_pain_points": "RWA dispute on species in Park 3 – resolution meeting scheduled.",
        "summary_where_heading": "Close Park 3 and central garden. Complete street trees and handover.",
    },
    {
        "name": "Institutional Campus – School of Horticulture",
        "description": "Demonstration gardens, nursery block, greenhouse, and training plots for horticulture school.",
        "budget": 9_200_000,
        "status": ProjectStatus.on_hold,
        "summary_what_completed": "Layout and soil work done. Greenhouse structure erected. Nursery block foundation laid.",
        "summary_where_we_stand": "Project put on hold pending release of next tranche of funding by institute.",
        "summary_pain_points": "Budget freeze by management. Key equipment orders cancelled until hold is lifted.",
        "summary_where_heading": "Resume nursery block and demonstration plots once funding is released.",
    },
    {
        "name": "Riverfront Promenade Landscaping",
        "description": "2.5 km riverfront walkway with planting, seating, lighting, and small pavilions.",
        "budget": 15_750_000,
        "status": ProjectStatus.active,
        "summary_what_completed": "Retaining wall and promenade base completed. 1.2 km of plantation and lighting done.",
        "summary_where_we_stand": "Remaining 1.3 km in progress. One pavilion completed, two under construction.",
        "summary_pain_points": "River level rise damaged a section of plantation – rework in progress.",
        "summary_where_heading": "Complete full stretch and all pavilions. Final lighting and signage.",
    },
    {
        "name": "Industrial Zone Green Buffer",
        "description": "Green buffer zone around industrial cluster: tree plantation, shrub screen, and basic irrigation.",
        "budget": 4_200_000,
        "status": ProjectStatus.completed,
        "summary_what_completed": "Full plantation and drip irrigation completed. Fencing and gates installed. Handover done.",
        "summary_where_we_stand": "Project closed. One-year defect liability period started.",
        "summary_pain_points": "Minor replacement of saplings in one patch – covered under DL.",
        "summary_where_heading": "Support DL period and close contract after final inspection.",
    },
    {
        "name": "Airport Approach Road Landscaping",
        "description": "Landscaping and beautification of 8 km airport approach; seasonal flowers and permanent planting.",
        "budget": 11_000_000,
        "status": ProjectStatus.active,
        "summary_what_completed": "Median and side strip plantation 100% done. Flower beds and mulch laid. Irrigation operational.",
        "summary_where_we_stand": "Seasonal flower rotation in place. One round of replacement and pruning completed.",
        "summary_pain_points": "Restriction on watering timings by airport authority – adjusting schedule.",
        "summary_where_heading": "Continue seasonal rotation and maintenance. Apply for final completion certificate.",
    },
    {
        "name": "Botanical Garden Extension",
        "description": "New 5-acre extension: thematic sections, glasshouse, and visitor facilities.",
        "budget": 22_000_000,
        "status": ProjectStatus.active,
        "summary_what_completed": "Land development and thematic layout done. 70% of planting and pathways completed.",
        "summary_where_we_stand": "Glasshouse and interpretation centre under construction. Some rare species yet to source.",
        "summary_pain_points": "Import permit for certain species delayed. Cost escalation on glasshouse.",
        "summary_where_heading": "Complete glasshouse and remaining planting. Soft launch by next quarter.",
    },
]

# ---------------------------------------------------------------------------
# WBS: Milestones (root) -> Sub-milestones -> Tasks (multi-level)
# ---------------------------------------------------------------------------
def _flat_wbs_with_parents() -> List[Tuple[Optional[str], str, str, float, WbsStatus]]:
    """(parent_name_or_none, name, type, weight, status). Root items have parent None."""
    base: List[Tuple[Optional[str], str, str, float, WbsStatus]] = [
        (None, "Earthwork & Drainage", "milestone", 25.0, WbsStatus.completed),
        ("Earthwork & Drainage", "Site clearance and stripping", "sub_milestone", 40.0, WbsStatus.completed),
        ("Site clearance and stripping", "Clear and strip topsoil", "task", 50.0, WbsStatus.completed),
        ("Site clearance and stripping", "Stockpile topsoil", "task", 50.0, WbsStatus.completed),
        ("Earthwork & Drainage", "Grading and levelling", "sub_milestone", 60.0, WbsStatus.completed),
        ("Grading and levelling", "Rough grading", "task", 50.0, WbsStatus.completed),
        ("Grading and levelling", "Fine grading and compaction", "task", 50.0, WbsStatus.completed),
        (None, "Irrigation System", "milestone", 30.0, WbsStatus.in_progress),
        ("Irrigation System", "Main line and submains", "sub_milestone", 50.0, WbsStatus.completed),
        ("Main line and submains", "Main line laying and pressure test", "task", 60.0, WbsStatus.completed),
        ("Main line and submains", "Submain and valve assembly", "task", 40.0, WbsStatus.completed),
        ("Irrigation System", "Laterals and drippers", "sub_milestone", 50.0, WbsStatus.in_progress),
        ("Laterals and drippers", "Lateral layout and connection", "task", 50.0, WbsStatus.in_progress),
        ("Laterals and drippers", "Dripper installation and flush", "task", 50.0, WbsStatus.pending),
        (None, "Plantation", "milestone", 35.0, WbsStatus.in_progress),
        ("Plantation", "Tree plantation", "sub_milestone", 50.0, WbsStatus.in_progress),
        ("Tree plantation", "Pit digging and soil mix", "task", 40.0, WbsStatus.completed),
        ("Tree plantation", "Staking and planting", "task", 60.0, WbsStatus.in_progress),
        ("Plantation", "Shrub and ground cover", "sub_milestone", 50.0, WbsStatus.pending),
        ("Shrub and ground cover", "Bed preparation", "task", 40.0, WbsStatus.pending),
        ("Shrub and ground cover", "Planting and mulching", "task", 60.0, WbsStatus.pending),
        (None, "Hardscape & Finishing", "milestone", 10.0, WbsStatus.pending),
        ("Hardscape & Finishing", "Pathways and edging", "sub_milestone", 60.0, WbsStatus.pending),
        ("Pathways and edging", "Base and paving", "task", 70.0, WbsStatus.pending),
        ("Pathways and edging", "Edging and joints", "task", 30.0, WbsStatus.pending),
        ("Hardscape & Finishing", "Furniture and signage", "sub_milestone", 40.0, WbsStatus.pending),
        ("Furniture and signage", "Bench and bin installation", "task", 50.0, WbsStatus.pending),
        ("Furniture and signage", "Signage and interpretation", "task", 50.0, WbsStatus.pending),
    ]
    # Extra deep branch (7–10 levels) for testing complex trees
    deep_branch: List[Tuple[Optional[str], str, str, float, WbsStatus]] = [
        (None, "Deep Branch L1", "milestone", 5.0, WbsStatus.in_progress),
        ("Deep Branch L1", "Deep Branch L2", "sub_milestone", 5.0, WbsStatus.in_progress),
        ("Deep Branch L2", "Deep Branch L3", "sub_milestone", 5.0, WbsStatus.in_progress),
        ("Deep Branch L3", "Deep Branch L4", "sub_milestone", 5.0, WbsStatus.in_progress),
        ("Deep Branch L4", "Deep Branch L5", "sub_milestone", 5.0, WbsStatus.pending),
        ("Deep Branch L5", "Deep Branch L6", "sub_milestone", 5.0, WbsStatus.pending),
        ("Deep Branch L6", "Deep Branch L7", "sub_milestone", 5.0, WbsStatus.pending),
        ("Deep Branch L7", "Deep Branch Task A", "task", 50.0, WbsStatus.pending),
        ("Deep Branch L7", "Deep Branch Task B", "task", 50.0, WbsStatus.pending),
    ]
    return base + deep_branch


# ---------------------------------------------------------------------------
# BOQ/BOM: material, unit, est qty, unit price. Some with actual qty for variance
# ---------------------------------------------------------------------------
BOQ_TEMPLATE: List[Dict[str, Any]] = [
    {"material_name": "Topsoil (screened)", "unit": "m3", "est": 450.0, "price": 850.0, "actual_pct": 1.0},
    {"material_name": "Vermicompost", "unit": "MT", "est": 25.0, "price": 12000.0, "actual_pct": 0.8},
    {"material_name": "FYM (Farmyard manure)", "unit": "MT", "est": 60.0, "price": 3500.0, "actual_pct": 0.6},
    {"material_name": "PVC pipe 80mm (main)", "unit": "m", "est": 1200.0, "price": 185.0, "actual_pct": 0.9},
    {"material_name": "PVC pipe 50mm (submain)", "unit": "m", "est": 2500.0, "price": 95.0, "actual_pct": 0.85},
    {"material_name": "Drip lateral 16mm", "unit": "m", "est": 8500.0, "price": 22.0, "actual_pct": 0.5},
    {"material_name": "Drippers (inline)", "unit": "pcs", "est": 12000.0, "price": 8.5, "actual_pct": 0.3},
    {"material_name": "Filter unit (screen)", "unit": "pcs", "est": 4.0, "price": 25000.0, "actual_pct": 1.0},
    {"material_name": "Submersible pump 2HP", "unit": "pcs", "est": 2.0, "price": 18500.0, "actual_pct": 1.0},
    {"material_name": "Tree saplings (native)", "unit": "pcs", "est": 1200.0, "price": 450.0, "actual_pct": 0.4},
    {"material_name": "Shrub / hedge plants", "unit": "pcs", "est": 3500.0, "price": 85.0, "actual_pct": 0.2},
    {"material_name": "Ground cover (sqm)", "unit": "sqm", "est": 2200.0, "price": 120.0, "actual_pct": 0.0},
    {"material_name": "Mulch (organic)", "unit": "m3", "est": 80.0, "price": 2200.0, "actual_pct": 0.0},
    {"material_name": "Tree stakes (bamboo)", "unit": "pcs", "est": 1200.0, "price": 65.0, "actual_pct": 0.35},
    {"material_name": "Paver blocks (interlock)", "unit": "sqm", "est": 350.0, "price": 420.0, "actual_pct": 0.0},
    {"material_name": "Edge restraint", "unit": "m", "est": 600.0, "price": 95.0, "actual_pct": 0.0},
    {"material_name": "Labour (plantation)", "unit": "mandays", "est": 450.0, "price": 650.0, "actual_pct": 0.5},
    {"material_name": "Labour (irrigation)", "unit": "mandays", "est": 120.0, "price": 700.0, "actual_pct": 0.7},
]

# ---------------------------------------------------------------------------
# Defects template: location, description, severity, status
# ---------------------------------------------------------------------------
DEFECTS_TEMPLATE: List[Dict[str, Any]] = [
    {"location": "Zone A - North strip", "description": "Drip line leak at junction 12; wet patch observed.", "severity": DefectSeverity.medium, "status": DefectStatus.resolved},
    {"location": "Median block 3", "description": "Five saplings wilted; possible overwatering.", "severity": DefectSeverity.low, "status": DefectStatus.open},
    {"location": "Pump house 1", "description": "Pressure gauge reading erratic; needs replacement.", "severity": DefectSeverity.high, "status": DefectStatus.in_progress},
    {"location": "Pathway section 2", "description": "Settlement crack in base; water pooling after rain.", "severity": DefectSeverity.medium, "status": DefectStatus.open},
    {"location": "Entrance bed", "description": "Vandalism – plants uprooted; need replanting and guard.", "severity": DefectSeverity.critical, "status": DefectStatus.in_progress},
]


def _get_type(s: str) -> WbsItemType:
    return WbsItemType.milestone if s == "milestone" else (WbsItemType.sub_milestone if s == "sub_milestone" else WbsItemType.task)


def _add_wbs_boq_defects(
    session: Session,
    p: Project,
    *,
    owner_id: Optional[str],
    field_id: Optional[str],
    super_id: Optional[str],
) -> None:
    """Add full WBS tree, BOQ items, and defects to project p."""
    # WBS: build hierarchy by parent name
    name_to_id: Dict[str, str] = {}
    for idx, (parent_name, name, itype, weight, status) in enumerate(_flat_wbs_with_parents()):
        parent_id = name_to_id.get(parent_name) if parent_name else None
        # Simple synthetic dates so every line shows dates in UI (MS Project–like)
        start_day = (idx % 25) + 1
        end_day = min(start_day + 5, 28)
        start_date = f"2025-01-{start_day:02d}"
        end_date = f"2025-01-{end_day:02d}"
        w = WbsItem(
            project_id=p.id,
            parent_id=parent_id,
            name=name,
            item_type=_get_type(itype),
            weight=weight,
            status=status,
            start_date=start_date,
            end_date=end_date,
            primary_owner_id=field_id,
            secondary_owner_id=super_id,
            created_at=_now(),
            updated_at=_now(),
        )
        session.add(w)
        session.flush()
        name_to_id[name] = w.id

    task_ids = [w.id for w in session.exec(select(WbsItem).where(WbsItem.project_id == p.id, WbsItem.item_type == WbsItemType.task)).all()]

    for i, b in enumerate(BOQ_TEMPLATE):
        task_id = task_ids[i % len(task_ids)] if task_ids else None
        est = b["est"]
        price = b["price"]
        actual_pct = b.get("actual_pct", 0.0)
        act = round(est * actual_pct, 2)
        session.add(
            BoqItem(
                project_id=p.id,
                wbs_item_id=task_id,
                material_name=b["material_name"],
                unit=b["unit"],
                estimated_quantity=est,
                unit_price=price,
                actual_quantity=act,
                created_at=_now(),
                updated_at=_now(),
            )
        )

    for d in DEFECTS_TEMPLATE:
        session.add(
            Defect(
                project_id=p.id,
                location=d["location"],
                description=d["description"],
                severity=d["severity"],
                status=d["status"],
                reported_by="Demo data",
                reporter_contact="",
                assigned_to_user_id=field_id,
                created_at=_now(),
                updated_at=_now(),
            )
        )


MATERIAL_MASTER_NAMES: List[Tuple[str, str]] = [
    ("Bricks", "pcs"), ("Cement", "bags"), ("Sand", "cum"), ("Steel", "kg"),
    ("Plants", "nos"), ("Soil", "cum"), ("Mulch", "cum"), ("Fertilizer", "kg"),
    ("Drip line", "m"), ("Pipe", "m"), ("Labour", "man-days"),
]


def _ensure_material_master(session: Session) -> None:
    """Ensure material master has default entries for BOQ dropdown."""
    existing = {m.name for m in session.exec(select(MaterialMaster)).all()}
    for name, unit in MATERIAL_MASTER_NAMES:
        if name not in existing:
            session.add(MaterialMaster(name=name, default_unit=unit))
            existing.add(name)


def seed_demo_projects(session: Session) -> int:
    """
    Create the 10 demo projects with full WBS, BOQ, defects only when they do not exist.
    Never deletes or overwrites existing project data (avoids wiping UI-created data on deploy/login).
    Returns number of projects created.
    """
    _ensure_material_master(session)
    session.flush()
    architect = session.exec(select(User).where(User.role == Role.architect)).first()
    field_user = session.exec(select(User).where(User.role == Role.field_manager)).first()
    supervisor_user = session.exec(select(User).where(User.role == Role.supervisor)).first()
    owner_id = architect.id if architect else None
    field_id = field_user.id if field_user else None
    super_id = supervisor_user.id if supervisor_user else None

    existing_by_name = {p.name: p for p in session.exec(select(Project)).all()}

    created = 0
    for pdef in PROJECTS:
        name = pdef["name"]
        if name in existing_by_name:
            # Project already exists (user-created or from previous seed). Do not touch it.
            continue
        p = Project(
            name=name,
            description=pdef["description"],
            budget=float(pdef["budget"]),
            status=pdef["status"],
            created_by_user_id=owner_id,
            summary_what_completed=pdef.get("summary_what_completed", ""),
            summary_where_we_stand=pdef.get("summary_where_we_stand", ""),
            summary_pain_points=pdef.get("summary_pain_points", ""),
            summary_where_heading=pdef.get("summary_where_heading", ""),
            created_at=_now(),
            updated_at=_now(),
        )
        session.add(p)
        session.flush()
        existing_by_name[name] = p
        _add_wbs_boq_defects(session, p, owner_id=owner_id, field_id=field_id, super_id=super_id)
        created += 1

    session.commit()
    return created
