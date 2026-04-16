# main.py — application entry point
# Parses CLI arguments and dispatches to the appropriate commands
# Run with: python src/main.py <command> [args]

# TODO: import argparse
# TODO: from src.database.db_handle import DatabaseHandle
# TODO: from src.monitoring.monitor import MonitoringSystem
# TODO: from src.utils.config import load_config
# TODO: import schedule, time  (for the monitoring loop)


import argparse
import os
import schedule
import time

from src.database.db_handle import DatabaseHandle
from src.monitoring.monitor import MonitoringSystem
from src.models.web_server import WebServer
from src.utils.config import load_config


def cmd_add(args) -> None:
    """
    Adds a new web server to the monitoring list.
    Usage: python src/main.py add <url> <email>

    # TODO: create WebServer object from args.url and args.email
    #        call db.addTarget(server) to persist it
    #        print confirmation
    """
    web_server = WebServer(url=args.url, email=args.email)
    db = DatabaseHandle()
    db.addTarget(web_server, email_recipient=args.email)
    print(f"Added {args.url} with notification email {args.email} to monitoring list.")


def cmd_remove(args) -> None:
    """
    Removes a server from the monitoring list by its ID.
    Usage: python src/main.py remove <id>

    # TODO: call db.removeTarget(args.id)
    #        print confirmation
    """
    db = DatabaseHandle()
    db.removeTarget(args.id)
    print(f"Removed server with ID {args.id} from monitoring list.")


def cmd_list(args) -> None:
    """
    Displays all currently monitored servers in a formatted table.
    Usage: python src/main.py list

    # TODO: call db.getAllTargets()
    #        print table with ID, URL, Email, latest Status
    """
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


def cmd_status(args) -> None:
    """
    Shows the latest monitoring result for a specific server.
    Usage: python src/main.py status <id>

    # TODO: call db.getRecent(number=1, server) and print the result
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


def main():
    """
    Parses command-line arguments and calls the appropriate command function.
    """
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


if __name__ == "__main__":
    main()
