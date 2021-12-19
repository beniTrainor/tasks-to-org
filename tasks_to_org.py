"""
Converts data from Android Tasks App into org-mode tasks.
"""

import argparse
import json
from datetime import datetime, timedelta


def main():

    args = parse_args()

    tasks = extract_tasks_from_file(args.tasksfile)

    if args.today:
        tasks = select_tasks_by_date(tasks, datetime.now().date())
    elif args.tomorrow:
        tasks = select_tasks_by_date(tasks, datetime.now().date() + timedelta(days=1))

    for task in tasks:
        print(org_format_task(task), "\n")


def parse_args():
    """
    Parses command line arguments.
    """

    parser = argparse.ArgumentParser(
        description="Converts data from Android Tasks App into org-mode tasks.")

    parser.add_argument("tasksfile", type=str, help="path of the tasks file")
    parser.add_argument("--today", action="store_true",
                        help="select tasks with today as due date")
    parser.add_argument("--tomorrow", action="store_true",
                        help="select tasks with tomorrow as due date")

    return parser.parse_args()


def extract_tasks_from_file(filepath):

    with open(filepath) as file:
        data = json.load(file)

    return data["data"]["tasks"]


def select_tasks_by_date(tasks, date):

    selected_tasks = []

    for task in tasks:
        due_date_timestamp = task["task"]["dueDate"]
        if due_date_timestamp in ("", 0):
            continue
        due_datetime = datetime.fromtimestamp(int(str(due_date_timestamp)[:-3]))
        if due_datetime.date() == date:
            selected_tasks.append(task)

    return selected_tasks


def org_format_task(task):
    """
    Extracts contents from a task provided as a dictionary and formats it
    following org-mode syntax.
    """

    output_lines = []

    title = task["task"]["title"]

    due_date_timestamp = task["task"]["dueDate"]
    if due_date_timestamp not in ("", 0):
        due_date = datetime.fromtimestamp(int(str(due_date_timestamp)[:-3]))
        output_lines.append("** TODO " + title)
        output_lines.append("   DEADLINE: " + due_date.strftime("<%Y-%m-%d %a %H:%M>"))
    else:
        output_lines.append("** " + title)

    notes = task["task"].get("notes", "")
    if len(notes) > 0:
        for line in notes.split("\n"):
            output_lines.append("   *** " + line)


    return "\n".join(output_lines)



if __name__ == "__main__":
    main()
