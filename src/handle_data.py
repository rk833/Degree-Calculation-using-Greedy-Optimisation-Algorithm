# src/handle_data.py

import csv
from src.module import Module
from src.student import Student


def load_modules(filename):
    """Load module definitions from a CSV file and return a code-to-Module dictionary."""
    modules = {}
    try:
        # open module file and read each row
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    code = row[0].strip()
                    name = row[1].strip()
                    
                    # create Module object and store by code
                    modules[code] = Module(code, name)

        print(f"loaded {len(modules)} modules from {filename}")
        return modules

    except FileNotFoundError:
        print(f"error: could not find file {filename}")
        return {}

    except Exception as e:
        print(f"error loading modules: {e}")
        return {}


def load_student_marks(filename, modules_dict):
    """Load student marks from CSV and return student_id → Student dict."""
    students = {}
    try:
        # open student marks file
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 3:
                    continue

                student_id = row[0].strip()
                student = Student(student_id)

                # read module-code / mark pairs
                i = 1
                while i < len(row) - 1:
                    module_code = row[i].strip()
                    try:
                        mark = int(row[i + 1].strip())
                        
                        # store the mark inside the student object
                        student.add_mark(module_code, mark)

                    except ValueError:
                        print(f"warning: invalid mark for student {student_id}, module {module_code}")

                    i += 2

                # store completed student object
                students[student_id] = student

        print(f"loaded {len(students)} students from {filename}")
        return students

    except FileNotFoundError:
        print(f"error: could not find file {filename}")
        return {}

    except Exception as e:
        print(f"error loading student marks: {e}")
        return {}


def save_results_csv(results, filename):
    """Write student degree results to a CSV file."""

    try:
        # open file in write mode
        with open(filename, 'w', newline='') as file:
            fieldnames = ['student_id', 'level5_avg', 'level5_credits',
                          'level6_avg', 'level6_credits', 'final_mark',
                          'classification']

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            # write one row per student
            for result in results:
                row = {
                    'student_id': result['student_id'],
                    'level5_avg': result['level5_avg'],
                    'level5_credits': result['level5_credits'],
                    'level6_avg': result['level6_avg'],
                    'level6_credits': result['level6_credits'],
                    'final_mark': result['final_mark'],
                    'classification': result['classification']
                }
                writer.writerow(row)

        print(f"results saved to {filename}")
        return True

    except Exception as e:
        print(f"error saving results to csv: {e}")
        return False


def save_summary_txt(stats, filename):
    """Create a text summary report of degree statistics."""
    try:
        # create summary text file
        with open(filename, 'w') as file:
            file.write("Degree calculation summary report\n")

            file.write(f"Total students processed: {stats['total_students']}\n")
            file.write(f"Students passed: {stats['passed_students']}\n")
            file.write(f"Students failed: {stats['failed_students']}\n")

            # calculate pass/fail percentages
            passed_pct = (stats['passed_students'] / stats['total_students'] * 100) if stats['total_students'] > 0 else 0
            failed_pct = (stats['failed_students'] / stats['total_students'] * 100) if stats['total_students'] > 0 else 0

            file.write(f"Pass rate: {passed_pct:.1f}%\n")
            file.write(f"Fail rate: {failed_pct:.1f}%\n\n")

            file.write("Degree classifications breakdown\n")

            classification_order = [
                'First Class',
                'Second Class (Upper Division)',
                'Second Class (Lower Division)',
                'Third Class',
                'Fail'
            ]

            # write classifications in fixed order
            for cls in classification_order:
                if cls in stats['classifications']:
                    count = stats['classifications'][cls]
                    percentage = (count / stats['total_students'] * 100) if stats['total_students'] > 0 else 0
                    file.write(f"{cls:35s}: {count:3d} ({percentage:5.1f}%)\n")

            file.write("\nAverage marks\n")
            file.write(f"Average year 2 mark: {stats['average_level5_mark']}%\n")
            file.write(f"Average year 3 mark: {stats['average_level6_mark']}%\n")
            file.write(f"Average final mark: {stats['average_final_mark']}%\n")

            file.write("\nFinal mark range\n")
            file.write(f"Highest final mark: {stats['highest_mark']}%\n")
            file.write(f"Lowest final mark: {stats['lowest_mark']}%\n")

            # academic regulation reference
            file.write("\nCalculation based on UWE Academic Regulations 23/24\n")
            file.write("Level 5: best 100 credits (typically 90 due to credit structure)\n")
            file.write("Level 6: all credits\n")
            file.write("Final mark: (Level 6 * 3 + Level 5) / 4\n")

        print(f"summary saved to {filename}")
        return True

    except Exception as e:
        print(f"error saving summary: {e}")
        return False


def display_summary(stats):
    """Print degree statistics to terminal for quick overview."""
    print("\nDegree calculation summary:")

    print(f"Total students processed: {stats['total_students']}")
    print(f"Students passed: {stats['passed_students']}")
    print(f"Students failed: {stats['failed_students']}")

    # calculate pass/fail percentages
    passed_pct = (stats['passed_students'] / stats['total_students'] * 100) if stats['total_students'] > 0 else 0
    failed_pct = (stats['failed_students'] / stats['total_students'] * 100) if stats['total_students'] > 0 else 0

    print(f"Pass rate: {passed_pct:.1f}%")
    print(f"Fail rate: {failed_pct:.1f}%")

    print("\nDegree classifications breakdown:")

    classification_order = [
        'First Class',
        'Second Class (Upper Division)',
        'Second Class (Lower Division)',
        'Third Class',
        'Fail'
    ]

    # display classification counts
    for cls in classification_order:
        if cls in stats['classifications']:
            count = stats['classifications'][cls]
            percentage = (count / stats['total_students'] * 100) if stats['total_students'] > 0 else 0
            print(f"{cls:35s}: {count:3d} ({percentage:5.1f}%)")

    print("\nAverage marks:")
    print(f"Average year 2 mark: {stats['average_level5_mark']}%")
    print(f"Average year 3 mark: {stats['average_level6_mark']}%")
    print(f"Average final mark: {stats['average_final_mark']}%")

    print("\nFinal mark range:")
    print(f"Highest final mark: {stats['highest_mark']}%")
    print(f"Lowest final mark: {stats['lowest_mark']}%")
