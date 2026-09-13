#Alexander Lund
#CIS261
#WK10 VIBE Coding

"""Student Grade Calculator."""

from dataclasses import dataclass


FILE_NAME = "student_grades.txt"


def print_header(title):
    """Print a bold-style section header with equal-sign borders."""
    border = "=" * max(len(title) + 8, 30)
    print(f"\n{border}")
    print(f"  {title}")
    print(border)


@dataclass
class Student:
	"""Store a student's scores and calculated results."""

	name: str
	student_id: str
	test1: float
	test2: float
	test3: float
	average: float = 0.0
	grade: str = "F"

	def __post_init__(self):
		self.calculate_grade()

	def calculate_grade(self):
		self.average = (self.test1 + self.test2 + self.test3) / 3
		if self.average >= 90:
			self.grade = "A"
		elif self.average >= 80:
			self.grade = "B"
		elif self.average >= 70:
			self.grade = "C"
		elif self.average >= 60:
			self.grade = "D"
		else:
			self.grade = "F"


def get_score(test_number):
	"""Prompt until a valid score from 0 through 100 is entered."""
	while True:
		try:
			score = float(input(f"Enter Test {test_number} score (0-100): "))
			if 0 <= score <= 100:
				return score
			print("Score must be between 0 and 100.")
		except ValueError:
			print("Please enter a valid number.")


def add_student(students):
	"""Prompt for and add one student record."""
	print_header("Add Student")
	name = input("Enter student name: ").strip()
	while not name:
		print("Student name cannot be blank.")
		name = input("Enter student name: ").strip()

	student_id = input("Enter student ID: ").strip()
	while not student_id:
		print("Student ID cannot be blank.")
		student_id = input("Enter student ID: ").strip()

	student = Student(
		name,
		student_id,
		get_score(1),
		get_score(2),
		get_score(3),
	)
	students.append(student)
	print(f"Added {student.name}. Average: {student.average:.2f}, Grade: {student.grade}")


def display_students(students):
	"""Display all student records in a formatted table."""
	if not students:
		print_header("No student records found")
		return

	print_header("Student Records")
	print("-" * 86)
	print(f"{'Name':<24}{'ID':<14}{'Test 1':>10}{'Test 2':>10}{'Test 3':>10}{'Average':>10}{'Grade':>8}")
	print("-" * 86)
	for student in students:
		print(
			f"{student.name:<24.24}{student.student_id:<14.14}"
			f"{student.test1:>10.2f}{student.test2:>10.2f}{student.test3:>10.2f}"
			f"{student.average:>10.2f}{student.grade:>8}"
		)
	print("-" * 86)


def display_statistics(students):
	"""Display highest, lowest, and class average scores."""
	if not students:
		print_header("No statistics available. Add a student first.")
		return

	averages = [student.average for student in students]
	print_header("Class Statistics")
	print(f"Highest average: {max(averages):.2f}")
	print(f"Lowest average:  {min(averages):.2f}")
	print(f"Class average:   {sum(averages) / len(averages):.2f}")


def search_student(students):
	"""Search for and display students by name, ignoring case."""
	search_name = input("\nEnter the student name to search for: ").strip().lower()
	matches = [student for student in students if search_name in student.name.lower()]
	if not matches:
		print("No matching student found.")
		return
	display_students(matches)


def save_students(students, file_name=FILE_NAME):
	"""Save student records using the required pipe-delimited format."""
	try:
		with open(file_name, "w", encoding="utf-8") as file:
			for student in students:
				file.write(
					f"{student.name}|{student.student_id}|{student.test1}|"
					f"{student.test2}|{student.test3}|{student.average}|{student.grade}\n"
				)
		print(f"Saved {len(students)} student record(s) to {file_name}.")
		return True
	except OSError as error:
		print(f"Error saving student records: {error}")
		return False


def load_students(file_name=FILE_NAME):
	"""Load valid student records from the pipe-delimited file."""
	students = []
	try:
		with open(file_name, "r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				fields = line.rstrip("\n").split("|")
				if len(fields) != 7:
					print(f"Skipping invalid record on line {line_number}.")
					continue
				try:
					students.append(
						Student(
							fields[0],
							fields[1],
							float(fields[2]),
							float(fields[3]),
							float(fields[4]),
						)
					)
				except ValueError:
					print(f"Skipping invalid record on line {line_number}.")
		print(f"Loaded {len(students)} student record(s) from {file_name}.")
	except FileNotFoundError:
		print(f"No existing {file_name} file found. Starting with an empty list.")
	except OSError as error:
		print(f"Error loading student records: {error}")
	return students


def display_menu():
	"""Display the program menu."""
	print_header("Student Grade Calculator")
	print("1. Add student")
	print("2. Display all students")
	print("3. Display class statistics")
	print("4. Search for a student")
	print("5. Save records")
	print("Press ESC, or enter 6, to save and exit")


def main():
	"""Run the Student Grade Calculator."""
	students = load_students()
	while True:
		display_menu()
		choice = input("Choose an option: ")
		if choice == "\x1b" or choice == "6":
			save_students(students)
			print("Goodbye!")
			break
		if choice == "1":
			add_student(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			display_statistics(students)
		elif choice == "4":
			search_student(students)
		elif choice == "5":
			save_students(students)
		else:
			print("Invalid option. Please choose 1 through 5, or press ESC to exit.")


if __name__ == "__main__":
	main()

