"""Data models and schemas for AP 3-Way Matching Agent.

Defines Pydantic models for Purchase Orders, Goods Receipt Notes,
Supplier Invoices, line item checks, and reconciliation reports.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    PURCHASE_ORDER = "PO"
    GOODS_RECEIPT_NOTE = "GRN"
    SUPPLIER_INVOICE = "INV"


class CheckStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"


class Verdict(str, Enum):
    MATCHED = "MATCHED"
    EXCEPTION = "EXCEPTION"
    HOLD = "HOLD"


class LineItem(BaseModel):
    item_code: str = Field(..., description="Unique SKU or item code")
    description: str = Field(..., description="Item textual description")
    qty: float = Field(..., description="Quantity ordered, received, or billed")
    unit_price: float = Field(..., description="Unit price per item")
    line_total: Optional[float] = Field(None, description="Line total amount")


class PurchaseOrder(BaseModel):
    po_number: str = Field(..., description="Purchase order identifier (e.g. PO-1001)")
    supplier_name: str = Field(..., description="Authorized vendor name")
    po_date: Optional[str] = Field(None, description="Date PO was authorized")
    line_items: List[LineItem] = Field(default_factory=list, description="Contracted items")
    total_amount: Optional[float] = Field(None, description="Total authorized commitment")


class GoodsReceiptNote(BaseModel):
    grn_number: Optional[str] = Field(None, description="GRN identifier (e.g. GRN-5001)")
    po_number: str = Field(..., description="Referenced PO number")
    delivery_date: Optional[str] = Field(None, description="Date goods received & inspected")
    line_items: List[LineItem] = Field(default_factory=list, description="Goods actually received")


class SupplierInvoice(BaseModel):
    invoice_number: str = Field(..., description="Invoice identifier (e.g. INV-9001)")
    po_number: str = Field(..., description="Referenced PO number")
    supplier_name: str = Field(..., description="Vendor billing name")
    invoice_date: Optional[str] = Field(None, description="Date invoice generated")
    line_items: List[LineItem] = Field(default_factory=list, description="Items billed")
    total_due: Optional[float] = Field(None, description="Total invoiced payable amount")


class LineReconciliation(BaseModel):
    item_code: str
    description: str
    po_qty: float
    received_qty: float
    billed_qty: float
    po_price: float
    billed_price: float
    price_check: CheckStatus
    qty_check: CheckStatus
    amount_check: CheckStatus
    item_check: CheckStatus
    price_variance: float = 0.0
    qty_variance: float = 0.0
    approved_amount: float = 0.0
    held_amount: float = 0.0
    is_short_receipt: bool = False
    exception_reason: Optional[str] = None


class ReconciliationReport(BaseModel):
    po_number: str
    supplier_name: str
    invoice_number: Optional[str] = None
    verdict: Verdict
    recommended_action: str
    total_invoiced: float = 0.0
    total_approved: float = 0.0
    total_held: float = 0.0
    line_reconciliations: List[LineReconciliation] = Field(default_factory=list)
    exception_reasons: List[str] = Field(default_factory=list)
    missing_documents: List[str] = Field(default_factory=list)
    summary_notes: str = ""
