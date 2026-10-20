# add_writing_pretest_questions.py
"""
Run this script using:
    python manage.py shell < add_writing_pretest_questions.py

Purpose:
    Restores the Writing pretest question bank with original primary keys.
"""

import json
from writing.models import WritingTest, WritingQuestion


def adapt_json_field(model, field_name, value):
    field = model._meta.get_field(field_name)
    if field.get_internal_type() == "JSONField":
        if value in (None, ""):
            return []
        if isinstance(value, str):
            try:
                return json.loads(value)
            except Exception:
                return value
        return value
    if isinstance(value, (list, dict)):
        return json.dumps(value)
    if value is None:
        return ""
    return value

WritingQuestion.objects.all().delete()
WritingTest.objects.all().delete()
print("✅ Deleted existing writing tests/questions")

test = WritingTest.objects.create(id=3, title='English Writing Test', description='Test your English writing skills with 5 different exercises covering grammar, vocabulary, organization, spelling, and paragraph writing.', is_active=True)
print(f'✅ Created WritingTest: {test.title}')

q = WritingQuestion.objects.create(
    id=11,
    test=test,
    order=1,
    question_type='fill_blanks',
    prompt='Fill in the blanks with the correct word:\n\n1. She ___ (go/goes) to college every day.\n2. The students ___ (is/are) in the classroom.\n3. This is ___ useful book. (a / an)\n\nWrite your answers separated by commas (e.g., goes, are, a)',
    correct_answer='goes, are, a',
    acceptable_answers=adapt_json_field(WritingQuestion, 'acceptable_answers', '["goes are a", "goes,are,a"]'),
    explanation="Subject-verb agreement: She goes (third person singular), Students are (plural), 'a' before consonant sound 'useful'",
    picture_filename='',
    required_keywords=adapt_json_field(WritingQuestion, 'required_keywords', '[]'),
    min_sentences=2,
    min_words=15,
    max_words=50,
    audio_filename='',
)
print(f'✅ Added Writing Q{q.order}: {q.question_type}')

q = WritingQuestion.objects.create(
    id=12,
    test=test,
    order=2,
    question_type='sentence_order',
    prompt='Arrange the sentences in a logical order:\n\nA. We submitted the assignment.\nB. The teacher explained the topic.\nC. The class started at ten.\n\nWrite the letters in order (e.g., C, B, A)',
    correct_answer='C, B, A',
    acceptable_answers=adapt_json_field(WritingQuestion, 'acceptable_answers', '["CBA", "c b a", "c,b,a"]'),
    explanation='First class starts, then teacher explains, then students submit',
    picture_filename='',
    required_keywords=adapt_json_field(WritingQuestion, 'required_keywords', '[]'),
    min_sentences=2,
    min_words=15,
    max_words=50,
    audio_filename='',
)
print(f'✅ Added Writing Q{q.order}: {q.question_type}')

q = WritingQuestion.objects.create(
    id=13,
    test=test,
    order=3,
    question_type='sentence_rewrite',
    prompt="Rewrite the sentence correctly with proper spelling and punctuation:\r\n\r\n'comunication skills are important however students often ignore punctution grammer and clarity'",
    correct_answer='Communication skills are important; however, students often ignore punctuation, grammar, and clarity.',
    acceptable_answers=adapt_json_field(WritingQuestion, 'acceptable_answers', '["Communication skills are important; however, students often ignore punctuation, grammar, and clarity.", "Communication skills are important; however, students often ignore punctuation, grammar and clarity."]'),
    explanation="Capitalize first letter, correct spelling (communication, punctuation, grammar), add semicolon before 'however', add commas in list",
    picture_filename='',
    required_keywords=adapt_json_field(WritingQuestion, 'required_keywords', '[]'),
    min_sentences=2,
    min_words=15,
    max_words=50,
    audio_filename='',
)
print(f'✅ Added Writing Q{q.order}: {q.question_type}')

q = WritingQuestion.objects.create(
    id=14,
    test=test,
    order=4,
    question_type='spelling_mcq',
    prompt='Choose the correctly spelled word (write the letters separated by commas):\r\n\r\n1. a) recieve\u2003b) receive   c) recive  d) receieve\r\n2. a) definately\u2003b) definitely  c) difinetly  d) defenetly\r\n3. a) seperate\u2003b) separate    c)sepereta  d)seprate\r\n\r\nYour answers (format: b, b, b)',
    correct_answer='b, d, a',
    acceptable_answers=adapt_json_field(WritingQuestion, 'acceptable_answers', '["bda", "b d a", "b,d,a", "b, d, a"]'),
    explanation='Correct spellings: receive, definitely, separate',
    picture_filename='',
    required_keywords=adapt_json_field(WritingQuestion, 'required_keywords', '[]'),
    min_sentences=2,
    min_words=15,
    max_words=50,
    audio_filename='',
)
print(f'✅ Added Writing Q{q.order}: {q.question_type}')

q = WritingQuestion.objects.create(
    id=15,
    test=test,
    order=5,
    question_type='paragraph_writing',
    prompt='Write a paragraph of 5–6 sentences using the clues given below:\r\n\r\nClue words:\r\ntime management\r\nplanning\r\ndaily routine\r\nstress\r\nsuccess\r\n\r\nYour paragraph:',
    correct_answer='["Time management is an important skill for everyone. With proper planning, we can organize our daily routine in a better way. When our work is well planned, we feel less stress. This helps us stay focused on our goals. Good habits make our life more disciplined. All these things together lead us to success."]',
    acceptable_answers=adapt_json_field(WritingQuestion, 'acceptable_answers', '["Good time management is important for a successful life. With proper planning, we can organize our daily routine and complete our tasks on time. This helps reduce stress and leads us toward success.", "When we follow a fixed daily routine, our time management becomes better. Careful planning helps us avoid stress, and this habit slowly brings success in our studies and life.", "Many students fail because of poor time management. If they do proper planning and follow a simple daily routine, they can reduce stress and achieve success easily.", "Planning our work helps improve time management in our daily routine. When we manage our time well, we feel less stress and move closer to success.", "Without planning, time management becomes difficult. A well-organized daily routine reduces stress and increases the chances of success in life.", "Proper time management teaches us how to plan our day. With good planning, our daily routine becomes smooth, stress decreases, and success becomes possible.", "Students who follow a daily routine learn the value of time management. Through proper planning, they can control stress and achieve success in their goals.", "Good time management and careful planning make our daily routine easier. When our work is organized, we feel less stress and move toward success with confidence.", "A healthy daily routine helps us practice good time management. Through proper planning, we can complete our tasks on time. When work is done on time, stress becomes less. We feel more confident and calm. This positive feeling motivates us to work harder. In this way, we can achieve success."]'),
    explanation='Write a coherent paragraph using all clue words. Focus on grammar, vocabulary, organization, and spelling.',
    picture_filename='',
    required_keywords=adapt_json_field(WritingQuestion, 'required_keywords', '[]'),
    min_sentences=2,
    min_words=15,
    max_words=50,
    audio_filename='',
)
print(f'✅ Added Writing Q{q.order}: {q.question_type}')

print('🎉 Writing pretest question bank restored successfully.')
