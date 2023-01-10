from sanic import (
    Blueprint,
    json,
)
from sanic.log import logger
from sanic_openapi.openapi3 import openapi

from src.schemas.suspicion import (
    GetSuspicionSchema,
    IncrementSuspicionBody,
    IncrementSuspicionSchema,
)
from src.http_app.app_entety import Request
from src.usescases.suspicions import (
    get_user_suspicion_usecase,
    increment_suspicion_usecase,
)


routes_blueprint = Blueprint("routes")


@openapi.parameter("id", str, location="query")
@routes_blueprint.route("/get_suspicion", methods=["GET"])
async def get_suspicion(request: Request):
    """Check id for suspicion level"""
    config = request.app.config

    schema = GetSuspicionSchema()
    request_data = schema.dump(request.args)
    if schema.validate(request_data):
        return json(
            {"error": schema.validate(request_data)},
            status=500,
        )

    suspicion = await get_user_suspicion_usecase(
        id_=request_data.get("id"),
        suspicion=config.repositories.suspicion,
        transport_to_analyzer=config.repositories.transport_to_analyzer,
        logger=logger,
    )
    return json({"suspicion": suspicion})


@openapi.body(
    {"application/json": IncrementSuspicionBody},
    description="id and suspicion",
    required=True,
)
@routes_blueprint.route("/increment_suspicion", methods=["POST"])
async def increment_suspicion(request: Request):
    """Increment suspicion user by id"""
    config = request.app.config

    schema = IncrementSuspicionSchema()
    request_data = schema.dump(request.json)
    if schema.validate(request_data):
        return json(
            {"error": schema.validate(request_data)},
            status=500,
        )

    status = await increment_suspicion_usecase(
        id_=request_data.get("id"),
        level=request_data.get("suspicion"),
        suspicion=config.repositories.suspicion,
        suspicion_settings=config.settings.suspicion,
        logger=logger,
    )
    if status:
        return json({"status": "success"})
    else:
        return json({"status": "failed"})
