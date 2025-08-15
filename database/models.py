from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class UserRole(Enum):
	ADMIN = "admin"
	MANAGER = "manager"
	JUNIOR_MANAGER = "junior_manager"
	CONTROLLER = "controller"
	TECHNICIAN = "technician"
	WAREHOUSE = "warehouse"
	CALL_CENTER = "call_center"
	CALL_CENTER_SUPERVISOR = "call_center_supervisor"
	CLIENT = "client"
	BLOCKED = "blocked"


class DocumentType(Enum):
	CONNECTION = "connection"
	TECHNICAL_SERVICE = "technical_service"
	STAFF_CREATED = "staff_created"


class Priority(Enum):
	LOW = "low"
	MEDIUM = "medium"
	HIGH = "high"
	URGENT = "urgent"


# ===== Core =====
@dataclass
class User:
	id: Optional[int] = None
	telegram_id: Optional[int] = None
	full_name: Optional[str] = None
	username: Optional[str] = None
	phone: Optional[str] = None
	role: str = UserRole.CLIENT.value
	abonent_id: Optional[str] = None
	language: str = "uz"
	is_active: bool = True
	address: Optional[str] = None
	permissions: Dict[str, Any] = field(default_factory=dict)
	last_activity: Optional[datetime] = None
	created_at: Optional[datetime] = None
	updated_at: Optional[datetime] = None


@dataclass
class RolePermissions:
	id: Optional[int] = None
	role: str = UserRole.CLIENT.value
	application_types: List[str] = field(default_factory=list)
	workflow_actions: List[str] = field(default_factory=list)
	inbox_access: bool = True
	client_search_access: bool = False
	inventory_access: bool = False
	reporting_access: bool = False
	admin_functions: List[str] = field(default_factory=list)
	created_at: Optional[datetime] = None
	updated_at: Optional[datetime] = None


@dataclass
class SystemSettings:
	id: Optional[int] = None
	setting_key: Optional[str] = None
	setting_value: Optional[str] = None
	description: Optional[str] = None
	updated_by: Optional[int] = None
	updated_at: Optional[datetime] = None


# ===== Workflow =====
@dataclass
class ServiceRequest:
	id: Optional[str] = None
	workflow_type: str = "connection_request"
	client_id: Optional[int] = None
	role_current: str = UserRole.MANAGER.value
	current_status: str = "created"
	priority: str = Priority.MEDIUM.value
	description: Optional[str] = None
	location: Optional[str] = None
	contact_info: Dict[str, Any] = field(default_factory=dict)
	state_data: Dict[str, Any] = field(default_factory=dict)
	equipment_used: List[Dict[str, Any]] = field(default_factory=list)
	inventory_updated: bool = False
	completion_rating: Optional[int] = None
	feedback_comments: Optional[str] = None
	current_assignee_id: Optional[int] = None
	current_assignee_role: Optional[str] = None
	created_by_staff: bool = False
	staff_creator_id: Optional[int] = None
	staff_creator_role: Optional[str] = None
	creation_source: str = "client"
	client_notified_at: Optional[datetime] = None
	diagnosis: Optional[str] = None
	service_order_number: Optional[str] = None
	accepted_by_fio: Optional[str] = None
	approvers: List[Dict[str, Any]] = field(default_factory=list)
	installation_date: Optional[datetime] = None
	installed_by: Optional[int] = None
	diagnosis_date: Optional[datetime] = None
	diagnosed_by: Optional[int] = None
	rated_at: Optional[datetime] = None
	assigned_technician_id: Optional[int] = None
	ready_to_install: bool = False
	created_at: Optional[datetime] = None
	updated_at: Optional[datetime] = None


@dataclass
class StateTransition:
	id: Optional[int] = None
	request_id: Optional[str] = None
	from_role: Optional[str] = None
	to_role: Optional[str] = None
	action: Optional[str] = None
	actor_id: Optional[int] = None
	transition_data: Dict[str, Any] = field(default_factory=dict)
	comments: Optional[str] = None
	created_at: Optional[datetime] = None


@dataclass
class WorkflowTracking:
	id: Optional[int] = None
	request_id: Optional[str] = None
	from_role: Optional[str] = None
	to_role: Optional[str] = None
	user_id: Optional[int] = None
	transition_time: Optional[datetime] = None
	duration_minutes: Optional[int] = None
	efficiency_score: Optional[float] = None
	notes: Optional[str] = None
	created_at: Optional[datetime] = None


@dataclass
class RoleStatistics:
	id: Optional[int] = None
	role: str = UserRole.MANAGER.value
	period: str = "daily"
	date: Optional[datetime] = None
	total_requests: int = 0
	completed_requests: int = 0
	avg_completion_time: Optional[float] = None
	avg_efficiency_score: Optional[float] = None
	avg_quality_rating: Optional[float] = None
	unique_users: int = 0
	created_at: Optional[datetime] = None
	updated_at: Optional[datetime] = None


# ===== Inbox / Transfers =====
@dataclass
class InboxMessage:
	id: Optional[int] = None
	application_id: Optional[str] = None
	application_type: str = "service_request"
	assigned_role: str = UserRole.MANAGER.value
	message_type: str = "application"
	title: Optional[str] = None
	description: Optional[str] = None
	priority: str = Priority.MEDIUM.value
	is_read: bool = False
	recipient_id: Optional[int] = None
	reply_markup_data: Dict[str, Any] = field(default_factory=dict)
	telegram_message_id: Optional[int] = None
	reply_button_clicked: bool = False
	inbox_viewed: bool = False
	completed: bool = False
	seen_by_users: List[int] = field(default_factory=list)
	metadata: Dict[str, Any] = field(default_factory=dict)
	created_at: Optional[datetime] = None
	updated_at: Optional[datetime] = None


@dataclass
class ApplicationTransfer:
	id: Optional[int] = None
	application_id: Optional[str] = None
	application_type: str = "service_request"
	from_role: Optional[str] = None
	to_role: Optional[str] = None
	transferred_by: Optional[int] = None
	transfer_reason: Optional[str] = None
	transfer_notes: Optional[str] = None
	created_at: Optional[datetime] = None


# ===== Time / Statistics =====
@dataclass
class TimeTracking:
	id: Optional[int] = None
	request_id: Optional[str] = None
	user_id: Optional[int] = None
	role: str = UserRole.TECHNICIAN.value
	action_type: str = "started"
	started_at: Optional[datetime] = None
	ended_at: Optional[datetime] = None
	duration_minutes: Optional[int] = None
	workflow_stage: Optional[str] = None
	efficiency_score: Optional[float] = None
	quality_rating: Optional[float] = None
	notes: Optional[str] = None
	created_at: Optional[datetime] = None
	updated_at: Optional[datetime] = None


@dataclass
class RealtimeTimeTracking:
	id: Optional[int] = None
	request_id: Optional[str] = None
	user_id: Optional[int] = None
	role: Optional[str] = None
	started_at: Optional[datetime] = None
	ended_at: Optional[datetime] = None
	duration_minutes: Optional[int] = None
	notes: Optional[str] = None
	efficiency_score: Optional[float] = None
	quality_rating: Optional[float] = None
	created_at: Optional[datetime] = None


@dataclass
class EmployeePerformance:
	id: Optional[int] = None
	user_id: Optional[int] = None
	date: Optional[datetime] = None
	role: str = UserRole.TECHNICIAN.value
	total_requests: int = 0
	completed_requests: int = 0
	total_time_minutes: int = 0
	avg_time_per_request: Optional[float] = None
	efficiency_score: Optional[float] = None
	quality_rating: Optional[float] = None
	notes: Optional[str] = None
	created_at: Optional[datetime] = None
	updated_at: Optional[datetime] = None


@dataclass
class DailyStatistics:
	id: Optional[int] = None
	date: Optional[datetime] = None
	total_requests: int = 0
	completed_requests: int = 0
	cancelled_requests: int = 0
	pending_requests: int = 0
	avg_completion_time_minutes: Optional[float] = None
	total_work_hours: Optional[float] = None
	total_employees_worked: int = 0
	active_employees: int = 0
	avg_rating: Optional[float] = None
	total_feedback: int = 0
	completion_rate: Optional[float] = None
	created_at: Optional[datetime] = None
	updated_at: Optional[datetime] = None


@dataclass
class ExcelExport:
	id: Optional[int] = None
	user_id: Optional[int] = None
	export_type: Optional[str] = None
	date_range_start: Optional[datetime] = None
	date_range_end: Optional[datetime] = None
	file_name: Optional[str] = None
	file_size_bytes: Optional[int] = None
	file_hash: Optional[str] = None
	download_count: int = 0
	last_downloaded_at: Optional[datetime] = None
	filters_applied: Dict[str, Any] = field(default_factory=dict)
	record_count: Optional[int] = None
	created_at: Optional[datetime] = None


# ===== Word documents =====
@dataclass
class WordDocument:
	id: Optional[int] = None
	request_id: Optional[str] = None
	document_type: str = DocumentType.CONNECTION.value
	generated_at: Optional[datetime] = None
	file_path: Optional[str] = None
	document_data: Dict[str, Any] = field(default_factory=dict)
	created_by: Optional[int] = None
	application_date: Optional[str] = None
	technician_fio: Optional[str] = None
	contract_number: Optional[str] = None
	service_order_number: Optional[str] = None
	organization_name: Optional[str] = None
	accepted_by_fio: Optional[str] = None
	diagnosis_result: Optional[str] = None
	installed_equipment: Optional[List[Dict[str, Any]]] = None
	installation_address: Optional[str] = None
	completion_date: Optional[str] = None
	client_rating: Optional[int] = None
	client_comment: Optional[str] = None
	approvers: Optional[List[Dict[str, Any]]] = None
	service_type: Optional[str] = None
	problem_description: Optional[str] = None
	work_performed: Optional[str] = None
	replaced_parts: Optional[List[Dict[str, Any]]] = None
	result: Optional[str] = None
	operator_fio: Optional[str] = None
	client_fio: Optional[str] = None
	client_phone: Optional[str] = None
	consultation_date: Optional[str] = None


# ===== Inventory / Warehouse =====
@dataclass
class Material:
	id: Optional[int] = None
	name: Optional[str] = None
	category: str = "general"
	quantity: int = 0
	unit: str = "pcs"
	min_quantity: int = 5
	price: float = 0.0
	description: Optional[str] = None
	supplier: Optional[str] = None
	is_active: bool = True
	created_at: Optional[datetime] = None
	updated_at: Optional[datetime] = None


@dataclass
class MaterialReceipt:
	id: Optional[int] = None
	material_id: Optional[int] = None
	quantity: Optional[int] = None
	received_by: Optional[int] = None
	supplier: Optional[str] = None
	notes: Optional[str] = None
	received_at: Optional[datetime] = None


@dataclass
class IssuedItem:
	id: Optional[int] = None
	request_id: Optional[str] = None
	material_id: Optional[int] = None
	quantity: Optional[int] = None
	issued_by: Optional[int] = None
	issued_to: Optional[int] = None
	issued_at: Optional[datetime] = None


@dataclass
class InventoryTransaction:
	id: Optional[int] = None
	request_id: Optional[str] = None
	material_id: Optional[int] = None
	change_type: Optional[str] = None
	quantity: Optional[int] = None
	unit_price: Optional[float] = None
	total_price: Optional[float] = None
	performed_by: Optional[int] = None
	performed_role: Optional[str] = None
	created_at: Optional[datetime] = None


@dataclass
class EquipmentRequest:
	id: Optional[int] = None
	technician_id: Optional[int] = None
	equipment_type: Optional[str] = None
	quantity: Optional[int] = None
	reason: Optional[str] = None
	status: str = "pending"
	approved_by: Optional[int] = None
	created_at: Optional[datetime] = None
	updated_at: Optional[datetime] = None


@dataclass
class TechnicianLocation:
	technician_id: Optional[int] = None
	latitude: Optional[float] = None
	longitude: Optional[float] = None
	updated_at: Optional[datetime] = None


@dataclass
class RequestMaterial:
	id: Optional[int] = None
	request_id: Optional[str] = None
	material_id: Optional[int] = None
	quantity: Optional[int] = None
	unit: str = "pcs"
	created_at: Optional[datetime] = None


# ===== Chat / Call / Help =====
@dataclass
class ChatSession:
	id: Optional[int] = None
	user_id: Optional[int] = None
	operator_id: Optional[int] = None
	status: str = "active"
	created_at: Optional[datetime] = None
	closed_at: Optional[datetime] = None


@dataclass
class ChatMessage:
	id: Optional[int] = None
	session_id: Optional[int] = None
	sender_id: Optional[int] = None
	message_text: Optional[str] = None
	message_type: str = "text"
	created_at: Optional[datetime] = None


@dataclass
class CallLog:
	id: Optional[int] = None
	user_id: Optional[int] = None
	phone_number: Optional[str] = None
	duration: int = 0
	result: Optional[str] = None
	notes: Optional[str] = None
	created_by: Optional[int] = None
	created_at: Optional[datetime] = None


@dataclass
class HelpRequest:
	id: Optional[int] = None
	technician_id: Optional[int] = None
	help_type: Optional[str] = None
	description: Optional[str] = None
	status: str = "pending"
	priority: str = Priority.MEDIUM.value
	assigned_to: Optional[int] = None
	resolution: Optional[str] = None
	created_at: Optional[datetime] = None
	updated_at: Optional[datetime] = None
	resolved_at: Optional[datetime] = None


# ===== Audit / Analytics =====
@dataclass
class AuditLog:
	id: Optional[int] = None
	actor_user_id: Optional[int] = None
	actor_role: Optional[str] = None
	action: Optional[str] = None
	entity_type: Optional[str] = None
	entity_id: Optional[str] = None
	request_id: Optional[str] = None
	target_user_id: Optional[int] = None
	channel: Optional[str] = None
	params: Dict[str, Any] = field(default_factory=dict)
	before_data: Optional[Dict[str, Any]] = None
	after_data: Optional[Dict[str, Any]] = None
	status: Optional[str] = None
	error_message: Optional[str] = None
	source_ip: Optional[str] = None
	user_agent: Optional[str] = None
	message_id: Optional[int] = None
	correlation_id: Optional[str] = None
	session_id: Optional[str] = None
	created_at: Optional[datetime] = None


@dataclass
class ClientSelectionData:
	id: Optional[int] = None
	search_method: Optional[str] = None
	search_value: Optional[str] = None
	client_id: Optional[int] = None
	new_client_data: Dict[str, Any] = field(default_factory=dict)
	verified: bool = False
	created_by: Optional[int] = None
	session_id: Optional[str] = None
	created_at: Optional[datetime] = None


@dataclass
class ApplicationAlert:
	id: Optional[int] = None
	alert_id: Optional[str] = None
	rule_id: Optional[str] = None
	alert_type: Optional[str] = None
	severity: Optional[str] = None
	title: Optional[str] = None
	message: Optional[str] = None
	data: Dict[str, Any] = field(default_factory=dict)
	channels: List[str] = field(default_factory=list)
	recipients: List[str] = field(default_factory=list)
	created_at: Optional[datetime] = None
	sent_at: Optional[datetime] = None
	delivery_status: Dict[str, Any] = field(default_factory=dict)
	acknowledged: bool = False
	acknowledged_by: Optional[int] = None
	acknowledged_at: Optional[datetime] = None


@dataclass
class AlertRule:
	id: Optional[int] = None
	rule_id: Optional[str] = None
	name: Optional[str] = None
	description: Optional[str] = None
	alert_type: Optional[str] = None
	threshold_config: Dict[str, Any] = field(default_factory=dict)
	frequency: Optional[str] = None
	channels: List[str] = field(default_factory=list)
	recipients: List[str] = field(default_factory=list)
	is_active: bool = True
	created_at: Optional[datetime] = None
	updated_at: Optional[datetime] = None
	last_triggered: Optional[datetime] = None
	trigger_count: int = 0


@dataclass
class ApplicationStatisticsCache:
	id: Optional[int] = None
	cache_key: Optional[str] = None
	period_days: Optional[int] = None
	source_filter: Optional[str] = None
	role_filter: Optional[str] = None
	statistics_data: Dict[str, Any] = field(default_factory=dict)
	created_at: Optional[datetime] = None
	expires_at: Optional[datetime] = None


@dataclass
class ApplicationTrackingReport:
	id: Optional[int] = None
	report_id: Optional[str] = None
	report_type: Optional[str] = None
	period: Optional[str] = None
	format_type: Optional[str] = None
	generated_by: Optional[int] = None
	report_data: Dict[str, Any] = field(default_factory=dict)
	summary_data: Dict[str, Any] = field(default_factory=dict)
	file_path: Optional[str] = None
	created_at: Optional[datetime] = None
	expires_at: Optional[datetime] = None