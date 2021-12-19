import tasks_to_org
import unittest
from datetime import datetime


class TestCase(unittest.TestCase):


    def test_extract_tasks_from_file(self):

        tasks = tasks_to_org.extract_tasks_from_file("sample.json")
        self.assertTrue(type(tasks) == list)
        
        if len(tasks) > 0:
            self.assertTrue(type(tasks[0]) == dict)


    def test_org_format_task(self):

        task = {
            "task": {
                "title": "Make breakfast",
                "dueDate": 1639836001000,
                "notes": "Multiple\nline\ndescription."
            }
        }

        expected_output = "** TODO Make breakfast\n" + \
                "   DEADLINE: <2021-12-18 Sat 15:00>\n" + \
                "   *** Multiple\n" + \
                "   *** line\n" + \
                "   *** description."

        output = tasks_to_org.org_format_task(task)

        self.assertEqual(output, expected_output)


    def test_select_tasks_by_date(self):

        tasks = tasks_to_org.extract_tasks_from_file("sample.json")

        today_date = datetime.now().date()
        today_tasks = list(tasks_to_org.select_tasks_by_date(tasks, today_date))
        if len(today_tasks) > 0:
            self.assertEqual(get_date_from_task(today_tasks[0]), today_date)
            self.assertEqual(get_date_from_task(today_tasks[-1]), today_date)


def get_date_from_task(task):

    due_datetime_timestamp = task["task"]["dueDate"]
    if due_datetime_timestamp in ("", 0):
        raise ValueError

    due_datetime = datetime.fromtimestamp(int(str(due_datetime_timestamp)[:-3]))

    return due_datetime.date()

if __name__ == "__main__":
    unittest.main()
