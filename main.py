# src/main.py

from src.handle_data import load_modules, load_student_marks
from src.handle_data import save_results_csv, save_summary_txt, display_summary
from src.degree_calculator import DegreeCalculator


def main():
    """
    main entry point for degree calculation system
    """
    print("UWE degree classification calculator")
    
    # input and output file paths
    modules_file = "dataset/cs_modules.csv"
    marks_file = "dataset/task1_1_marks.csv"
    results_file = "degree_results.csv"
    summary_file = "degree_summary.txt"
    
    print("\nloading data files...")
    modules = load_modules(modules_file)
    
    # stop program if modules failed to load
    if not modules:
        print("failed to load modules. exiting.")
        return
    
    students = load_student_marks(marks_file, modules)
    
    # stop program if student data failed to load
    if not students:
        print("failed to load student marks. exiting.")
        return
    
    # create calculator and run all degree calculations
    calculator = DegreeCalculator(modules, students)
    results = calculator.process_all_students()
    
    # generate overall statistics
    stats = calculator.get_summary_statistics()
    
    display_summary(stats)
    print("\nsaving results...")
    save_results_csv(results, results_file)
    save_summary_txt(stats, summary_file)

if __name__ == "__main__":
    main()
