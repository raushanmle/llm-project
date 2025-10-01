import sqlite3
import random

# Connect to SQLite
connection = sqlite3.connect("student.db")
cursor = connection.cursor()

# Drop table if exists and create new one
cursor.execute("DROP TABLE IF EXISTS STUDENT")
table_info = """
CREATE TABLE STUDENT(
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
)
"""
cursor.execute(table_info)

# Generate 1000 random student records efficiently
def generate_random_data(num_records=1000):
    # Sample data pools
    first_names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack',
                   'Kate', 'Liam', 'Maya', 'Noah', 'Olivia', 'Peter', 'Quinn', 'Ruby', 'Sam', 'Tina',
                   'Uma', 'Victor', 'Wendy', 'Xavier', 'Yara', 'Zoe', 'Alex', 'Blake', 'Casey', 'Drew']
    
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                  'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']
    
    classes = ['Data Science', 'Machine Learning', 'Web Development', 'DevOps', 'Cloud Computing', 
               'Cybersecurity', 'Mobile Development', 'AI Engineering', 'Data Engineering', 'Software Engineering']
    
    sections = ['A', 'B', 'C']
    
    # Generate data in bulk
    students_data = []
    for i in range(num_records):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        class_name = random.choice(classes)
        section = random.choice(sections)
        # Generate realistic marks with some distribution
        if section == 'A':  # High performers
            marks = random.randint(80, 100)
        elif section == 'B':  # Medium performers
            marks = random.randint(60, 89)
        else:  # Section C - Lower performers
            marks = random.randint(35, 79)
            
        students_data.append((name, class_name, section, marks))
    
    return students_data

# Generate and insert 1000 records using executemany (much faster)
print("Generating 1000 random student records...")
random_data = generate_random_data(1000)

# Bulk insert - much more efficient than individual inserts
cursor.executemany("INSERT INTO STUDENT VALUES (?, ?, ?, ?)", random_data)
print(f"Successfully inserted {len(random_data)} records!")

## Display all the records
print("The inserted records are")
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

## Commit your changes in the database
connection.commit()
connection.close()
