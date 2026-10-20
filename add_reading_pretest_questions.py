# add_reading_pretest_questions.py
"""
Run this script using:
    python manage.py shell < add_reading_pretest_questions.py

Purpose:
    Restores the Reading pretest passages and questions with original primary keys.
"""

from reading.models import Test, Paragraph, Question

Question.objects.all().delete()
Paragraph.objects.all().delete()
Test.objects.all().delete()
print("✅ Deleted existing reading tests/passages/questions")

test = Test.objects.create(id=1, title='Reading Comprehension Test', description='Test your English reading skills with rubric-based assessment')
print(f'✅ Created Reading Test: {test.title}')

paragraphs = {}
paragraphs[5] = Paragraph.objects.create(id=5, test=test, order=1, content='Many students struggle with English not because they lack knowledge, but because they rarely use the language outside the classroom. Regular practice through reading, listening, and speaking can gradually improve confidence and fluency.')
print('✅ Added Paragraph 1')

paragraphs[6] = Paragraph.objects.create(id=6, test=test, order=2, content='Learning a language requires more than memorizing grammar rules. Students develop stronger communication skills when they actively use the language in meaningful situations. Activities such as discussions, presentations, and problem-solving tasks allow learners to express ideas and interact with others. When students participate in such activities regularly, their confidence gradually increases and they become more comfortable using the language in real-life situations.')
print('✅ Added Paragraph 2')

paragraphs[7] = Paragraph.objects.create(id=7, test=test, order=3, content="In today's academic environment, students are exposed to a large amount of information through textbooks, online articles, and multimedia resources. Although this abundance of information offers valuable learning opportunities, it also requires students to read more thoughtfully. Simply collecting facts does not lead to real understanding. Effective learners evaluate the credibility of sources, compare different perspectives, and interpret ideas carefully. By developing such critical reading habits, students become more capable of analysing information and applying knowledge in practical situations.")
print('✅ Added Paragraph 3')

Question.objects.create(
    id=6,
    test=test,
    paragraph=paragraphs[5],
    order=1,
    question_text='What is the passage mainly about?',
    option1='Classroom teaching methods',
    option2='Importance of grammar',
    option3='Need for regular language practice',
    option4='Examination patterns',
    correct_option=3,
    parameter_type='MAIN_IDEA',
    weight=20,
)
print('✅ Added Reading Q1')

Question.objects.create(
    id=7,
    test=test,
    paragraph=paragraphs[6],
    order=2,
    question_text='What is the main idea of the passage?',
    option1='Grammar is not important in language learning',
    option2='Active use of language improves communication skills',
    option3='Students dislike classroom activities',
    option4='Presentations are difficult for students',
    correct_option=2,
    parameter_type='MAIN_IDEA',
    weight=20,
)
print('✅ Added Reading Q2')

Question.objects.create(
    id=8,
    test=test,
    paragraph=paragraphs[6],
    order=3,
    question_text='According to the passage, which activity helps students improve communication skills?',
    option1='Memorizing vocabulary',
    option2='Participating in discussions',
    option3='Avoiding interaction',
    option4='Reading dictionaries',
    correct_option=2,
    parameter_type='DETAIL',
    weight=20,
)
print('✅ Added Reading Q3')

Question.objects.create(
    id=9,
    test=test,
    paragraph=paragraphs[6],
    order=4,
    question_text='The word "meaningful" in the passage most nearly means:',
    option1='useless',
    option2='important and purposeful',
    option3='confusing',
    option4='temporary',
    correct_option=2,
    parameter_type='VOCAB',
    weight=20,
)
print('✅ Added Reading Q4')

Question.objects.create(
    id=10,
    test=test,
    paragraph=paragraphs[6],
    order=5,
    question_text='The writer suggests that confidence improves when students:',
    option1='avoid speaking in class',
    option2='practice language regularly',
    option3='study grammar books only',
    option4='learn vocabulary lists',
    correct_option=2,
    parameter_type='LOGICAL',
    weight=20,
)
print('✅ Added Reading Q5')

Question.objects.create(
    id=11,
    test=test,
    paragraph=paragraphs[7],
    order=6,
    question_text='Which statement best expresses the main idea of the passage?',
    option1='Students should avoid using online resources',
    option2='Access to information requires students to develop critical reading skills',
    option3='Textbooks are the only reliable sources of knowledge',
    option4='Multimedia resources replace traditional learning methods',
    correct_option=2,
    parameter_type='MAIN_IDEA',
    weight=20,
)
print('✅ Added Reading Q6')

Question.objects.create(
    id=12,
    test=test,
    paragraph=paragraphs[7],
    order=7,
    question_text='According to the passage, effective learners usually:',
    option1='collect as much information as possible',
    option2='rely only on textbooks',
    option3='evaluate and interpret information carefully',
    option4='ignore different viewpoints',
    correct_option=3,
    parameter_type='DETAIL',
    weight=20,
)
print('✅ Added Reading Q7')

Question.objects.create(
    id=13,
    test=test,
    paragraph=paragraphs[7],
    order=8,
    question_text='The word "abundance" in the passage most nearly means:',
    option1='shortage',
    option2='large quantity',
    option3='confusion',
    option4='limitation',
    correct_option=2,
    parameter_type='VOCAB',
    weight=20,
)
print('✅ Added Reading Q8')

print('🎉 Reading pretest question bank restored successfully.')
