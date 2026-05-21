from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.auth import check_role
from app.database import get_db
from app.schemas import InventoryCreate, InventoryOut
from app.schemas import InventoryAdjust

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post("", response_model=InventoryOut, status_code=201, dependencies=[Depends(check_role(["Admin", "Accounts"]))])
def add_inventory_item(
    data: InventoryCreate,
    db: Session = Depends(get_db),
):
    """Add a new item to inventory."""
    return crud.create_inventory_item(db, data)

@router.get("/low-stock", response_model=List[InventoryOut], dependencies=[Depends(check_role(["Admin", "Accounts", "Pharmacy", "Lab"]))])
def get_low_stock_items(
    db: Session = Depends(get_db),
):
    """Get items at or below reorder level."""
    return crud.get_low_stock(db)


@router.get("", response_model=List[InventoryOut], dependencies=[Depends(check_role(["Admin", "Accounts", "Pharmacy", "Lab"]))])
def list_inventory(db: Session = Depends(get_db)):
    """List all inventory items."""
    return crud.get_inventory(db)


@router.patch("/{item_id}/adjust", response_model=InventoryOut, dependencies=[Depends(check_role(["Admin", "Accounts", "Pharmacy"]))])
def adjust_item(item_id: int, data: InventoryAdjust, db: Session = Depends(get_db)):
    """Adjust stock quantity by delta (positive or negative)."""
    return crud.adjust_inventory(db, item_id, data.delta)
