"""Word Document queries - placeholder.

- insert/update/select word_documents
"""
from typing import Any, Dict, List, Optional

from .db_router import DBRouter

router = DBRouter()


async def upsert_word_document(region_code: str, request_id: str, document_type: str,
		payload: Dict[str, Any]) -> int:
	"""Upsert by (request_id, document_type). Returns id."""
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		row = await conn.fetchrow(
			"""
			INSERT INTO word_documents(
				request_id, document_type, document_data, file_path, created_by,
				application_date, technician_fio, contract_number, service_order_number,
				organization_name, accepted_by_fio, diagnosis_result, installed_equipment,
				installation_address, completion_date, client_rating, client_comment, approvers,
				service_type, problem_description, work_performed, replaced_parts, result,
				operator_fio, client_fio, client_phone, consultation_date
			) VALUES (
				$1,$2, COALESCE($3,'{}'::jsonb), $4, $5,
				$6,$7,$8,$9,
				$10,$11,$12,$13,
				$14,$15,$16,$17,$18,
				$19,$20,$21,$22,$23,
				$24,$25,$26,$27
			)
			ON CONFLICT (request_id, document_type) DO UPDATE SET
				document_data = COALESCE(EXCLUDED.document_data, word_documents.document_data),
				file_path = COALESCE(EXCLUDED.file_path, word_documents.file_path),
				created_by = COALESCE(EXCLUDED.created_by, word_documents.created_by),
				application_date = COALESCE(EXCLUDED.application_date, word_documents.application_date),
				technician_fio = COALESCE(EXCLUDED.technician_fio, word_documents.technician_fio),
				contract_number = COALESCE(EXCLUDED.contract_number, word_documents.contract_number),
				service_order_number = COALESCE(EXCLUDED.service_order_number, word_documents.service_order_number),
				organization_name = COALESCE(EXCLUDED.organization_name, word_documents.organization_name),
				accepted_by_fio = COALESCE(EXCLUDED.accepted_by_fio, word_documents.accepted_by_fio),
				diagnosis_result = COALESCE(EXCLUDED.diagnosis_result, word_documents.diagnosis_result),
				installed_equipment = COALESCE(EXCLUDED.installed_equipment, word_documents.installed_equipment),
				installation_address = COALESCE(EXCLUDED.installation_address, word_documents.installation_address),
				completion_date = COALESCE(EXCLUDED.completion_date, word_documents.completion_date),
				client_rating = COALESCE(EXCLUDED.client_rating, word_documents.client_rating),
				client_comment = COALESCE(EXCLUDED.client_comment, word_documents.client_comment),
				approvers = COALESCE(EXCLUDED.approvers, word_documents.approvers),
				service_type = COALESCE(EXCLUDED.service_type, word_documents.service_type),
				problem_description = COALESCE(EXCLUDED.problem_description, word_documents.problem_description),
				work_performed = COALESCE(EXCLUDED.work_performed, word_documents.work_performed),
				replaced_parts = COALESCE(EXCLUDED.replaced_parts, word_documents.replaced_parts),
				result = COALESCE(EXCLUDED.result, word_documents.result),
				operator_fio = COALESCE(EXCLUDED.operator_fio, word_documents.operator_fio),
				client_fio = COALESCE(EXCLUDED.client_fio, word_documents.client_fio),
				client_phone = COALESCE(EXCLUDED.client_phone, word_documents.client_phone),
				consultation_date = COALESCE(EXCLUDED.consultation_date, word_documents.consultation_date)
			RETURNING id
			""",
			request_id, document_type,
			payload.get("document_data"),
			payload.get("file_path"),
			payload.get("created_by"),
			payload.get("application_date"),
			payload.get("technician_fio"),
			payload.get("contract_number"),
			payload.get("service_order_number"),
			payload.get("organization_name"),
			payload.get("accepted_by_fio"),
			payload.get("diagnosis_result"),
			payload.get("installed_equipment"),
			payload.get("installation_address"),
			payload.get("completion_date"),
			payload.get("client_rating"),
			payload.get("client_comment"),
			payload.get("approvers"),
			payload.get("service_type"),
			payload.get("problem_description"),
			payload.get("work_performed"),
			payload.get("replaced_parts"),
			payload.get("result"),
			payload.get("operator_fio"),
			payload.get("client_fio"),
			payload.get("client_phone"),
			payload.get("consultation_date"),
		)
		return int(row["id"]) if row else 0


async def get_word_document(region_code: str, request_id: str, document_type: str) -> Optional[Dict[str, Any]]:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		row = await conn.fetchrow(
			"SELECT * FROM word_documents WHERE request_id=$1 AND document_type=$2",
			request_id, document_type,
		)
		return dict(row) if row else None


async def list_word_documents(region_code: str, request_id: str) -> List[Dict[str, Any]]:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		rows = await conn.fetch(
			"SELECT * FROM word_documents WHERE request_id=$1 ORDER BY generated_at DESC",
			request_id,
		)
		return [dict(r) for r in rows]