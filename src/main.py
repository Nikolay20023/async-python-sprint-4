from fastapi import FastAPI, Request, Response, status
import uvicorn
from fastapi.responses import ORJSONResponse
import ipaddress
import logging

from api.v1 import variables_root
from api.v1 import base
from core.config import AppSettings


setting = AppSettings()


app = FastAPI(
    title=setting.app_title,
    redoc_url=None,
    default_response_class=ORJSONResponse,
    openapi_url='/api/openapi.json'
)


app.include_router(base.router, prefix='/api/v1')


@app.middleware("http")
async def add_middleware_black_list(
    request: Request,
    call_next
):
    client_ip = request.client.host
    for subnet in variables_root.BLACKLISTED_SUBNETS:
        logging.info(subnet)
        logging.info(ipaddress.ip_address(client_ip))
        if ipaddress.ip_address(client_ip) in ipaddress.ip_network(subnet):
            return Response(status_code=status.HTTP_403_FORBIDDEN)
    response = await call_next(request)
    return response

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=setting.project_host,
        port=setting.project_port
    )
