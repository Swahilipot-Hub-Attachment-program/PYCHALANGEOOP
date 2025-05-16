class Attachee:
    """Class representing an intern (attachee) at the tech innovation hub"""
    
    def __init__(self, name, division):
        """
        Initialize an attachee with name and division
        Args:
            name (str): Full name of the attachee
            division (str): One of the 4 hub divisions
        """
        self.name = name
        self.division = division
        self.tasks = []
        self.feedback = []
        self.score = 0
        
    def assign_task(self, task_description, deadline=None):
        """
        Assign a new task to the attachee
        Args:
            task_description (str): Description of the task
            deadline (str, optional): Due date for the task
        """
        task = {
            'description': task_description,
            'completed': False,
            'deadline': deadline
        }
        self.tasks.append(task)
        print(f"New task assigned to {self.name}: {task_description}")
        
    def add_feedback(self, feedback_text, rating):
        """
        Record feedback for the attachee
        Args:
            feedback_text (str): Written feedback
            rating (int): Numerical rating (1-10)
        """
        if not 1 <= rating <= 10:
            print("Error: Rating must be between 1 and 10")
            return
            
        feedback = {
            'text': feedback_text,
            'rating': rating,
            'date': datetime.date.today().strftime("%Y-%m-%d")
        }
        self.feedback.append(feedback)
        self._calculate_score()
        print(f"Feedback recorded for {self.name}")
        
    def _calculate_score(self):
        """Calculate average score from all feedback ratings"""
        if not self.feedback:
            self.score = 0
            return
            
        total = sum(fb['rating'] for fb in self.feedback)
        self.score = round(total / len(self.feedback), 1)
        
    def complete_task(self, task_index):
        """
        Mark a task as completed
        Args:
            task_index (int): Index of the task to mark complete
        """
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index]['completed'] = True
            print(f"Task marked complete: {self.tasks[task_index]['description']}")
        else:
            print("Invalid task index")
            
    def get_performance_report(self):
        """Generate a performance report for the attachee"""
        completed_tasks = sum(1 for task in self.tasks if task['completed'])
        completion_rate = (completed_tasks / len(self.tasks)) * 100 if self.tasks else 0
        
        return {
            'name': self.name,
            'division': self.division,
            'total_tasks': len(self.tasks),
            'completed_tasks': completed_tasks,
            'completion_rate': round(completion_rate, 1),
            'feedback_count': len(self.feedback),
            'average_score': self.score
        }


class DivisionManager:
    """Class to manage attachees across all divisions"""
    
    DIVISIONS = [
        "Engineering",
        "Tech Programs", 
        "Radio Support",
        "Hub Support"
    ]
    
    def __init__(self):
        """Initialize division manager with empty lists for each division"""
        self.attachees = {division: [] for division in self.DIVISIONS}
        
    def add_attachee(self, name, division):
        """
        Add a new attachee to the system
        Args:
            name (str): Full name of attachee
            division (str): Valid division name
        Returns:
            bool: True if successful, False if division is invalid
        """
        if division not in self.DIVISIONS:
            print(f"Error: Invalid division. Must be one of {', '.join(self.DIVISIONS)}")
            return False
            
        new_attachee = Attachee(name, division)
        self.attachees[division].append(new_attachee)
        print(f"Added new attachee: {name} to {division} division")
        return True
        
    def assign_division_task(self, division, task_description):
        """
        Assign a task to all attachees in a division
        Args:
            division (str): Division name
            task_description (str): Task to assign
        """
        if division not in self.attachees:
            print("Invalid division")
            return
            
        for attachee in self.attachees[division]:
            attachee.assign_task(task_description)
            
    def get_division_performance(self, division):
        """
        Get performance summary for a division
        Args:
            division (str): Division name
        Returns:
            list: Performance reports for all attachees in division
        """
        if division not in self.attachees:
            print("Invalid division")
            return []
            
        return [attachee.get_performance_report() for attachee in self.attachees[division]]
        
    def display_division_summary(self, division):
        """
        Display a formatted summary of a division's performance
        Args:
            division (str): Division name
        """
        if division not in self.attachees:
            print("Invalid division")
            return
            
        print(f"\n{'='*30}")
        print(f"{division.upper()} DIVISION SUMMARY")
        print(f"{'='*30}")
        
        performance_reports = self.get_division_performance(division)
        
        if not performance_reports:
            print("No attachees in this division")
            return
            
        for report in performance_reports:
            print(f"\nAttachee: {report['name']}")
            print(f"- Tasks: {report['completed_tasks']}/{report['total_tasks']} completed ({report['completion_rate']}%)")
            print(f"- Feedback received: {report['feedback_count']}")
            print(f"- Average score: {report['average_score']}/10")
            
        avg_score = sum(r['average_score'] for r in performance_reports) / len(performance_reports)
        print(f"\nDivision average score: {round(avg_score, 1)}/10")


# Example Usage
if __name__ == "__main__":
    import datetime
    
    # Initialize division manager
    hub_manager = DivisionManager()
    
    # Add attachees to different divisions
    hub_manager.add_attachee("Alice Johnson", "Engineering")
    hub_manager.add_attachee("Bob Smith", "Engineering")
    hub_manager.add_attachee("Carol Williams", "Tech Programs")
    hub_manager.add_attachee("David Brown", "Radio Support")
    hub_manager.add_attachee("Eve Davis", "Hub Support")
    
    # Assign tasks to divisions
    hub_manager.assign_division_task("Engineering", "Review codebase for optimization opportunities")
    hub_manager.assign_division_task("Tech Programs", "Prepare workshop materials for next week")
    
    # Add individual tasks
    engineering_team = hub_manager.attachees["Engineering"]
    engineering_team[0].assign_task("Fix login page UI bugs", "2023-11-15")
    engineering_team[1].assign_task("Implement new API endpoint", "2023-11-20")
    
    # Record feedback
    engineering_team[0].add_feedback("Excellent problem-solving skills", 9)
    engineering_team[0].add_feedback("Needs to improve documentation", 7)
    engineering_team[1].add_feedback("Great teamwork and communication", 10)
    
    # Mark some tasks complete
    engineering_team[0].complete_task(0)
    engineering_team[1].complete_task(1)
    
    # Display division summaries
    for division in hub_manager.DIVISIONS:
        hub_manager.display_division_summary(division)