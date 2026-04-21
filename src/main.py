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
# server = "expired-rsa-dv.ssl.com"
# server = "http://google.com/404"
server = "https://expired.badssl.com/"

def run_test() -> None:
    """
    function to run the test, store results in database and run retry mode if it fails
    """
    monitoring_system = MonitoringSystem()

    result = monitoring_system.run_check(server)

    if result[0]:
        result =  True, analyse(result[1])

    db = DatabaseHandle("./data.db")
    db.save_result(server, result)

    if result[0]:
        return
    else:
        run_retry()


def run_retry() -> None:
    """
    function to run retry mode in case first try failed
    """
    #sleep(300) #5 min wait used for regular operation
    sleep(300)

    monitoring_system = MonitoringSystem()

    result = monitoring_system.run_check(server)

    if result[0]:
        result = True, analyse(result[1])

    db = DatabaseHandle("./data.db")
    db.save_result(server, result)

    past_results = db.get_recent(10, server)

    #only send an email if the error still persists and the problem has not been reported previously
    if result[0] or  (len(past_results) >= 3 and not past_results[2].is_success):
        print("no email send early exit")
        return

    NotificationService().generate_and_send_report(results=past_results, server_url=server, http_code=result[1].args[0][0], http_description=result[1].args[0][1], )

def generate_report() -> None:
    """
    function to generate report from past results
    """
    db = DatabaseHandle("./data.db")
    past_results = db.get_recent(10, server)
    NotificationService().generate_and_send_report(results=past_results, server_url=server,http_code="NONE - REPORT",http_description="NONE - REPORT" )

def debug() -> None:
    """
    function to experiment with, debugging mode
    """
    db = DatabaseHandle("./data.db")
    past_results = db.get_recent(10, server)
    print(past_results[0])
    print(type(past_results[1]))
    print(past_results[1])
    print(past_results[1].is_success)
    print(past_results[2])
    print(past_results[2].is_success)

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
        generate_report()
    elif args.mode == "debug":
        debug()
    else:
        print("invalid mode")


if __name__ == "__main__":
    main()
