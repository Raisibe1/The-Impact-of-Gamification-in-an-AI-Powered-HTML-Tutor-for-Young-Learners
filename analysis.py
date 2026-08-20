import sqlite3
import pandas as pd

DB_NAME = "tutor.db"

conn = sqlite3.connect(DB_NAME)

print("="*60)
print("TUTOR DATABASE ANALYSIS")
print("="*60)

# 1. STUDENTS table
print("\n1. STUDENTS TABLE")
df_students = pd.read_sql_query("SELECT * FROM students", conn)
print(df_students)
print(f"Total students: {len(df_students)}")

# 2. WEBDEV_MODULES table
print("\n2. WEBDEV MODULES")
df_modules = pd.read_sql_query("SELECT * FROM webdev_modules", conn)
print(df_modules)
print(f"Total modules: {len(df_modules)}")

# 3. STUDENT_PROGRESS table
print("\n3. STUDENT PROGRESS")
df_progress = pd.read_sql_query("SELECT * FROM student_progress", conn)
print(df_progress.head())
print(f"Total progress records: {len(df_progress)}")

# 4. CODE_SUBMISSIONS table
print("\n4. CODE SUBMISSIONS")
df_code = pd.read_sql_query("SELECT * FROM code_submissions", conn)
print(df_code.head())
print(f"Total submissions: {len(df_code)}")

# 5. BEHAVIORAL_DATA table
print("\n5. BEHAVIORAL DATA")
df_behavior = pd.read_sql_query("SELECT * FROM behavioral_data", conn)
print(df_behavior.head())
print(f"Total behavioral records: {len(df_behavior)}")

# 6. ENGAGEMENT_DATA table
print("\n6. ENGAGEMENT DATA")
df_engagement = pd.read_sql_query("SELECT * FROM engagement_data", conn)
print(df_engagement.head())
print(f"Total engagement records: {len(df_engagement)}")

# 7. PERFORMANCE_DATA table
print("\n7. PERFORMANCE DATA")
df_performance = pd.read_sql_query("SELECT * FROM performance_data", conn)
print(df_performance.head())
print(f"Total performance records: {len(df_performance)}")

# 8. AI_INTERACTIONS table
print("\n8. AI INTERACTIONS")
df_ai = pd.read_sql_query("SELECT * FROM ai_interactions", conn)
print(df_ai.head())
print(f"Total AI interactions: {len(df_ai)}")

# 9. MISTAKE_PATTERNS table
print("\n9. MISTAKE PATTERNS")
df_mistakes = pd.read_sql_query("SELECT * FROM mistake_patterns", conn)
print(df_mistakes.head())
print(f"Total mistake patterns: {len(df_mistakes)}")

# 10. PROJECTS table
print("\n10. PROJECTS")
df_projects = pd.read_sql_query("SELECT * FROM projects", conn)
print(df_projects.head())
print(f"Total projects: {len(df_projects)}")

conn.close()