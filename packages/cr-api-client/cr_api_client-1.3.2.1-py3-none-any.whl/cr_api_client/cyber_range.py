#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import configparser
import sys
import time

import requests

import cr_api_client.core_api_client as core_api_client
import cr_api_client.core_helper as core_helper
import cr_api_client.provisioning_helper as provisioning_helper
import cr_api_client.redteam_helper as redteam_helper
import cr_api_client.scenario_helper as scenario_helper


#
# 'status' related functions
#
def status_handler(args):
    """Get platform status."""

    print("[+] Platform status")

    # Testing Core API
    print("  [+] Core API")
    print("    [+] address: {}".format(core_api_client.CORE_API_URL))
    try:
        core_api_client.fetch_simulations()
    except requests.exceptions.ConnectionError:
        print("    [+] status: not running !")
        return
    else:
        print("    [+] status: OK")

    # Testing Virtclient API
    print("  [+] Virtclient API")
    try:
        status = core_api_client.virtclient_status()
    except Exception:
        print("    [+] status: not running !")
    else:
        print("    [+] status: OK")
        print("    [+] available slots: {}".format(status["nb_slots"]))

    # # Testing frontend
    # print("  [+] Frontend")
    # print(
    #     "    [+] Address: {}:{}".format(
    #         cyber_range_conf.frontend["listen_host"],
    #         cyber_range_conf.frontend["listen_port"],
    #     )
    # )
    # try:
    #     result = requests.get(
    #         "http://{}:{}".format(
    #             cyber_range_conf.frontend["listen_host"],
    #             cyber_range_conf.frontend["listen_port"],
    #         )
    #     )
    #     if result.status_code != 200:
    #         raise Exception("Error detected in frontend response")
    # except requests.exceptions.ConnectionError:
    #     print("    [+] Status: not running !")
    # except Exception:
    #     print("    [+] Status: not working properly !")
    #     return
    # else:
    #     print("    [+] Status: OK")


#
# 'init' related functions
#
def init_handler(args):
    """Process initialization of mysql db and snapshots path."""

    print(
        "[+] Reset virtclient (stop VMs, stop Docker containers, delete snaphots, ...)"
    )
    core_api_client.virtclient_reset()

    print("[+] Initialize database")
    core_api_client.reset_database()


#
# 'basebox_list' related functions
#
def basebox_list_handler(args):
    """List available baseboxes, for use in simulations."""
    print("[+] List of available baseboxes")
    baseboxes = core_api_client.fetch_baseboxes()

    for basebox in baseboxes:

        # Check if basebox is in local catalog
        if basebox["available"]:
            local_basebox = "yes: {}".format(basebox["path"])
        else:
            local_basebox = "no"

        print(
            "  [+] {}: {} (role: {}, {}, {}) - available? {}".format(
                basebox["id"],
                basebox["description"],
                basebox["role"],
                basebox["language"],
                basebox["operating_system"],
                local_basebox,
            )
        )


#
# 'simu_create' simulation related functions
#
def simu_create_handler(args):
    """Process YAML configuration file and request core API to create a
    new simulation.

    """

    # Parameters
    architecture_file = args.architecture_file

    # Compute elpased time
    t1 = time.time()

    id_simulation = core_helper.simu_create(architecture_file)
    print("Created simulation ID: '{}'".format(id_simulation))

    t2 = time.time()
    time_elapsed = t2 - t1
    print("[+] Time elapsed: {0:.2f} seconds".format(time_elapsed))


#
# 'aging_execute' related functions
#
def aging_execute_handler(args):
    """Process YAML configuration file and execute a new aging
    chronology (generate + play)).

    """
    # Parameters
    aging_configuration_file = args.aging_configuration_file
    id_simulation = args.id_simulation

    provisioning_helper.aging_execute(aging_configuration_file, id_simulation)


#
# 'scenario_play' simulation
#
def scenario_play_handler(args):
    """Play scenario on targeted simulation."""
    # Parameters
    id_simulation = args.id_simulation
    scenario_path = args.scenario_path

    print(
        "[+] Playing scenario '{}' on simulation id '{}'".format(
            scenario_path, id_simulation
        )
    )
    scenario_helper.scenario_play(id_simulation, scenario_path)


#
# 'scenario_status' simulation
#
def scenario_status_handler(args):
    """Get scenario status on targeted simulation."""
    # Parameters
    id_simulation = args.id_simulation

    print("[+] Get scenario status on simulation id '{}'".format(id_simulation))
    status = scenario_helper.scenario_status(id_simulation)
    print("  [+] Current status: {}".format(status["status"]))


#
# 'simu_run' simulation
#
def simu_run_handler(args):
    # Parameters
    id_simulation = args.id_simulation
    use_vm_time = not args.use_current_time

    # Compute elpased time
    t1 = time.time()

    core_helper.simu_run(id_simulation, use_vm_time)

    t2 = time.time()
    time_elapsed = t2 - t1
    print("[+] Time elapsed: {0:.2f} seconds".format(time_elapsed))

    print("[+] Simulation is running...")


#
# 'simu_status' of simulation
#
def simu_status_handler(args):
    # Parameters
    requested_simulation_id = args.id_simulation

    simulations = core_api_client.fetch_simulations()

    for simulation in simulations:
        if (
            requested_simulation_id is None
            or requested_simulation_id == simulation["id"]
        ):
            id_simulation = simulation["id"]

            print("[+] simulation id {}:".format(id_simulation))
            print("  [+] name: {}".format(simulation["name"]))
            print("  [+] status: {}".format(simulation["status"]))

            # Fetch associated machines
            machines = core_api_client.fetch_machines(id_simulation)

            print("  [+] machines:")
            for machine in machines:
                print("    [+] name: {} ({})".format(machine["name"], machine["type"]))
                print("      [+] status: {}".format(machine["status"]))
                print(
                    "      [+] machine stats: {} Mo, {} core(s)".format(
                        machine["memory_size"],
                        machine["nb_proc"],
                    )
                )

                if machine["type"] == "virtual_machine":
                    print(
                        "      [+] basebox: {}".format(
                            machine["basebox_id"],
                        )
                    )
                    print(
                        "      [+] current basebox path: {}".format(
                            machine["hard_drive"]
                        )
                    )
                    print("      [+] uuid: {}".format(machine["system_uid"]))
                    print("      [+] VNC port: {}".format(machine["vnc_port"]))
                    if machine["username"] is not None:
                        print(
                            "      [+] user account: {}:{}".format(
                                machine["username"], machine["password"]
                            )
                        )
                    else:
                        print("      [+] user account: None")
                    if machine["admin_username"] is not None:
                        print(
                            "      [+] admin account: {}:{}".format(
                                machine["admin_username"], machine["admin_password"]
                            )
                        )
                    else:
                        print("      [+] admin account: None")
                elif machine["type"] == "docker":
                    print(
                        "      [+] docker image: {}".format(
                            machine["base_image"],
                        )
                    )


#
# 'simu_pause' simulation
#
def simu_pause_handler(args):
    # Parameters
    id_simulation = args.id_simulation

    core_helper.simu_pause(id_simulation)
    print("Simulation paused")


#
# 'simu_unpause' simulation
#
def simu_unpause_handler(args):
    # Parameters
    id_simulation = args.id_simulation

    core_helper.simu_unpause(id_simulation)
    print("Simulation unpaused")


#
# 'simu_halt' simulation
#
def simu_halt_handler(args):
    # Parameters
    id_simulation = args.id_simulation

    core_helper.simu_halt(id_simulation)
    print("Simulation halted")


#
# 'simu_destroy' simulation
#
def simu_destroy_handler(args):
    # Parameters
    id_simulation = args.id_simulation

    core_helper.simu_destroy(id_simulation)
    print("Simulation destroyed")


#
# 'simu_clone' simulation
#
def simu_clone_handler(args):
    # Parameters
    id_simulation = args.id_simulation

    id_new_simulation = core_helper.simu_clone(id_simulation)
    print("Simulation cloned")
    print("Created simulation ID: '{}'".format(id_new_simulation))


#
# 'simu_tap' simulation
#
def simu_tap_handler(args):
    # Parameters
    id_simulation = args.id_simulation
    iface = args.iface

    core_helper.simu_tap(id_simulation, iface)
    print("Redirect network traffic to the tap interface")


#
# 'simu_untap' simulation
#
def simu_untap_handler(args):
    # Parameters
    id_simulation = args.id_simulation
    iface = args.iface

    core_helper.simu_untap(id_simulation, iface)
    print("Stop redirection of network traffic to the tap interface")


#
# 'simu_delete' simulation
#
def simu_delete_handler(args):
    # Parameters
    id_simulation = args.id_simulation

    core_helper.simu_delete(id_simulation)
    print("[+] VMs destroyed")
    print("[+] VMs snapshots deleted")
    print("[+] Simulation deleted from database")


def set_core_api_url(core_api_url):
    print("  [+] Using core API URL: {}".format(core_api_url))
    core_api_client.CORE_API_URL = core_api_url
    return core_api_url


def set_scenario_api_url(scenario_api_url):
    print("  [+] Using scenario API URL: {}".format(scenario_api_url))
    scenario_helper.SCENARIO_API_URL = scenario_api_url
    return scenario_api_url


def set_provisioning_api_url(provisioning_api_url):
    print("  [+] Using provisioning API URL: {}".format(provisioning_api_url))
    provisioning_helper.PROVISIONING_API_URL = provisioning_api_url
    return provisioning_api_url


def set_redteam_api_url(redteam_api_url):
    print("  [+] Using redteam API URL: {}".format(redteam_api_url))
    redteam_helper.REDTEAM_API_URL = redteam_api_url
    return redteam_api_url


def set_cacert(cacert):
    print("  [+] Using CA certs path: {}".format(cacert))
    core_api_client.CA_CERT_PATH = cacert
    scenario_helper.CA_CERT_PATH = cacert
    provisioning_helper.CA_CERT_PATH = cacert
    redteam_helper.CA_CERT_PATH = cacert
    return cacert


def set_cert(cert):
    print("  [+] Using client cert path: {}".format(cert))
    core_api_client.CLIENT_CERT_PATH = cert
    scenario_helper.CLIENT_CERT_PATH = cert
    provisioning_helper.CLIENT_CERT_PATH = cert
    redteam_helper.CLIENT_CERT_PATH = cert
    return cert


def set_key(key):
    print("  [+] Using client key path: {}".format(key))
    core_api_client.CLIENT_KEY_PATH = key
    scenario_helper.CLIENT_KEY_PATH = key
    provisioning_helper.CLIENT_KEY_PATH = key
    redteam_helper.CLIENT_KEY_PATH = key
    return key


def main():

    print("[+] Config")
    parser = argparse.ArgumentParser()

    # Manage options passed in config file
    parser.add_argument("--config", help="Configuration file")
    args, left_argv = parser.parse_known_args()
    if args.config:
        print(f"  [+] Using config file: {args.config}")
        config = configparser.SafeConfigParser()
        config.read(args.config)

    # Common debug argument
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        dest="debug_mode",
        help="Activate debug mode (not set by default)",
    )

    # Common options to access remote API
    parser.add_argument(
        "--core-url",
        dest="core_api_url",
        type=set_core_api_url,
        help="Set core API URL (default: '{}')".format(core_api_client.CORE_API_URL),
    )
    parser.add_argument(
        "--scenario-url",
        dest="scenario_api_url",
        type=set_scenario_api_url,
        help="Set scenario API URL (default: '{}')".format(
            scenario_helper.SCENARIO_API_URL
        ),
    )
    parser.add_argument(
        "--provisioning-url",
        dest="provisioning_api_url",
        type=set_provisioning_api_url,
        help="Set provisioning API URL (default: '{}')".format(
            provisioning_helper.PROVISIONING_API_URL
        ),
    )
    parser.add_argument(
        "--redteam-url",
        dest="redteam_api_url",
        type=set_redteam_api_url,
        help="Set redteam API URL (default: '{}')".format(
            redteam_helper.REDTEAM_API_URL
        ),
    )
    parser.add_argument(
        "--cacert", dest="cacert", type=set_cacert, help="Set path to CA certs"
    )
    parser.add_argument(
        "--cert", dest="cert", type=set_cert, help="Set path to client cert"
    )
    parser.add_argument(
        "--key", dest="key", type=set_key, help="Set path to client key"
    )

    subparsers = parser.add_subparsers()

    # 'status' command
    parser_status = subparsers.add_parser("status", help="Get platform status")
    parser_status.set_defaults(func=status_handler)

    # 'init' command
    parser_init = subparsers.add_parser(
        "init",
        help="Initialize database (override previous simulations!)",
    )
    parser_init.set_defaults(func=init_handler)

    # 'basebox_list' command
    parser_bb_list = subparsers.add_parser(
        "basebox_list",
        help="List available baseboxes",
    )
    parser_bb_list.set_defaults(func=basebox_list_handler)

    # -----------------------
    # --- Core/simu options
    # -----------------------

    # 'simu_create' simulation command
    parser_simu_create = subparsers.add_parser(
        "simu_create",
        help="Create a new simulation",
    )
    parser_simu_create.set_defaults(func=simu_create_handler)
    parser_simu_create.add_argument(
        "-a",
        action="store",
        required=True,
        dest="architecture_file",
        help="Input path of simulation architecture",
    )

    # 'simu_run' simulation command
    parser_simu_run = subparsers.add_parser("simu_run", help="Run a simulation")
    parser_simu_run.set_defaults(func=simu_run_handler)
    parser_simu_run.add_argument("id_simulation", type=int, help="The simulation id")
    parser_simu_run.add_argument(
        "--use_current_time",
        action="store_true",
        dest="use_current_time",
        help="Indicates that hypervisor time will be used to set VMs boot time",
    )

    # 'simu_status' simulation command
    parser_simu_status = subparsers.add_parser(
        "simu_status", help="Get status of a simulation or all simulations"
    )
    parser_simu_status.set_defaults(func=simu_status_handler)
    parser_simu_status.add_argument(
        "id_simulation", type=int, nargs="?", help="The simulation id"
    )

    # 'simu_pause' simulation command
    parser_simu_pause = subparsers.add_parser(
        "simu_pause",
        help="Pause a simulation (suspend VMs)",
    )
    parser_simu_pause.set_defaults(func=simu_pause_handler)
    parser_simu_pause.add_argument("id_simulation", type=int, help="The simulation id")

    # 'simu_unpause' simulation command
    parser_simu_unpause = subparsers.add_parser(
        "simu_unpause",
        help="Unpause a simulation (resume VMs)",
    )
    parser_simu_unpause.set_defaults(func=simu_unpause_handler)
    parser_simu_unpause.add_argument(
        "id_simulation", type=int, help="The simulation id"
    )

    # 'simu_halt' simulation command
    parser_simu_halt = subparsers.add_parser(
        "simu_halt",
        help="Halt a simulation (stop VMs and save VMs state)",
    )
    parser_simu_halt.set_defaults(func=simu_halt_handler)
    parser_simu_halt.add_argument("id_simulation", type=int, help="The simulation id")

    # 'simu_destroy' simulation command
    parser_simu_destroy = subparsers.add_parser(
        "simu_destroy",
        help="Destroy a simulation (stop VMs and delete VMs state)",
    )
    parser_simu_destroy.set_defaults(func=simu_destroy_handler)
    parser_simu_destroy.add_argument(
        "id_simulation", type=int, help="The simulation id"
    )

    # 'simu_clone' simulation command
    parser_simu_clone = subparsers.add_parser("simu_clone", help="Clone a simulation")
    parser_simu_clone.set_defaults(func=simu_clone_handler)
    parser_simu_clone.add_argument("id_simulation", type=int, help="The simulation id")

    # 'simu_delete' simulation command
    parser_simu_delete = subparsers.add_parser(
        "simu_delete",
        help="Delete a simulation",
    )
    parser_simu_delete.set_defaults(func=simu_delete_handler)
    parser_simu_delete.add_argument("id_simulation", type=int, help="The simulation id")

    # 'simu_tap' simulation command
    parser_simu_tap = subparsers.add_parser(
        "simu_tap",
        help="Redirect network traffic to the tap interface",
    )
    parser_simu_tap.set_defaults(func=simu_tap_handler)
    parser_simu_tap.add_argument("id_simulation", type=int, help="The simulation id")
    parser_simu_tap.add_argument("iface", type=str, help="The tap network interface")

    # 'simu_untap' simulation command
    parser_simu_untap = subparsers.add_parser(
        "simu_untap",
        help="Stop redirection of network traffic",
    )
    parser_simu_untap.set_defaults(func=simu_untap_handler)
    parser_simu_untap.add_argument("id_simulation", type=int, help="The simulation id")
    parser_simu_untap.add_argument("iface", type=str, help="The tap network interface")

    # -----------------------
    # --- Aging options
    # -----------------------

    # 'aging_execute' command
    parser_aging_execute = subparsers.add_parser(
        "aging_execute", help="Execute aging chronology for a simulation"
    )
    parser_aging_execute.set_defaults(func=aging_execute_handler)
    parser_aging_execute.add_argument(
        "id_simulation", type=int, help="The simulation id"
    )
    parser_aging_execute.add_argument(
        "-c",
        action="store",
        required=True,
        dest="aging_configuration_file",
        help="Input path of aging configuration",
    )

    # -----------------------
    # --- Scenario options
    # -----------------------

    # 'scenario_play' command
    parser_scenario_play = subparsers.add_parser(
        "scenario_play", help="Play scenario on a simulation"
    )
    parser_scenario_play.set_defaults(func=scenario_play_handler)
    parser_scenario_play.add_argument(
        "id_simulation", type=int, help="The simulation id"
    )
    parser_scenario_play.add_argument(
        "-i",
        action="store",
        nargs="?",
        # required=True,
        dest="scenario_path",
        help="Path of the scenario to play",
    )

    # 'scenario_status' command
    parser_scenario_status = subparsers.add_parser(
        "scenario_status", help="Get scenario status on a simulation"
    )
    parser_scenario_status.set_defaults(func=scenario_status_handler)
    parser_scenario_status.add_argument(
        "id_simulation", type=int, help="The simulation id"
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)

    # Handle parameter written in config file
    if args.config:
        for k, v in config.items("DEFAULT"):
            parser.parse_args([str(k), str(v)], args)

    # Parse remaining args from command line (overriding potential config file parameters)
    args = parser.parse_args(left_argv, args)

    args.func(args)
    sys.exit(0)


if __name__ == "__main__":
    main()
