import os
import unittest
import yaml
import subprocess
import filecmp
import time
import logging
import difflib

# Configure logging for detailed output during tests.
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


def get_file_diff(expected_path, output_path):
    """
    Compute a unified diff between expected and output files, assuming they are text.
    If the files cannot be read as text, return a message indicating that.
    """
    try:
        with open(expected_path, "r", encoding="utf8", errors="replace") as f:
            expected_lines = f.readlines()
        with open(output_path, "r", encoding="utf8", errors="replace") as f:
            output_lines = f.readlines()
        diff = list(difflib.unified_diff(expected_lines, output_lines,
                                         fromfile="expected", tofile="output", lineterm=""))
        if diff:
            return "\n".join(diff)
        else:
            return "No differences found."
    except Exception as e:
        return f"Could not compute diff: {e}"


def create_test_method(test_case):
    """
    Creates a test method for a given test case.
    """
    def test_method(self):
        # Resolve the absolute path to the example directory.
        example_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", test_case["example_dir"]))
        logging.info("Starting test case '%s' in directory '%s'", test_case["name"], example_dir)
        
        created_files = []
        
        # Loop through each command defined for this test case.
        for command in test_case["commands"]:
            config_file = command["config"]
            config_path = os.path.join(example_dir, config_file)
            logging.info("Executing command: vcast %s --test-mode", config_path)
            
            start_time = time.time()
            result = subprocess.run(
                ["vcast", config_path, "--test-mode"],
                cwd=example_dir,
                capture_output=True,
                text=True
            )
            elapsed_time = time.time() - start_time
            logging.info("Command completed in %.2f seconds", elapsed_time)
            
            if result.stdout:
                logging.info("STDOUT: %s", result.stdout.strip())
            if result.stderr:
                logging.info("STDERR: %s", result.stderr.strip())
            
            self.assertEqual(
                result.returncode, 0,
                msg=f"Test case '{test_case['name']}' with config '{config_file}' failed.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
            )
            
            # Compare outputs with expected outputs.
            outputs = command.get("outputs", {})
            for output_file, expected_file in outputs.items():
                output_path = os.path.join(example_dir, output_file)
                expected_path = os.path.join(example_dir, expected_file)
                logging.info("Comparing output file '%s' with expected '%s'", output_path, expected_path)
                
                self.assertTrue(
                    os.path.exists(output_path),
                    msg=f"Output file '{output_path}' missing in test case '{test_case['name']}'."
                )
                files_equal = filecmp.cmp(expected_path, output_path, shallow=False)
                if not files_equal:
                    diff_output = get_file_diff(expected_path, output_path)
                    self.fail(f"File '{output_file}' in test case '{test_case['name']}' does not match expected output. Diff:\n{diff_output}")
                else:
                    logging.info("File '%s' matches expected output.", output_file)
                created_files.append(output_path)
                
        # Accumulate created files for later cleanup.
        self.__class__.all_created_files.extend(created_files)
    return test_method


class DynamicTestFramework(unittest.TestCase):
    """
    A test class with dynamically-added test methods.
    """
    @classmethod
    def setUpClass(cls):
        cls.all_created_files = []

    # Instead of cleaning up in each test, clean up after all tests have run.
    @classmethod
    def tearDownClass(cls):
        logging.info("Cleaning up generated output files...")
        for filepath in cls.all_created_files:
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    logging.info("Removed output file: %s", filepath)
            except Exception as err:
                logging.error("Failed to remove output file %s: %s", filepath, err)


def load_tests(loader, tests, pattern):
    # Load test specification from the YAML file.
    test_yaml = os.path.join(os.path.dirname(__file__), "test_cases.yaml")
    with open(test_yaml, "r") as f:
        test_spec = yaml.safe_load(f)
    # Dynamically create a test method for each test case.
    for test_case in test_spec["tests"]:
        # Create a valid method name (replace spaces with underscores)
        test_name = "test_" + test_case["name"].replace(" ", "_")
        setattr(DynamicTestFramework, test_name, create_test_method(test_case))
    return loader.loadTestsFromTestCase(DynamicTestFramework)


if __name__ == "__main__":
    unittest.main()
