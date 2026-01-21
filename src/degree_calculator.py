# src/degree_calculator.py

class DegreeCalculator:
    """Processes students, calculates degrees, and stores results."""
    def __init__(self, modules_dict, students_dict):
        """
        initializes with modules and students data
        """
        self.modules = modules_dict      # stores all module information
        self.students = students_dict    # stores all student objects
        self.results = []                # will hold final results for each student
    
    def process_all_students(self):
        """Calculate degree results for all students and store them."""
        print("\nprocessing student degree calculations...")
        
        passed_count = 0
        failed_count = 0
        
        for student_id, student in self.students.items():
            
            # if the student has failed any required module
            if not student.has_passed_all():
                result = {
                    'student_id': student_id,
                    'level5_avg': 0.0,
                    'level5_credits': 0,
                    'level6_avg': 0.0,
                    'level6_credits': 0,
                    'final_mark': 0.0,
                    'classification': 'Fail - not all modules passed',
                    'passed': False
                }
                failed_count += 1
            
            else:
                # best 100 credits from level 5 (greedy selection)
                level5_avg, level5_credits = student.calculate_best_100_credits_greedy(2, self.modules)
                
                # all credits from level 6
                level6_avg, level6_credits = student.calculate_all_credits_average(3, self.modules)
                
                # final weighted degree mark
                final_mark = student.calculate_final_aggregate(level5_avg, level6_avg)
                
                # determine degree classification
                classification = student.get_degree_classification(final_mark)
                
                result = {
                    'student_id': student_id,
                    'level5_avg': round(level5_avg, 2),
                    'level5_credits': level5_credits,
                    'level6_avg': round(level6_avg, 2),
                    'level6_credits': level6_credits,
                    'final_mark': round(final_mark, 2),
                    'classification': classification,
                    'passed': True
                }
                passed_count += 1
            
            # store each student's final result
            self.results.append(result)
        
        print(f"completed calculations for {len(self.students)} students")
        print(f"passed: {passed_count}, failed: {failed_count}")
        
        return self.results
    
    def get_summary_statistics(self):
        """Return basic statistics for all student results."""
        if not self.results:
            return {}
        
        # split results into passed and failed groups
        passed_results = [r for r in self.results if r['passed']]
        failed_results = [r for r in self.results if not r['passed']]
        
        classifications = {}
        
        # count each degree classification
        for result in self.results:
            cls = result['classification']
            if result['passed']:
                classifications[cls] = classifications.get(cls, 0) + 1
            else:
                classifications['Fail'] = classifications.get('Fail', 0) + 1
        
        # collect marks for statistics
        final_marks = [r['final_mark'] for r in passed_results]
        level5_marks = [r['level5_avg'] for r in passed_results if r['level5_avg'] > 0]
        level6_marks = [r['level6_avg'] for r in passed_results if r['level6_avg'] > 0]
        
        stats = {
            'total_students': len(self.results),
            'passed_students': len(passed_results),
            'failed_students': len(failed_results),
            'classifications': classifications,
            'average_level5_mark': round(sum(level5_marks) / len(level5_marks), 2) if level5_marks else 0,
            'average_level6_mark': round(sum(level6_marks) / len(level6_marks), 2) if level6_marks else 0,
            'average_final_mark': round(sum(final_marks) / len(final_marks), 2) if final_marks else 0,
            'highest_mark': round(max(final_marks), 2) if final_marks else 0,
            'lowest_mark': round(min(final_marks), 2) if final_marks else 0
        }
        
        return stats
