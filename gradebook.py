"""
=====================================================
Name:         Chhavi Goyal
Date:         2024-10-02
Assignment:   Mini Project - GradeBook Analyzer
Course:       Programming for ProblemSolving using Python
=====================================================

This script is a Command-Line Interface (CLI) tool to analyze
student grades. It allows for manual data entry or CSV import
and performs statistical analysis, grade assignment, and
pass/fail filtering.
"""

import csv
import os
import math

# --- Task 2: Data Entry Functions ---

def get_manual_input() -> dict:
    """
    Allows the user to manually enter student names and marks.
    Validates marks are numeric and between 0-100.
    Returns a dictionary of {name: mark}.
    """
    marks_dict = {}
    print("\n--- Manual Mark Entry ---")
    print("Enter student name and mark. Type 'done' as the name to finish.")
    
    while True:
        name = input("Enter student name: ").strip()
        if name.lower() == 'done':
            break
        
        if not name:
            print("Name cannot be empty. Please try again.")
            continue
            
        try:
            mark_str = input(f"  Enter mark for {name}: ").strip()
            mark = float(mark_str)
            
            if 0 <= mark <= 100:
                marks_dict[name] = mark
            else:
                print("Invalid mark. Please enter a value between 0 and 100.")
        except ValueError:
            print("Invalid input. Mark must be a numeric value.")
        except EOFError:
            break
            
    print(f"Added {len(marks_dict)} student(s).")
    return marks_dict

def load_from_csv() -> dict:
    """
    Loads student names and marks from a user-specified CSV file.
    Assumes CSV format: Name,Mark (with a potential header).
    Returns a dictionary of {name: mark}.
    """
    marks_dict = {}
    filename = input("\nEnter CSV filename (e.g., students.csv): ").strip()
    
    if not os.path.exists(filename):
        print(f"Error: File not found at '{filename}'")
        return marks_dict
        
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            
            # Skip header row
            try:
                header = next(reader)
                print(f"CSV header found: {', '.join(header)}")
            except StopIteration:
                print("Warning: CSV file is empty.")
                return marks_dict

            # Read data rows
            for row in reader:
                if not row or len(row) < 2:
                    print(f"Skipping malformed row: {row}")
                    continue
                
                name = row[0].strip()
                try:
                    mark = float(row[1].strip())
                    if 0 <= mark <= 100:
                        if name in marks_dict:
                            print(f"Warning: Duplicate name '{name}'. Overwriting old mark.")
                        marks_dict[name] = mark
                    else:
                        print(f"Skipping '{name}': Mark {mark} is outside 0-100 range.")
                except ValueError:
                    print(f"Skipping row for '{name}': Invalid mark '{row[1]}'.")
                
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return {} # Return empty dict on critical read error
        
    print(f"Successfully loaded {len(marks_dict)} student records from '{filename}'.")
    return marks_dict

# --- Task 3: Statistical Analysis Functions ---

def calculate_average(marks_dict: dict) -> float:
    """Calculates the average (mean) of all marks."""
    if not marks_dict:
        return 0.0
    return sum(marks_dict.values()) / len(marks_dict)

def calculate_median(marks_dict: dict) -> float:
    """Calculates the median of all marks."""
    if not marks_dict:
        return 0.0
        
    sorted_marks = sorted(marks_dict.values())
    n = len(sorted_marks)
    mid = n // 2
    
    if n % 2 == 0:
        # Even number of students
        return (sorted_marks[mid - 1] + sorted_marks[mid]) / 2
    else:
        # Odd number of students
        return sorted_marks[mid]

def find_max_score(marks_dict: dict) -> tuple:
    """Finds the highest score and the student(s) who achieved it."""
    if not marks_dict:
        return ("N/A", 0.0)
        
    max_mark = -math.inf
    students = []
    
    for name, mark in marks_dict.items():
        if mark > max_mark:
            max_mark = mark
            students = [name]
        elif mark == max_mark:
            students.append(name)
            
    return (", ".join(students), max_mark)

def find_min_score(marks_dict: dict) -> tuple:
    """Finds the lowest score and the student(s) who achieved it."""
    if not marks_dict:
        return ("N/A", 0.0)
        
    min_mark = math.inf
    students = []
    
    for name, mark in marks_dict.items():
        if mark < min_mark:
            min_mark = mark
            students = [name]
        elif mark == min_mark:
            students.append(name)
            
    return (", ".join(students), min_mark)

# --- Task 4: Grade Assignment Functions ---

def assign_grade(mark: float) -> str:
    """Assigns a letter grade based on a numeric mark."""
    if mark >= 90:
        return 'A'
    elif mark >= 80:
        return 'B'
    elif mark >= 70:
        return 'C'
    elif mark >= 60:
        return 'D'
    else:
        return 'F'

def get_grade_distribution(grades_dict: dict) -> dict:
    """Counts the total number of students per grade category."""
    distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    for grade in grades_dict.values():
        if grade in distribution:
            distribution[grade] += 1
    return distribution

# --- Task 5: Pass/Fail Filter ---

def get_pass_fail_lists(marks_dict: dict, pass_mark: float = 40.0) -> tuple:
    """
    Uses list comprehensions to filter students into pass and fail lists.
    Returns (passed_students_list, failed_students_list).
    """
    passed_students = [name for name, mark in marks_dict.items() if mark >= pass_mark]
    failed_students = [name for name, mark in marks_dict.items() if mark < pass_mark]
    
    return (passed_students, failed_students)

# --- Task 6: Results Display Functions ---

def print_results_table(marks_dict: dict, grades_dict: dict):
    """Prints a formatted table of all students, their marks, and grades."""
    print("\n" + "-"*42)
    print(f"| {'Name':<20} | {'Mark':<6} | {'Grade':<5} |")
    print(f"|{'-'*22}|{'-'*8}|{'-'*7}|")
    
    # Sort by name for consistent output
    for name in sorted(marks_dict.keys()):
        mark = marks_dict[name]
        grade = grades_dict[name]
        print(f"| {name:<20} | {mark:>6.2f} | {grade:<5} |")
        
    print(f"{'-'*42}\n")

def run_analysis(marks_dict: dict):
    """
    Runs all analysis tasks and prints a full report.
    """
    if not marks_dict:
        print("No student data to analyze.")
        return

    # --- Task 4 ---
    grades_dict = {name: assign_grade(mark) for name, mark in marks_dict.items()}
    grade_distribution = get_grade_distribution(grades_dict)

    # --- Task 5 ---
    passed_students, failed_students = get_pass_fail_lists(marks_dict, pass_mark=40.0)

    # --- Task 6 (Report) ---
    print("\n======= Full Grade Report =======")
    
    # Results Table
    print_results_table(marks_dict, grades_dict)
    
    # Statistical Summary (Task 3)
    print("--- 📊 Statistical Analysis ---")
    min_student, min_val = find_min_score(marks_dict)
    max_student, max_val = find_max_score(marks_dict)
    
    print(f"  Total Students: {len(marks_dict)}")
    print(f"  Class Average:  {calculate_average(marks_dict):.2f}")
    print(f"  Class Median:   {calculate_median(marks_dict):.2f}")
    print(f"  Highest Score:  {max_val:.2f} (by {max_student})")
    print(f"  Lowest Score:   {min_val:.2f} (by {min_student})")

    # Grade Distribution (Task 4)
    print("\n--- 📈 Grade Distribution ---")
    for grade, count in grade_distribution.items():
        print(f"  Grade {grade}: {count} student(s)")
        
    # Pass/Fail Summary (Task 5)
    print("\n--- ✅ Pass / Fail Summary (Passing Mark: 40) ---")
    print(f"  Passed: {len(passed_students)}")
    print(f"  Failed: {len(failed_students)}")
    
    if failed_students:
        print(f"  Failing Students: {', '.join(sorted(failed_students))}")
    
    print("===================================")


# --- Task 1: Project Setup and Main Loop ---

def print_welcome_menu():
    """Prints the main menu for the CLI."""
    print("\n" + "="*40)
    print(" 📊 Welcome to the GradeBook Analyzer")
    print("="*40)
    print("  1. Enter Marks Manually")
    print("  2. Load Marks from CSV File")
    print("  3. Exit Program")
    print("-"*40)

def main():
    """
    Main function to run the CLI loop.
    """
    while True:
        print_welcome_menu()
        choice = input("Please select an option (1-3): ").strip()
        
        marks_data = {}
        
        if choice == '1':
            marks_data = get_manual_input()
        elif choice == '2':
            marks_data = load_from_csv()
        elif choice == '3':
            print("\nGoodbye! 👋")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            
        # If data was loaded (from manual or CSV), run the analysis
        if marks_data:
            run_analysis(marks_data)
        
        # Pause for user to read before looping
        if choice in ('1', '2'):
            input("\nPress Enter to return to the main menu...")

# Standard boilerplate to run the main() function
if __name__ == "__main__":
    main()