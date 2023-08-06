import socket
import time
from typing import Optional

import docker
import jsonpickle
import requests
from docker.errors import NotFound
from requests import ConnectionError


def execute_api_call(
    host: str, port: int, method_name: str, kwargs: Optional[dict] = None
):
    if kwargs is None:
        kwargs = {}
    url = f"http://{host}:{port}/{method_name}"
    resp = requests.post(url, json=kwargs)
    data = jsonpickle.decode(resp.content)
    return data["response"]


def _get_free_port(host) -> int:
    for port_num in range(6000, 6500):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex((host, port_num)) != 0:
                return port_num


def get_service_port(
    host: str,
    docker_client: docker.DockerClient,
    driver_name: str,
    docker_img_name: str,
):
    try:
        container = docker_client.containers.get(driver_name)
        port = int(next(iter(container.ports.values()))[0]["HostPort"])
        try:
            execute_api_call(host, port, "_is_alive")
        except Exception:
            container.remove()
            raise NotFound
    except NotFound:
        port = _get_free_port(host)
        container = docker_client.containers.run(
            docker_img_name,
            detach=True,
            remove=True,
            ports={"5000/tcp": port},
            name=driver_name,
        )
        starting = True
        while starting:
            try:
                execute_api_call(host, port, "_is_alive")
            except ConnectionError:
                time.sleep(1)
                continue
            else:
                starting = False
    return port


def _test():
    from cloudshell.shell.core.driver_context import ReservationContextDetails

    _context = ReservationContextDetails(
        "env_name",
        "env_path",
        "domain",
        "desc",
        "owner_user",
        "owner_email",
        "res_id",
        "",
        "",
        "",
    )
    docker_host = ""
    docker_user = ""
    shell_name = ""
    _kwargs = jsonpickle.encode({"context": _context})
    command_name = "shutdown"
    docker_client = docker.DockerClient(
        base_url=f"ssh://{docker_user}@{docker_host}", tls=True
    )
    port = get_service_port(docker_host, docker_client, shell_name)
    res = execute_api_call(docker_host, port, command_name, _kwargs)
    print(f"result = {res}")  # noqa


def execute_command(
    docker_user, docker_host, docker_img_name, driver_name, command_name, kwargs
):
    docker_client = docker.DockerClient(
        base_url=f"ssh://{docker_user}@{docker_host}", tls=True
    )
    port = get_service_port(docker_host, docker_client, driver_name, docker_img_name)
    res = execute_api_call(docker_host, port, command_name, kwargs)
    return res


def convert_objects(object_):
    from cloudshell.shell.core import driver_context

    cls = type(object_)
    if cls.__module__ == "contracts.driver_context":
        cls_name = cls.__name__
        new_cls = getattr(driver_context, cls_name)
        kwargs = {k: convert_objects(v) for k, v in object_.__dict__.items()}
        if cls_name == "ConnectivityContext":
            kwargs.pop("use_webapi_endpoint", None)
        new_object = new_cls(**kwargs)
    elif isinstance(object_, dict):
        new_object = {k: convert_objects(v) for k, v in object_.items()}
    elif isinstance(object_, list):
        new_object = list(map(convert_objects, object_))
    elif isinstance(object_, set):
        new_object = set(map(convert_objects, object_))
    elif isinstance(object_, tuple):
        new_object = tuple(map(convert_objects, object_))
    else:
        new_object = object_
    return new_object


def get_docker_name(driver_inst):
    return getattr(driver_inst, "DOCKER_IMG")


if __name__ == "__main__":
    _test()
