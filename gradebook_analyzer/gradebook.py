# GradeBook Analyzer
# Name: Agrima Mishra
# Date: 2025-11-27
# Simple CLI for manual or CSV input, stats, grades, pass/fail, and results table

import csv
import os
import statistics

# Task 1: welcome and menu
def print_welcome_menu():
    print()
    print("welcome to gradebook analyzer")
    print("choose input method:")
    print("1 - manual entry (type names and marks)")
    print("2 - load from csv file (name,marks columns)")
    print("3 - exit")
    print()

# Task 2a: manual entry
def manual_entry():
    marks = {}
    while True:
        try:
            n = int(input("how many students? ").strip())
            if n <= 0:
                print("enter a positive whole number")
                continue
            break
        except ValueError:
            print("please enter a whole number like 5")
    for i in range(1, n + 1):
        name = input(f"student {i} name: ").strip() or f"Student_{i}"
        while True:
            s = input(f"{name} marks (0-100): ").strip()
            try:
                score = float(s)
                if score < 0 or score > 100:
                    print("marks should be between 0 and 100")
                    continue
                break
            except ValueError:
                print("enter a number like 78 or 92.5")
        marks[name] = score
    return marks

# Task 2b: load from CSV
def load_from_csv(path):
    marks = {}
    if not os.path.exists(path):
        print("file not found:", path)
        return marks
    try:
        with open(path, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                name = row[0].strip() if row[0].strip() else None
                score = None
                if len(row) > 1:
                    try:
                        score = float(row[1].strip())
                    except Exception:
                        score = None
                # try other cells if second column not a number
                if score is None and len(row) > 1:
                    for cell in row[1:]:
                        try:
                            score = float(cell.strip())
                            break
                        except Exception:
                            continue
                if name is None:
                    name = f"Student_{len(marks) + 1}"
                if score is None:
                    print("skipping row, cannot parse marks:", row)
                    continue
                marks[name] = score
    except Exception as e:
        print("error reading csv:", e)
    return marks

# Task 3: statistical functions
def calculate_average(marks_dict):
    if not marks_dict:
        return None
    values = list(marks_dict.values())
    return sum(values) / len(values)

def calculate_median(marks_dict):
    if not marks_dict:
        return None
    return statistics.median(sorted(marks_dict.values()))

def find_max_score(marks_dict):
    if not marks_dict:
        return None, None
    name = max(marks_dict, key=marks_dict.get)
    return name, marks_dict[name]

def find_min_score(marks_dict):
    if not marks_dict:
        return None, None
    name = min(marks_dict, key=marks_dict.get)
    return name, marks_dict[name]

# Task 4: grade assignment and distribution
def assign_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

def build_grades_dict(marks_dict):
    return {name: assign_grade(score) for name, score in marks_dict.items()}

def grade_counts(grades_dict):
    counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for g in grades_dict.values():
        if g in counts:
            counts[g] += 1
        else:
            counts[g] = counts.get(g, 0) + 1
    return counts

# Task 5: pass/fail with list comprehension
def pass_fail_lists(marks_dict, pass_mark=40):
    passed_students = [name for name, m in marks_dict.items() if m >= pass_mark]
    failed_students = [name for name, m in marks_dict.items() if m < pass_mark]
    return passed_students, failed_students

# Task 6 helpers: results table, export
def print_results_table(marks_dict, grades_dict):
    print()
    print(f"{'Name':30} {'Marks':>6} {'Grade':>6}")
    print("-" * 46)
    for name, score in marks_dict.items():
        grade = grades_dict.get(name, "")
        print(f"{name:30} {score:6.1f} {grade:6}")
    print("-" * 46)
    print()

def export_to_csv(marks_dict, grades_dict, filename):
    try:
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Marks", "Grade"])
            for name, score in marks_dict.items():
                writer.writerow([name, score, grades_dict.get(name, "")])
        print("exported results to", filename)
    except Exception as e:
        print("could not write CSV:", e)

# combined analysis, prints everything in required order
def show_analysis(marks):
    if not marks:
        print("no student data available")
        return

    avg = calculate_average(marks)
    med = calculate_median(marks)
    max_name, max_score = find_max_score(marks)
    min_name, min_score = find_min_score(marks)

    print()
    print("analysis summary")
    print("----------------")
    print(f"total students: {len(marks)}")
    print(f"average marks: {avg:.2f}")
    print(f"median marks: {med:.2f}")
    print(f"highest: {max_name} with {max_score}")
    print(f"lowest: {min_name} with {min_score}")

    grades = build_grades_dict(marks)
    counts = grade_counts(grades)

    print()
    print("grade distribution")
    for k in ["A", "B", "C", "D", "F"]:
        print(f"{k}: {counts.get(k, 0)}")

    # pass / fail using list comprehension
    passed, failed = pass_fail_lists(marks)

    print()
    print("pass / fail summary")
    print("passed count:", len(passed))
    print("passed names:", ", ".join(passed) if passed else "None")
    print("failed count:", len(failed))
    print("failed names:", ", ".join(failed) if failed else "None")

    # results table
    print_results_table(marks, grades)

    # optional export
    while True:
        opt = input("do you want to export results to CSV? (y/n): ").strip().lower()
        if opt == "y":
            fname = input("enter file name (e.g. results.csv): ").strip() or "results.csv"
            export_to_csv(marks, grades, fname)
            break
        elif opt in ("n", ""):
            break
        else:
            print("enter y or n")

# main loop for repeated analysis
def main():
    while True:
        print_welcome_menu()
        choice = input("enter 1, 2 or 3: ").strip()
        if choice == "1":
            marks = manual_entry()
            show_analysis(marks)
            cont = input("analyze again? (y to continue): ").strip().lower()
            if cont != "y":
                print("good luck. submit on time.")
                break
        elif choice == "2":
            path = input("enter csv path like students.csv: ").strip()
            marks = load_from_csv(path)
            if marks:
                show_analysis(marks)
            else:
                print("no valid data loaded from csv")
            cont = input("analyze again? (y to continue): ").strip().lower()
            if cont != "y":
                print("good luck. submit on time.")
                break
        elif choice == "3":
            print("bye")
            break
        else:
            print("please enter 1 2 or 3")

if __name__ == "__main__":
    main()
