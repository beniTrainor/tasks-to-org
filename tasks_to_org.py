"""
Converts data from Android Tasks App into org-mode tasks.
"""

import argparse
import json
from datetime import datetime, timedelta


def main():

    args = parse_args()

    tasks = extract_tasks_from_file(args.tasksfile)

    if args.list is not None:
        list_data = extract_list_data_from_file(args.tasksfile)

        # Task items in the JSON data don't have the name of the list they
        # belong to. Instead, they have the UUID. So, in order to filter by
        # the list name the matching UUID needs to be found.
        matching_list_uuid = None
        for list_data_item in list_data:
            if list_data_item["name"] == args.list:
                matching_list_uuid = list_data_item["uuid"]
        if matching_list_uuid is None:
            print("Error: list not found.")
            exit(1)

        # Task items sometimes have more than one list assigned to them. (This
        # I guess is because it stores a history of the lists it belonged to.)
        # So, all but the last list in that history need to be ignored, the
        # last one is the one it currently belongs to.
        tasks = [task for task in tasks
                 if task["caldavTasks"][-1]["calendar"] == matching_list_uuid]


    if args.tag is not None:
        tasks = [task for task in tasks
                 if args.tag in map(lambda x: x["name"], task["tags"])]


    date = None
    if args.today:
        date = datetime.now().date()
    elif args.tomorrow:
        date = datetime.now().date() + timedelta(days=1)
    if date is not None:
        tasks = list(select_tasks_by_date(tasks, date))

    for task in sorted(tasks, key=lambda task: task["task"]["dueDate"]):
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

    parser.add_argument("--list", type=str,
                        help="select tasks from a given LIST")
    parser.add_argument("--tag", type=str,
                        help="select tasks with a given TAG")

    return parser.parse_args()


def extract_tasks_from_file(filepath):

    with open(filepath) as file:
        data = json.load(file)

    return data["data"]["tasks"]


def extract_list_data_from_file(filepath):
    """
    Returns a list of dictionaries with data of each list created in the Tasks
    App.
    """

    with open(filepath) as file:
        data = json.load(file)

    return data["data"]["caldavCalendars"]


def select_tasks_by_date(tasks, date):

    for task in tasks:
        due_date_timestamp = task["task"]["dueDate"]
        if due_date_timestamp in ("", 0):
            continue
        due_datetime = datetime.fromtimestamp(int(str(due_date_timestamp)[:-3]))
        if due_datetime.date() == date:
            yield task


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
