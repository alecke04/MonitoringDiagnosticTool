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


<<<<<<< HEAD
#from SCons.Tool.ninja_tool.ninja_scons_daemon import server_thread
# server = "expired-rsa-dv.ssl.com"
# server = "http://google.com/404"
server = "https://expired.badssl.com/"

def run_test() -> None:
=======
import argparse
import os
import schedule
import time

from src.database.db_handle import DatabaseHandle
from src.monitoring.monitor import MonitoringSystem
from src.models.web_server import WebServer
from src.utils.config import load_config


def cmd_add(args) -> None:
>>>>>>> main
    """
    function to run the test, store results in database and run retry mode if it fails
    """
<<<<<<< HEAD
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
=======
    web_server = WebServer(url=args.url, email=args.email)
    db = DatabaseHandle()
    db.addTarget(web_server, email_recipient=args.email)
    print(f"Added {args.url} with notification email {args.email} to monitoring list.")
>>>>>>> main


def run_retry() -> None:
    """
    function to run retry mode in case first try failed
    """
<<<<<<< HEAD
    #sleep(300) #5 min wait used for regular operation
    sleep(300)
=======
    db = DatabaseHandle()
    db.removeTarget(args.id)
    print(f"Removed server with ID {args.id} from monitoring list.")
>>>>>>> main

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
<<<<<<< HEAD
    db = DatabaseHandle("./data.db")
    past_results = db.get_recent(10, server)
    NotificationService().generate_and_send_report(results=past_results, server_url=server,http_code="NONE - REPORT",http_description="NONE - REPORT" )
=======
    db = DatabaseHandle()
    servers = db.getAllTargets()
    print(f"{'ID':<5} {'URL':<30} {'Email':<30} {'Latest Status':<15}")
    print("-" * 80)
    for server in servers:
        latest_runs = db.getRecent(number=1, server=server)
        latest_status = "N/A"
        if latest_runs and len(latest_runs) > 0:
            latest_status = "UP" if latest_runs[0].reachable else "DOWN"
        print(f"{server.id:<5} {server.url:<30} {server.email:<30} {latest_status:<15}")
>>>>>>> main

def debug() -> None:
    """
    function to experiment with, debugging mode
    """
<<<<<<< HEAD
    db = DatabaseHandle("./data.db")
    past_results = db.get_recent(10, server)
    print(past_results[0])
    print(type(past_results[1]))
    print(past_results[1])
    print(past_results[1].is_success)
    print(past_results[2])
    print(past_results[2].is_success)
=======
    db = DatabaseHandle()
    servers = db.getAllTargets()
    target_server = None
    for server in servers:
        if server.id == args.id:
            target_server = server
            break
    
    if not target_server:
        print(f"Server with ID {args.id} not found.")
        return
    
    latest_runs = db.getRecent(number=1, server=target_server)
    if latest_runs and len(latest_runs) > 0:
        status = "UP" if latest_runs[0].reachable else "DOWN"
        print(f"Latest status for server {args.id}: {status}")
        print(f"Timestamp: {latest_runs[0].timestamp}")
        print(f"HTTP Status: {latest_runs[0].httpStatus if latest_runs[0].httpStatus else 'N/A'}")
    else:
        print(f"No monitoring data available for server {args.id}.")


def cmd_history(args) -> None:
    """
    Displays historical monitoring runs for a server, optionally filtered by date range.
    Usage: python src/main.py history <id> [--from DATE] [--to DATE]

    # TODO: call db.getRunsInTimeframe(server, args.from_date, args.to_date)
    #        print each run in a readable format
    """
    db = DatabaseHandle()
    servers = db.getAllTargets()
    target_server = None
    for server in servers:
        if server.id == args.id:
            target_server = server
            break
    
    if not target_server:
        print(f"Server with ID {args.id} not found.")
        return
    
    # Default date range: all time if not specified
    from_date = args.from_date or "1970-01-01"
    to_date = args.to_date or "2099-12-31"
    
    runs = db.getRunsInTimeframe(server=target_server, start=from_date, end=to_date)
    if runs:
        print(f"Monitoring history for server {args.id}:")
        for run in runs:
            timestamp = run.timestamp
            status = "UP" if run.reachable else "DOWN"
            http_code = run.httpStatus if run.httpStatus else "N/A"
            print(f"{timestamp}: {status} (HTTP {http_code})")
    else:
        print(f"No monitoring data available for server {args.id}.")


def cmd_start(args) -> None:
    """
    Starts the monitoring loop using the schedule library.
    Runs MonitoringSystem.runCheck() at each server's configured interval.
    Usage: python src/main.py start

    # TODO: load config, instantiate MonitoringSystem
    #        use schedule.every(interval).seconds.do(monitoring_system.runCheck)
    #        loop: schedule.run_pending(); time.sleep(1)
    """
    try:
        config = load_config()
        db = DatabaseHandle()
        monitoring_system = MonitoringSystem(config=config, db=db)
        
        for server in db.getAllTargets():
            print(f"Scheduling monitoring for {server.url} every {server.interval} seconds.")
            schedule.every(server.interval).seconds.do(monitoring_system.runCheck)
        
        print("Monitoring loop started. Press Ctrl+C to stop.")
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nMonitoring loop stopped.")


def cmd_stop(args) -> None:
    """
    Stops the monitoring loop (for future implementation — may use a PID file or signal).
    Usage: python src/main.py stop

    # TODO: implement graceful shutdown (e.g. write stop flag or send SIGTERM)
    """
    if os.path.exists("monitoring.pid"):
        os.remove("monitoring.pid")
        print("Monitoring loop stopped.")
    else:
        print("Monitoring loop is not running.")


def cmd_init_db(args) -> None:
    """
    Initializes the SQLite database by running schema.sql.
    Usage: python src/main.py --init-db

    # TODO: instantiate DatabaseHandle which calls _init_db() internally
    #        print success message
    """
    db = DatabaseHandle()
    print("Database initialized successfully.")

>>>>>>> main

def main():
    """
    Parses command-line arguments and calls the appropriate command function.
    """
<<<<<<< HEAD

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
=======
    # TODO: create argparse.ArgumentParser
    # TODO: add subparsers for: add, remove, list, status, history, start, stop
    # TODO: add --init-db flag
    # TODO: parse args and call the matching cmd_* function
    parser = argparse.ArgumentParser(description="Monitoring Diagnostic Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new server to monitor")
    add_parser.add_argument("url", help="URL of the server to monitor")
    add_parser.add_argument("email", help="Email address for notifications")
    add_parser.set_defaults(func=cmd_add)
    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a server from monitoring")
    remove_parser.add_argument("id", type=int, help="ID of the server to remove")
    remove_parser.set_defaults(func=cmd_remove)
    # List command
    list_parser = subparsers.add_parser("list", help="List all monitored servers")
    list_parser.set_defaults(func=cmd_list)
    # Status command
    status_parser = subparsers.add_parser("status", help="Show latest status for a server")
    status_parser.add_argument("id", type=int, help="ID of the server to check")
    status_parser.set_defaults(func=cmd_status)
    # History command
    history_parser = subparsers.add_parser("history", help="Show monitoring history for a server")
    history_parser.add_argument("id", type=int, help="ID of the server to check")
    history_parser.add_argument("--from", dest="from_date", help="Start date for the time frame")
    history_parser.add_argument("--to", dest="to_date", help="End date for the time frame")
    history_parser.set_defaults(func=cmd_history)
    # Start command
    start_parser = subparsers.add_parser("start", help="Start the monitoring loop")
    start_parser.set_defaults(func=cmd_start)
    # Stop command
    stop_parser = subparsers.add_parser("stop", help="Stop the monitoring loop")
    stop_parser.set_defaults(func=cmd_stop)
    # Init-db command
    init_db_parser = subparsers.add_parser("init-db", help="Initialize the database")
    init_db_parser.set_defaults(func=cmd_init_db)
    
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
>>>>>>> main


if __name__ == "__main__":
    main()
