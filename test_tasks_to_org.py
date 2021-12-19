import tasks_to_org
import unittest


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


if __name__ == "__main__":
    unittest.main()
