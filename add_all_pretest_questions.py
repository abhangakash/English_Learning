# add_all_pretest_questions.py
"""
Run this script using:
    python manage.py shell < add_all_pretest_questions.py

This restores Writing, Reading, and Listening pretest question banks.
Speaking has no question table in the uploaded database; its prompts appear to be hardcoded in views/templates.
"""

exec(open("add_writing_pretest_questions.py", encoding="utf-8").read())
print("\n" + "="*70 + "\n")
exec(open("add_reading_pretest_questions.py", encoding="utf-8").read())
print("\n" + "="*70 + "\n")
exec(open("add_listening_pretest_questions.py", encoding="utf-8").read())
print("\n🎉 ALL PRETEST QUESTION BANKS RESTORED SUCCESSFULLY")
