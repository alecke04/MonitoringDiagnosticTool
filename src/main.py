# main.py — application entry point
# Parses CLI arguments and dispatches to the appropriate commands
# Run with: python src/main.py <command> [args]
import argparse

from database import DatabaseHandle

from monitoring import *
from utils.analysis import analyse


#from SCons.Tool.ninja_tool.ninja_scons_daemon import server_thread


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

def run_test() -> None:
    server = "git.sidolaboratories.com"
    monitoring_system = MonitoringSystem()
    result = monitoring_system.run_check(server)

    if result[0]:
        result =  True, analyse(result[1])

    print(result)
    print("FROM DB:")

    db = DatabaseHandle("./data.db")
    db.save_result(server, result)

    db.get_recent(10, server)


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
