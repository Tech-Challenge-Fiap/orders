from app import app
from flask import request
from pydantic import ValidationError
from system.application.exceptions.client_exceptions import ClientAlreadyExistsError, ClientDoesNotExistError
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.usecase import client_usecase
from system.application.dto.requests.client_request import CreateClientRequest
from system.infrastructure.adapters.decorators.jwt_decorator import require_auth

@app.route("/create_client", methods=["POST"])
# @require_auth
def create_client():
    try:
        create_client_request = CreateClientRequest(**request.get_json())
    except ValidationError as ex:
        return ex.errors(), 400
    try:
        client = client_usecase.CreateClientUseCase.execute(request=create_client_request)
    except ClientAlreadyExistsError:
        return {"error": "This Client already exists"}, 400
    except InfrastructureError:
        return {"error": "Internal Error"}, 500
    return client.response


@app.route("/get_client/<cpf>", methods=["GET"])
# @require_auth
def get_client_by_cpf(cpf):
    try:
        client = client_usecase.GetClientByCPFUseCase.execute(cpf=cpf)
    except ClientDoesNotExistError:
        return {"error": "This Client does not exist"}, 404
    except InfrastructureError:
        return {"error": "Internal Error"}, 500
    return client.response


@app.route("/get_clients/", methods=["GET"])
# @require_auth
def get_clients():
    try:
        clients = client_usecase.GetAllClientsUseCase.execute()
        clients_list = [vars(client) for client in clients.response]
    except InfrastructureError:
        return {"error": "Internal Error"}, 500
    return clients_list


@app.route("/delete_client/<cpf>", methods=["DELETE"])
# @require_auth
def delete_client(cpf):
    try:
        client_usecase.DeleteClientUseCase.execute(cpf=cpf)
        return '', 204
    except InfrastructureError:
        return {"error": "Internal Error"}, 500
