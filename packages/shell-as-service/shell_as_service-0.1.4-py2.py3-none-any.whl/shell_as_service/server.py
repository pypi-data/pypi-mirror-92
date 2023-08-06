import sys
import threading
import time
from typing import Optional

import jsonpickle
import xmltodict
from flask import Flask, request
from werkzeug.serving import BaseWSGIServer, make_server

sys.path += ["."]
from . import driver

app = Flask(__name__)


def _get_driver():
    with open("drivermetadata.xml") as fp:
        data = xmltodict.parse(fp.read())
    driver_name = data["Driver"]["@MainClass"].rsplit(".", 1)[-1]
    return getattr(driver, driver_name)()


driver_inst = _get_driver()
time_lock = threading.Lock()
last_time_executed = time.time()
server: Optional[BaseWSGIServer] = None


@app.route("/_is_alive", methods=["POST"])
def _is_alive():
    with time_lock:
        global last_time_executed
        last_time_executed = time.time()

    return jsonpickle.encode({"response": True})


@app.route("/<method_name>", methods=["POST"])
def run_driver_methods(method_name):
    with time_lock:
        global last_time_executed
        last_time_executed = time.time()

    method = getattr(driver_inst, method_name)
    kwargs = jsonpickle.decode(request.json)
    resp = method(**kwargs)
    return jsonpickle.encode({"response": resp})


def check_last_time_executed():
    while time.time() - last_time_executed < 60:
        delay = int(60 - (time.time() - last_time_executed) + 1)
        if delay > 0:
            time.sleep(delay)
    if server is not None:
        server.shutdown()


def main():
    global server

    server = make_server("0.0.0.0", 5000, app)
    service_thread = threading.Thread(target=server.serve_forever)
    check_service_thread = threading.Thread(target=check_last_time_executed)

    service_thread.start()
    check_service_thread.start()

    service_thread.join()
    check_service_thread.join()


main()
