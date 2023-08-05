"""

"""
from requests import Session

from fhir_starter import audit_messages


class AuditClient:
    def __init__(self, fhir_base_url, session: Session()):
        self.fhir_base_url = fhir_base_url
        self.session = session

    def log_dicom_study_event(self, audit_info: audit_messages.AuditInfo):
        self._post(audit_messages.create_dicom_study_audit_message(audit_info))

    def _post(self, message):
        self.session.post(self.fhir_base_url, json=message)
