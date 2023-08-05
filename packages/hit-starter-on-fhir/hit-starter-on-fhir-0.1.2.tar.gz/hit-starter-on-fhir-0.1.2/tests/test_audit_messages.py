#!/usr/bin/env python
import datetime

from fhir.resources.auditevent import AuditEvent

from fhir_starter import audit_messages
from fhir_starter.audit_messages import AuditOutcome, DicomAuditEventType


def test_shall_create_audit_event_shall_contain_required_fields():
    info = audit_messages.AuditInfo(type=DicomAuditEventType.INSTANCES_TRANSFERRED, outcome=AuditOutcome.SUCCESS,
                                    action='C', study_instance_uid='1.2.3',
                                    patient_id='patid',
                                    requesting_user='localsystem', source_system='Orthanc', receiver='pacs')
    audit_message = audit_messages.create_dicom_study_audit_message(info)

    event = AuditEvent.parse_raw(audit_message)

    assert event.type.code == '110104'
    assert event.outcome == '0'
    assert event.recorded < datetime.datetime.now(datetime.timezone.utc)
    assert event.action == 'C'

    assert event.source.observer.type == 'Device'
    assert event.source.observer.identifier.value == 'Orthanc'

    study = event.entity[0].what

    assert study.identifier.value == '1.2.3'

    patient = event.entity[1].what

    assert patient.identifier.value == 'patid'

    source = event.agent[0]

    assert source.requestor
    assert source.who.identifier.value == 'localsystem'

    dest = event.agent[1]

    assert not dest.requestor
    assert dest.who.identifier.value == 'pacs'


def test_export_audit_event_shall_contain_called_ae_title_in_receiver():
    # TODO: to be implemented
    pass


def test_query_audit_event_shall_contain_http_user_in_requestor():
    # TODO: to be implemented
    pass


def test_import_audit_event_shall_contain_calling_ae_title():
    # TODO: to be implemented
    pass
