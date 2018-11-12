import subprocess
import tempfile
import nbformat
import unittest


class TestNotebookConsistency(unittest.TestCase):
    @staticmethod
    def _execute_notebook(path):
        """
        Execute a Jupyter Notebook from scratch and convert it into another Jupyter Notebook.
           :returns a converted Jupyter Notebook
        """
        with tempfile.NamedTemporaryFile(suffix = ".ipynb") as tmp_notebook:
            args = [
                "jupyter", "nbconvert",
                "--to", "notebook",
                "--execute",
                "--ExecutePreprocessor.timeout=3600",
                "--output", tmp_notebook.name,
                path
            ]
            subprocess.check_call(args)

            tmp_notebook.seek(0)
            return nbformat.read(tmp_notebook, nbformat.current_nbformat)

    @staticmethod
    def _analise_notebook(notebook):
        """
        Analise notebook cell outputs.

        The function goes through all cell outputs and finds either error or warning.

        :returns a tuple of errors (0th) and warnings (1st)
        """
        errors = []
        warnings = []
        for cell in notebook.cells:
            if 'outputs' in cell:
                for output in cell['outputs']:
                    if output.output_type == "error":
                        errors.append(output)
                    if output.output_type == "warning":
                        warnings.append(output)
        return errors, warnings

    def test_notebooks(self):
        # A set of Jupyter Notebooks to test.
        # Note #1: it is assumed that the current directory
        # is the same where the test file is located.
        # Note #2: the name of the Notebook defined without the extension `*.ipynb'.
        for case in {
            'Getting Started',
            'Compare Agents',
            'Pure Organic vs Bandit - Number of Online Users',
        }:
            with self.subTest(i = case):
                try:
                    notebook = self._execute_notebook(case)
                except Exception:
                    self.fail(f"Case have not passed: {case}")

            errors, warnings = self._analise_notebook(notebook)
            self.assertEqual(errors, [], f"Case '{case}': NOK -- Errors: {errors}")
            self.assertEqual(warnings, [], f"Case '{case}': NOK -- Warnings: {warnings}")
            print(f"Case '{case}': OK")


if __name__ == '__main__':
    unittest.main()
