"""
Provide status views.
"""
from typing import Union
from uuid import UUID

from fastapi import (
    APIRouter,
    Response,
    status,
)

from src.common.schemas.common import (
    DetailsResponse,
    ErrorResponse,
)
from src.general.routes import GeneralRoutesPrefixes
from src.general.schemas.task_status import TaskStatusModel


router = APIRouter()


@router.get(
    GeneralRoutesPrefixes.health_check,
    tags=['Status'],
    response_model=DetailsResponse,
    status_code=status.HTTP_200_OK,
)
def health_check() -> DetailsResponse:
    """
    Health check endpoint.

    Returns:
        Response showing whether server is alive.
    """
    return DetailsResponse(details='UP')


@router.get(
    GeneralRoutesPrefixes.task_status,
    tags=['Status'],
    responses={
        status.HTTP_200_OK: {'model': TaskStatusModel},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
    response_model=Union[TaskStatusModel, ErrorResponse],
)
async def get_status(uuid: UUID, response: Response) -> Union[TaskStatusModel, ErrorResponse]:
    """
    Endpoint for check status of task action by unique ID.
    Args:
        uuid: unique ID of the task action.
        response: Response instance.

    Returns:
        Response with task status.
    """
    transfer_status = await TaskStatusModel.get_from_redis(uuid=uuid)

    if transfer_status is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=f'Task with UUID {uuid} does not exist.')

    return transfer_status
