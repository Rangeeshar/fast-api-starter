"""
Claim service layer
===================
- What needs to be done if there is a failure in either service and steps need to be unwinded.

We can handle this scenario if we add a queueing system to first receive a request and multiple
worker system which can take it from the queue and process it making sure at any given point our
process/event/job is processed.

Assuming all the system crashed we could spin up a new listener all together for this queue to
manage this scenario

Assuming we have launched multiple instances of payment service and claim process service,
I also propose 2 queues one to receive claim process request and another to push net fee
event request at any given point if one microservice failed, others can take up and work
their task

If the service failed during the processing that can also be handled as the queue won't be receiving an ack,
and it would be put in another dead queue after timeout and a notification can be sent if n number of retries failed
by another sync service which takes up from dead queue and process it.


- Multiple instances of either service are running concurrently to handle a large volume of claims.

Same as above a simple managed queue service like SQS or kafka cluster will be able to handle this
We just have to spin up multiple instances of Our payment and claim service to make sure our event gets
processed from the queue

"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from http import HTTPStatus

from app.api.v1.claim.validation import validate_fields
from app.database.postgres.model.claim import Claim
from app.database.postgres.repository.claim import claim_repository
from app.services.v1.claim.claim_schema import ClaimRequest, ClaimResponse
from app.common.api_error import ErrorCode
from app.common.api_exceptions import RequestError


def create_claim(claim_request: ClaimRequest, db: Session) -> Claim:
    """
    Function to create a new claim, calculate netfee etc.

    :param claim_request: request payload
    :param db: db session for performing db operation
    :return: claim data which was created inside DB
    """
    claim: Claim = Claim()
    validate_fields(
        [
            {"name": "submitted_procedure", "value": claim_request.submitted_procedure},
            {"name": "provider_npi", "value": claim_request.provider_npi},
        ]
    )
    claim.service_date = claim_request.service_date
    claim.submitted_procedure = claim_request.submitted_procedure
    claim.quadrant = claim_request.quadrant
    claim.plan_or_group = claim_request.plan_or_group
    claim.subscriber = claim_request.subscriber
    claim.provider_npi = claim_request.provider_npi
    claim.provider_fee = claim_request.provider_fee
    claim.allowed_fee = claim_request.allowed_fee
    claim.member_coinsurance = claim_request.member_coinsurance
    claim.member_copay = claim_request.member_copay
    # Publish the net fee via an event so another service called payment can use it for its own purpose.
    # We can use kafka to publish it as it makes sure to receive ack and checks offset of sent vs received.
    # We could run a sync service which checks and syncs if the data is not in sync.
    claim.net_fee = (
        claim_request.provider_fee
        + claim_request.member_coinsurance
        + claim_request.member_copay
        - claim_request.allowed_fee
    )
    claim: Claim = claim_repository.create(db=db, obj_in=claim)
    return claim


def get_claims(db: Session) -> List[ClaimResponse]:
    """
    Fetch all claims
    :param db: db session
    :return: All claims present in DB or Empty
    """
    claims: Optional[List[Claim]] = claim_repository.get(db=db)
    return claims


def get_claim_by_id(_id: UUID, db: Session) -> Claim:
    """
    Get claims by id
    :param _id: claim id to fetch the matching data
    :param db: db session for the same
    :return: A matching record if matched or Not found error
    """
    claim: Optional[Claim] = claim_repository.get_by_id(db=db, id=_id)
    if not claim:
        raise RequestError(
            status_code=HTTPStatus.NOT_FOUND,
            error_code=ErrorCode.INCORRECT_CLAIM_ID,
            error_msg="Claim Not Found",
        )
    return claim


def delete_claim_by_id(_id: UUID, db: Session) -> None:
    """
    Delete claim by given claim id
    :param _id: claim id to delete
    :param db: db session
    :return: none
    """
    validate_claim_id(_id=_id, db=db)
    claim_repository.delete_by_id(db=db, id=_id)


def validate_claim_id(_id: UUID, db: Session) -> None:
    """
    Validate the current claim ID
    :param _id: validating claim id
    :param db: session of db
    :return: none if all good or not found error
    """
    claim: Optional[Claim] = claim_repository.get_by_id(db=db, id=_id)
    if not claim:
        raise RequestError(
            status_code=HTTPStatus.NOT_FOUND, error_code=ErrorCode.INCORRECT_CLAIM_ID
        )


def update_claim(_id: UUID, claim_request: ClaimRequest, db) -> Claim:
    """
    Updates the claim (assuming full updated payload to be sent)
    :param claim_request: Payload of claim which is updated
    :param _id: id of the claim to update
    :param db: db session
    :return: updated claim
    """
    claim: Optional[Claim] = claim_repository.get_by_id(db=db, id=_id)
    validate_fields(
        [
            {"name": "submitted_procedure", "value": claim_request.submitted_procedure},
            {"name": "provider_npi", "value": claim_request.provider_npi},
        ]
    )
    claim.service_date = claim_request.service_date
    claim.submitted_procedure = claim_request.submitted_procedure
    claim.quadrant = claim_request.quadrant
    claim.plan_or_group = claim_request.plan_or_group
    claim.subscriber = claim_request.subscriber
    claim.provider_npi = claim_request.provider_npi
    claim.provider_fee = claim_request.provider_fee
    claim.allowed_fee = claim_request.allowed_fee
    claim.member_coinsurance = claim_request.member_coinsurance
    claim.member_copay = claim_request.member_copay
    # Publish the net fee via an event so another service called payment can use it for its own purpose.
    # We can use kafka to publish it as it makes sure to receive ack and checks offset of sent vs received.
    # We could run a sync service which checks and syncs if the data is not in sync.
    claim.net_fee = (
        claim_request.provider_fee
        + claim_request.member_coinsurance
        + claim_request.member_copay
        - claim_request.allowed_fee
    )
    claim: Claim = claim_repository.update(db=db, db_obj=claim)
    return claim
