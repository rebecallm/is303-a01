"""
IS 303 Autograder - A01: Your First GitHub Submission

This autograder checks student Python files against a rubric JSON file.
Students can run this locally before submitting to verify their work meets
the basic requirements.

Usage:
    python a01_autograder.py

    By default, the autograder looks for .py files in the current directory
    and uses a01_rubric.json for grading instructions. You can also pass
    a folder path as an argument to grade a specific folder.

    python a01_autograder.py /path/to/student/folder

Checks performed:
    1. File identification: matches file names to known problem contexts
    2. Content checks: verifies the I/P/O comment block exists
    3. Execution checks: runs the program with simulated inputs and
       compares output against expected results using regex matching
"""

import json
import os
import re
import subprocess
import sys


def load_rubric(rubric_path):
    """Load and return the rubric from a JSON file."""
    with open(rubric_path, "r", encoding="utf-8") as f:
        return json.load(f)


def identify_problem(file_name, rubric):
    """
    Match a file name to a problem context using the rubric's naming dictionary.
    Returns the problem name if matched, or None if no match is found.
    """
    file_lower = file_name.lower()
    for problem_name, possible_names in rubric["problem_naming"].items():
        for name in possible_names:
            if name.lower() == file_lower:
                return problem_name
    return None


def check_file_contents(file_path, problem_rubric):
    """
    Check the file contents against the rubric's content checks.
    Returns a tuple of (points_earned, list_of_notes).
    """
    points = 0
    notes = []

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    for check in problem_rubric["content_checks"]:
        field = check["field"]
        regexes = check["regexes"]
        check_points = check["points"]
        found = False

        for regex in regexes:
            if re.search(regex, content, re.IGNORECASE | re.DOTALL):
                found = True
                break

        if found:
            points += check_points
        else:
            notes.append(f"  MISSING: {field}")

    return points, notes


def run_with_simulated_input(file_path, problem_rubric, timeout=15):
    """
    Run the student's file with simulated inputs and check the output
    against expected patterns. Returns (points_earned, list_of_notes).
    """
    points = 0
    notes = []
    simulated_inputs = problem_rubric["simulated_inputs"]
    expected_outputs = problem_rubric["expected_outputs"]
    points_per_check = problem_rubric["points_per_output_check"]

    for i, (sim_input, expected) in enumerate(zip(simulated_inputs, expected_outputs)):
        try:
            result = subprocess.run(
                [sys.executable, os.path.abspath(file_path)],
                input=sim_input,
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            if result.returncode != 0:
                notes.append(f"  ERROR: Program crashed on test {i + 1}")
                if result.stderr:
                    # Show only the last line of the error (the useful part)
                    error_lines = result.stderr.strip().split("\n")
                    notes.append(f"    {error_lines[-1]}")
                continue

            if re.search(expected, result.stdout, re.DOTALL | re.IGNORECASE):
                points += points_per_check
            else:
                notes.append(f"  OUTPUT MISMATCH on test {i + 1}:")
                notes.append(f"    Expected pattern: {expected}")
                notes.append(f"    Got: {result.stdout.strip()[:200]}")

        except subprocess.TimeoutExpired:
            notes.append(
                f"  TIMEOUT: Program took more than {timeout} seconds on test {i + 1}. "
                f"Check for infinite loops."
            )
        except Exception as e:
            notes.append(f"  ERROR running test {i + 1}: {str(e)}")

    return points, notes


def grade_file(file_path, problem_name, problem_rubric):
    """
    Grade a single file. Returns (points_earned, list_of_notes).
    """
    total_points = 0
    all_notes = []

    # Check file contents (I/P/O block, etc.)
    pts, notes = check_file_contents(file_path, problem_rubric)
    total_points += pts
    all_notes.extend(notes)

    # Run with simulated inputs
    pts, notes = run_with_simulated_input(file_path, problem_rubric)
    total_points += pts
    all_notes.extend(notes)

    return total_points, all_notes


def find_student_files(folder_path, rubric):
    """
    Scan a folder for .py files that match known problem contexts.
    Returns a list of (file_path, problem_name) tuples.
    Ignores the autograder file itself.
    """
    matches = []
    autograder_name = os.path.basename(__file__).lower()

    for file_name in sorted(os.listdir(folder_path)):
        if not file_name.endswith(".py"):
            continue
        if file_name.lower() == autograder_name:
            continue

        problem_name = identify_problem(file_name, rubric)
        if problem_name:
            matches.append((os.path.join(folder_path, file_name), problem_name))
        else:
            print(f"  [?] {file_name}: not recognized as a known context (skipped)")

    return matches


def print_separator():
    """Print a visual separator line."""
    print("-" * 60)


def main():
    # Determine folder and rubric paths
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = os.path.dirname(os.path.abspath(__file__))

    rubric_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "a01_rubric.json"
    )

    if not os.path.exists(rubric_path):
        print(f"Error: Cannot find a01_rubric.json at {rubric_path}")
        print("Make sure the rubric file is in the same folder as this autograder.")
        sys.exit(1)

    rubric = load_rubric(rubric_path)

    print()
    print("=" * 60)
    print("  IS 303 Autograder: A01 - Your First GitHub Submission")
    print("=" * 60)
    print(f"  Scanning: {folder_path}")
    print()

    # Find matching files
    matches = find_student_files(folder_path, rubric)

    if not matches:
        print("  No recognized Python files found.")
        print()
        print("  Make sure your file names match one of these patterns:")
        for problem, names in rubric["problem_naming"].items():
            print(f"    {problem}: {', '.join(names[:3])}")
        print()
        sys.exit(1)

    # Grade each file
    total_score = 0
    problems_found = []

    for file_path, problem_name in matches:
        file_name = os.path.basename(file_path)
        problem_rubric = rubric["problem_rubrics"][problem_name]

        print_separator()
        print(f"  File: {file_name}")
        print(f"  Context: {problem_name}")
        print()

        pts, notes = grade_file(file_path, problem_name, problem_rubric)
        total_score += pts
        problems_found.append(problem_name)

        # Calculate max possible for this problem
        max_content = sum(c["points"] for c in problem_rubric["content_checks"])
        max_output = problem_rubric["points_per_output_check"] * len(
            problem_rubric["simulated_inputs"]
        )
        max_possible = max_content + max_output

        print(f"  Score: {pts}/{max_possible}")

        if notes:
            print()
            print("  Issues found:")
            for note in notes:
                print(f"    {note}")
        else:
            print("  All checks passed!")

        print()

    # Summary
    print_separator()
    print()
    print("  SUMMARY")
    print()
    print(f"  Programs found: {len(matches)}")
    for pname in problems_found:
        print(f"    - {pname}")
    print()

    if len(matches) < 2:
        print("  WARNING: This assignment requires TWO programs from")
        print("  different contexts. Only one was found.")
        print()

    if len(matches) >= 2 and len(set(problems_found)) < 2:
        print("  WARNING: Both files matched the same context.")
        print("  You need two DIFFERENT contexts.")
        print()

    print(f"  Autograder score: {total_score} (content + output checks only)")
    print()
    print("  Note: This score does NOT include points for variable naming")
    print("  quality, output readability, commit messages, or GitHub")
    print("  submission. Those are graded by your instructor.")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
