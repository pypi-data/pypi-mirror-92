"""Audit events for DICOM"""

import datetime
from dataclasses import dataclass

from fhir.resources.auditevent import AuditEvent
from fhir.resources.fhirtypes import CodingType, AuditEventSourceType, IdentifierType, AuditEventAgentType, \
    AuditEventEntityType
from fhir.resources.reference import Reference


class AuditOutcome:
    SUCCESS = '0'
    MINOR_FAILURE = '4'
    SERIOUS_FAILURE = '8'
    MAJOR_FAILURE = '12'


class DicomAuditEventEntity:
    AE_TITLE = CodingType(code='110119',
                          system='http://dicom.nema.org/resources/ontology/DCM',
                          display='Station AE Title')
    STUDY_INSTANCE_UID = CodingType(code='110180', system='http://dicom.nema.org/resources/ontology/DCM',
                                    display='Study Instance UID')


class DicomAuditEventType:
    APPLICATION_ACTIVITY = CodingType(code='110100',
                                      system='http://dicom.nema.org/resources/ontology/DCM',
                                      display='Application Activity')
    AUDIT_LOG_USED = CodingType(code='110101',
                                system='http://dicom.nema.org/resources/ontology/DCM',
                                display='Audit Log Used')
    BEGIN_TRANSFERRING_INSTANCES = CodingType(code='110102',
                                              system='http://dicom.nema.org/resources/ontology/DCM',
                                              display='Begin Transferring DICOM Instances')
    INSTANCES_ACCESSED = CodingType(code='110103',
                                    system='http://dicom.nema.org/resources/ontology/DCM',
                                    display='DICOM Instances Accessed')
    INSTANCES_TRANSFERRED = CodingType(code='110104',
                                       system='http://dicom.nema.org/resources/ontology/DCM',
                                       display='DICOM Instances Transferred')
    STUDY_DELETED = CodingType(code='110105',
                               system='http://dicom.nema.org/resources/ontology/DCM',
                               display='DICOM Study Deleted')
    QUERY = CodingType(code='110112',
                       system='http://dicom.nema.org/resources/ontology/DCM',
                       display='DICOM Instances Transferred')


@dataclass
class AuditInfo:
    outcome: AuditOutcome
    type: CodingType
    action: str = 'R'  # per http://dicom.nema.org/medical/dicom/current/output/chtml/part15/sect_A.5.3.7.html
    requesting_user: str = None  # can be
    receiver: str = 'Unknown'
    source_user: str = 'Unknown'
    source_system: str = None
    remote_host: str = None
    remote_user: str = None
    destination_system: str = None
    source_service: str = None
    patient_id: str = 'Unknown'
    study_instance_uid: str = 'Unknown'


def create_dicom_study_audit_message(audit_info):
    now = datetime.datetime.now(datetime.timezone.utc)
    source = AuditEventSourceType(
        observer=Reference(type='Device', identifier=IdentifierType(value=audit_info.source_system)),
        type=[CodingType(code='4')])
    agent_requestor = AuditEventAgentType(requestor=True,
                                          who=Reference(identifier=IdentifierType(value=audit_info.requesting_user)))
    agent_receiver = AuditEventAgentType(requestor=False,
                                         who=Reference(identifier=IdentifierType(value=audit_info.receiver)))
    study = AuditEventEntityType(
        what=Reference(
            identifier=IdentifierType(
                value=audit_info.study_instance_uid,
                type={'coding': [DicomAuditEventEntity.STUDY_INSTANCE_UID]})),
        type=CodingType(code='2'), role=CodingType(code='3'),
        lifecycle=CodingType(code='1'))
    patient = AuditEventEntityType(
        what=Reference(
            identifier=IdentifierType(
                value=audit_info.patient_id,
                type={'coding': [CodingType(code='2',
                                            system='RFC-3881',
                                            display="Patient Number")]})),
        type=CodingType(code='1'), role=CodingType(code='1'),
        lifecycle=CodingType(code='1'))

    event = AuditEvent(action=audit_info.action, recorded=now, agent=[agent_requestor, agent_receiver],
                       source=source, outcome=audit_info.outcome,
                       type=audit_info.type,
                       entity=[study, patient])

    json = event.json(indent=2)
    return json
