# main.py — application entry point
# Parses CLI arguments and dispatches to the appropriate commands
# Run with: python src/main.py <command> [args]

# TODO: import argparse
# TODO: from src.database.db_handle import DatabaseHandle
# TODO: from src.monitoring.monitor import MonitoringSystem
# TODO: from src.utils.config import load_config
# TODO: import schedule, time  (for the monitoring loop)


def cmd_add(args) -> None:
    """
    Adds a new web server to the monitoring list.
    Usage: python src/main.py add <url> <email>

    # TODO: create WebServer object from args.url and args.email
    #        call db.addTarget(server) to persist it
    #        print confirmation
    """
    pass


def cmd_remove(args) -> None:
    """
    Removes a server from the monitoring list by its ID.
    Usage: python src/main.py remove <id>

    # TODO: call db.removeTarget(args.id)
    #        print confirmation
    """
    pass


def cmd_list(args) -> None:
    """
    Displays all currently monitored servers in a formatted table.
    Usage: python src/main.py list

    # TODO: call db.getAllTargets()
    #        print table with ID, URL, Email, latest Status
    """
    pass


def cmd_status(args) -> None:
    """
    Shows the latest monitoring result for a specific server.
    Usage: python src/main.py status <id>

    # TODO: call db.getRecent(number=1, server) and print the result
    """
    pass


def cmd_history(args) -> None:
    """
    Displays historical monitoring runs for a server, optionally filtered by date range.
    Usage: python src/main.py history <id> [--from DATE] [--to DATE]

    # TODO: call db.getRunsInTimeframe(server, args.from_date, args.to_date)
    #        print each run in a readable format
    """
    pass


def cmd_start(args) -> None:
    """
    Starts the monitoring loop using the schedule library.
    Runs MonitoringSystem.runCheck() at each server's configured interval.
    Usage: python src/main.py start

    # TODO: load config, instantiate MonitoringSystem
    #        use schedule.every(interval).seconds.do(monitoring_system.runCheck)
    #        loop: schedule.run_pending(); time.sleep(1)
    """
    pass


def cmd_stop(args) -> None:
    """
    Stops the monitoring loop (for future implementation — may use a PID file or signal).
    Usage: python src/main.py stop

    # TODO: implement graceful shutdown (e.g. write stop flag or send SIGTERM)
    """
    pass


def cmd_init_db(args) -> None:
    """
    Initializes the SQLite database by running schema.sql.
    Usage: python src/main.py --init-db

    # TODO: instantiate DatabaseHandle which calls _init_db() internally
    #        print success message
    """
    pass


def main():
    """
    Parses command-line arguments and calls the appropriate command function.
    """
    # TODO: create argparse.ArgumentParser
    # TODO: add subparsers for: add, remove, list, status, history, start, stop
    # TODO: add --init-db flag
    # TODO: parse args and call the matching cmd_* function
    pass


if __name__ == "__main__":
    main()
