#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import time
from typing import Any

import requests

import cr_api_client.core_api_client as core_api_client


# Configuration access to Cyber Range endpoint
PROVISIONING_API_URL = "http://127.0.0.1:5003"
CA_CERT_PATH = None  # Expect a path to CA certs (see: https://requests.readthedocs.io/en/master/user/advanced/)
CLIENT_CERT_PATH = None  # Expect a path to client cert (see: https://requests.readthedocs.io/en/master/user/advanced/)
CLIENT_KEY_PATH = None  # Expect a path to client private key (see: https://requests.readthedocs.io/en/master/user/advanced/)


# -------------------------------------------------------------------------- #
# Internal helpers
# -------------------------------------------------------------------------- #


def __get(route: str, **kwargs: str) -> Any:
    return requests.get(
        f"{PROVISIONING_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def __post(route: str, **kwargs: str) -> Any:
    return requests.post(
        f"{PROVISIONING_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def __put(route: str, **kwargs: str) -> Any:
    return requests.put(
        f"{PROVISIONING_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def __delete(route: str, **kwargs: str) -> Any:
    return requests.delete(
        f"{PROVISIONING_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


# -------------------------------------------------------------------------- #


#
# 'aging' related functions
#
def _aging_generate_validate_input_file(input_file: str) -> None:
    if os.path.exists(input_file) is not True:
        raise Exception("The provided path does not exist: '{}'".format(input_file))

    if os.path.isfile(input_file) is not True:
        raise Exception("The provided path is not a file: '{}'".format(input_file))

    if os.access(input_file, os.R_OK) is not True:
        raise Exception("The provided file is not readable: '{}'".format(input_file))


def _aging_generate_read_yaml_file(yaml_configuration_file: str) -> str:
    with open(yaml_configuration_file, "r") as fd:
        yaml_content = fd.read()
        return yaml_content


def aging_execute(aging_configuration_file: str, id_simulation: int) -> None:
    """Process YAML configuration file and generate a new aging
    chronology.

    """

    print(f"[+] Starting provisioning of simulation ID {id_simulation}")

    # Check simulation is running
    simulation_dict = core_api_client.fetch_simulation(id_simulation)
    simulation_status = simulation_dict["status"]
    if simulation_status != "RUNNING":
        raise Exception(
            "The simulation {id_simulation} should have is status RUNNING "
            "(current status is {current_status}) in order to generate aging "
            "chronology. Try the command 'cyber_range simu_run {id_simulation}' "
            "to start the simulation.".format(
                id_simulation=id_simulation, current_status=simulation_status
            )
        )

    # Validate input file
    _aging_generate_validate_input_file(aging_configuration_file)

    # Open and read YAML input files
    yaml_aging_config = _aging_generate_read_yaml_file(aging_configuration_file)

    data = json.dumps(
        {"idSimulation": id_simulation, "provisioningYAML": yaml_aging_config}
    )

    result = __post(
        "/provisioning/start_provisioning",
        data=data,
        headers={"Content-Type": "application/json"},
    )

    if result.status_code != 200:
        raise Exception(
            "Cannot start scenario at scenario API. "
            "Status code: '{}'. Error message: '{}'".format(
                result.status_code, result.json()["message"]
            )
        )

    # Wait for the operation to be completed in backend
    current_status = ""
    while True:
        # Sleep before next iteration
        time.sleep(2)

        print(f"    [+] Currently provisioning simulation ID '{id_simulation}'...")

        result = __get("/provisioning/status_provisioning")

        result.raise_for_status()

        result = result.json()

        if "status" in result:
            current_status = result["status"]

            if current_status == "ERROR":
                error_message = result["error_msg"]
                raise Exception(
                    "Error durring simulation operation: '{}'".format(error_message)
                )
            elif current_status == "DONE":
                # Operation has ended
                break

    print(f"[+] Provisioning on simulation ID '{id_simulation}' was correctly executed")
