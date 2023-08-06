import responses
from requests import Session

from fhir_starter.audit_client import AuditClient
from fhir_starter.audit_messages import DicomAuditEventType, AuditOutcome, AuditInfo


@responses.activate
def test_log_dicom_transfer_should_post_audit_event_to_configured_endpoint():
    target_url = 'http://localhost/fhir'
    responses.add(method='POST', url=target_url)

    audit_client = AuditClient(target_url, Session())
    audit_client.log_dicom_study_event(
        AuditInfo(type=DicomAuditEventType.INSTANCES_TRANSFERRED, outcome=AuditOutcome.SUCCESS,
                  action='C', study_instance_uid='1.2.3',
                  patient_id='patid',
                  requesting_user='localsystem', source_system='Orthanc', receiver='pacs'))
