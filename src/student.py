# src/student.py

class Student:
    """
    Represents a student with their ID and module marks.
    Handles calculation of weighted averages and degree classification.
    """
    
    def __init__(self, student_id):
        """
        initializes student with id and marks dictionary
        """
        self.student_id = student_id
        self.marks = {}   # stores module_code = mark
    
    def add_mark(self, module_code, mark):
        """
        add or update the student's mark for a module
        """
        self.marks[module_code] = mark
    
    def get_modules_by_level(self, level, modules_dict):
        """
        gets all modules for a specific year level
        returns list of tuples with (module_obj, mark)
        """
        result = []
        for code, mark in self.marks.items():
            if code in modules_dict:
                module = modules_dict[code]
                
                # only include modules from the requested level
                if module.level == level:
                    result.append((module, mark))
        return result
    
    def has_passed_all(self):
        """
        checks if student passed everything
        need at least 40% on all modules to pass
        """
        # fail immediately if any module mark is below 40
        for mark in self.marks.values():
            if mark < 40:
                return False
        return True
    
    def calculate_best_100_credits_greedy(self, level, modules_dict):
        """
        Calculate weighted average using best modules up to 100 credits.
        Greedy selection: sort by mark descending and take highest scoring modules.
        """
        level_modules = self.get_modules_by_level(level, modules_dict)
        
        if not level_modules:
            return 0.0, 0
        
        # sort modules by mark (highest first)
        sorted_modules = sorted(level_modules, key=lambda x: x[1], reverse=True)
        
        selected = []
        total_credits = 0
        
        # greedily select highest scoring modules without exceeding 100 credits
        for module, mark in sorted_modules:
            if total_credits + module.credits <= 100:
                selected.append((module, mark))
                total_credits += module.credits
        
        if total_credits == 0:
            return 0.0, 0
        
        # calculate weighted average based on credits
        weighted_sum = sum(module.credits * mark for module, mark in selected)
        weighted_average = weighted_sum / total_credits
        
        return weighted_average, total_credits
    
    def calculate_all_credits_average(self, level, modules_dict):
        """
        calculates weighted average for all modules at a level
        used for level 6 (all modules count).
        """
        level_modules = self.get_modules_by_level(level, modules_dict)
        
        if not level_modules:
            return 0.0, 0
        
        total_credits = sum(module.credits for module, mark in level_modules)
        
        if total_credits == 0:
            return 0.0, 0
        
        # weighted average across all credits
        weighted_sum = sum(module.credits * mark for module, mark in level_modules)
        weighted_average = weighted_sum / total_credits
        
        return weighted_average, total_credits
    
    def calculate_final_aggregate(self, level5_avg, level6_avg):
        """
        combines level 5 and 6 marks in 1:3 ratio
        level 6 counts 3 times as much as level 5
        """
        # uwe weighting formula
        return (level6_avg * 3 + level5_avg) / 4
    
    def get_degree_classification(self, final_mark):
        """
        converts final percentage into degree class
        follows uwe regulations
        """
        if final_mark >= 70:
            return "First Class"
        elif final_mark >= 60:
            return "Second Class (Upper Division)"
        elif final_mark >= 50:
            return "Second Class (Lower Division)"
        elif final_mark >= 40:
            return "Third Class"
        else:
            return "Fail"
