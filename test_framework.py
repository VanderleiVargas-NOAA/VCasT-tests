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

def create_test_method(test_case):
    """
    Creates a test method function for a given test case.
    """
    def test_method(self):
        # Resolve the absolute path to the example directory.
        example_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", test_case["example_dir"]))
        logging.info("Starting test case '%s' in directory '%s'", test_case["name"], example_dir)
        
        created_files = []
        
        # Loop through each command defined in the test case.
        for command in test_case["commands"]:
            config_file = command["config"]
            config_path = os.path.join(example_dir, config_file)
            logging.info("Executing command: vcast %s", config_path)
            
            start_time = time.time()
            result = subprocess.run(
                ["vcast", config_path],
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
                
                if not filecmp.cmp(expected_path, output_path, shallow=False):
                    diff_text = ""
                    try:
                        with open(expected_path, 'r', encoding='utf8') as f:
                            expected_lines = f.readlines()
                        with open(output_path, 'r', encoding='utf8') as f:
                            output_lines = f.readlines()
                        diff = difflib.unified_diff(
                            expected_lines, output_lines,
                            fromfile='expected',
                            tofile='actual',
                            lineterm=''
                        )
                        diff_text = '\n'.join(diff)
                    except Exception:
                        diff_text = "Binary files differ or files cannot be read as text."
                    self.fail(
                        f"File '{output_file}' in test case '{test_case['name']}' does not match expected output.\nDiff:\n{diff_text}"
                    )
                else:
                    logging.info("File '%s' matches expected output.", output_file)
                created_files.append(output_path)
        
        # Remove all created output files for this test case.
        for filepath in created_files:
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    logging.info("Removed output file: %s", filepath)
            except Exception as err:
                logging.error("Failed to remove output file %s: %s", filepath, err)
    return test_method

class DynamicTestFramework(unittest.TestCase):
    """
    A test class that will have individual test methods added dynamically.
    """
    pass

def load_tests(loader, tests, pattern):
    # Load test specification from YAML file.
    test_yaml = os.path.join(os.path.dirname(__file__), "test_cases.yaml")
    with open(test_yaml, "r") as f:
        test_spec = yaml.safe_load(f)
    # Dynamically create a test method for each test case.
    for test_case in test_spec["tests"]:
        # Create a valid method name (replace spaces with underscores).
        test_name = "test_" + test_case["name"].replace(" ", "_")
        setattr(DynamicTestFramework, test_name, create_test_method(test_case))
    return loader.loadTestsFromTestCase(DynamicTestFramework)

if __name__ == "__main__":
    unittest.main()
