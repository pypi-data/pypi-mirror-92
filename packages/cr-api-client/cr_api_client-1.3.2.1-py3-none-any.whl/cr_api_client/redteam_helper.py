# -*- coding: utf-8 -*-
import json
import time
from typing import Any

import requests


# Configuration access to Cyber Range endpoint
REDTEAM_API_URL = "http://127.0.0.1:5004"
# Expect a path to CA certs (see:
# https://requests.readthedocs.io/en/master/user/advanced/)
CA_CERT_PATH = None
# Expect a path to client cert (see:
# https://requests.readthedocs.io/en/master/user/advanced/)
CLIENT_CERT_PATH = None
# Expect a path to client private key (see:
# https://requests.readthedocs.io/en/master/user/advanced/)
CLIENT_KEY_PATH = None

# Module variables
attack_list = {}


# -------------------------------------------------------------------------- #
# Internal helpers
# -------------------------------------------------------------------------- #


def __get(route: str, **kwargs: str) -> Any:
    return requests.get(
        f"{REDTEAM_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def __post(route: str, **kwargs: str) -> Any:
    return requests.post(
        f"{REDTEAM_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def __put(route: str, **kwargs: str) -> Any:
    return requests.put(
        f"{REDTEAM_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


def __delete(route: str, **kwargs: str) -> Any:
    return requests.delete(
        f"{REDTEAM_API_URL}{route}",
        verify=CA_CERT_PATH,
        cert=(CLIENT_CERT_PATH, CLIENT_KEY_PATH),
        **kwargs,
    )


# -------------------------------------------------------------------------- #


def reset_redteam() -> None:
    result = __delete("/api/platform")
    result.raise_for_status()
    result = result.json()


def execute_attack(idAttack: int, name: str) -> None:
    url = REDTEAM_API_URL + "/api/attack/" + str(idAttack)

    payload = {
        "action": "start",
    }
    headers = {"Content-Type": "application/json"}
    response = requests.__put(url, headers=headers, data=json.dumps(payload))
    print(response.json())
    idAttack = response.json().get("idAttack", None)
    print(idAttack)
    print(response.json().get("started_date", None) + " : " + name + " : Started")

    if idAttack is not None:
        waiting_attack(idAttack)


def waiting_attack(id_attack: str) -> None:
    url = REDTEAM_API_URL + "/api/attack/" + str(id_attack)
    payload = {}
    headers = {}

    response = __get(url, headers=headers, data=payload)
    status = response.json().get("status", None)
    while status != "success":
        time.sleep(1)
        response = __get(url, headers=headers, data=payload)
        status = response.json().get("status", None)
        if status == "waiting":
            break

        time.sleep(1)

    attack_list[response.json().get("worker", None)] = status

    print(
        response.json().get("last_update", None)
        + " : "
        + response.json().get("worker", None)
        + " : "
        + status
    )


def stop_satan() -> None:
    url = REDTEAM_API_URL + "/api/platform"
    payload = {}
    headers = {}

    response = __delete(url, headers=headers, data=payload)
    if response:
        print("Done")
    else:
        print(" ERROR - " + str(response.text.encode("utf8")))


def attack_in_list(attack_name: str, workers: str) -> str:
    return next((x for x in workers if x["name"] == attack_name), None)


def attack_is_possible(attack_name: str) -> str:
    print("test possible : " + attack_name)
    url = REDTEAM_API_URL + "/api/attack"
    payload = {}
    headers = {}

    response = __get(url, headers=headers, data=payload)
    attacks = response.json()
    print(attacks)

    return next((x["idAttack"] for x in attacks if x["worker"] == attack_name), None)


def execute_scenario(attacks: list) -> None:
    if attacks is not None:
        # if type(attack) == dict:
        #     name = list(attack.keys())[0]
        #     attack_list[name] = "init"
        # else:
        #     attack_list[attack] = "init"

        scheduler(attacks)


def scheduler(attack_list: list) -> None:
    print(attack_list)
    for attack in attack_list:
        print(attack)
        time.sleep(5)
        # Scenario language constraint not use currently
        if type(attack) == dict:
            name = list(attack.keys())[0]
            # requirements = attack[name]
        else:
            name = attack

        idAttack = attack_is_possible(name)
        print(idAttack)
        while idAttack is None:
            print("Attack " + name + "not available : Waiting ...")
            time.sleep(5)
            idAttack = attack_is_possible(name)
        if idAttack is not None:
            print("execution" + name)
            execute_attack(idAttack, name)
        else:
            print("Attack not available.")
            break
