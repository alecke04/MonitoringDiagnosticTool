# main.py — application entry point
# Parses CLI arguments and dispatches to the appropriate commands
# Run with: python src/main.py <command> [args]
import argparse
from time import sleep

from database import DatabaseHandle

from monitoring import *
from utils.analysis import analyse
from notifications.email_service import NotificationService
import time


#from SCons.Tool.ninja_tool.ninja_scons_daemon import server_thread

def run_test() -> None:
    monitoring_system = MonitoringSystem()
    #server = "expired-rsa-dv.ssl.com"
    #server = "http://google.com/404"
    server = "https://httpbin.io/delay/60"
    result = monitoring_system.run_check(server)

    if result[0]:
        result =  True, analyse(result[1])

    db = DatabaseHandle("./data.db")
    db.save_result(server, result)

    if result[0]:
        return
    else:
        run_retry(server)


def run_retry(server:str) -> None:
    sleep(300)

    monitoring_system = MonitoringSystem()

    result = monitoring_system.run_check(server)

    if result[0]:
        result = True, analyse(result[1])

    db = DatabaseHandle("./data.db")
    db.save_result(server, result)

    past_results = db.get_recent(10, server)

    if result[0]:
    #if result[0] or past_results[0]:
        print("no email send early exit")
        return

    NotificationService().generate_and_send_report(results=past_results, server_url=server, http_code=result[1].args[0][0], http_description=result[1].args[0][1], )

def main():
    """
    Parses command-line arguments and calls the appropriate command function.
    """

    parser = argparse.ArgumentParser(description="program to load and assess model")

    desc_mode = "define the current mode"
    parser.add_argument("mode", type=str, help=desc_mode)

    args = parser.parse_args()

    if args.mode == "help":
        print("help page")
    elif args.mode == "run_test":
        run_test()
    elif args.mode == "generate_report":
        pass
    else:
        print("invalid mode")


if __name__ == "__main__":
    main()
