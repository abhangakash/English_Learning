# add_listening_pretest_questions.py
"""
Run this script using:
    python manage.py shell < add_listening_pretest_questions.py

Purpose:
    Restores the Listening pretest audio questions and MCQ options with original primary keys.
"""

import json
from listening.models import ListeningTest, AudioQuestion, AnswerOption


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
        return None
    return value

AnswerOption.objects.all().delete()
AudioQuestion.objects.all().delete()
ListeningTest.objects.all().delete()
print("✅ Deleted existing listening tests/questions/options")

test = ListeningTest.objects.create(id=6, title='English Listening Practice Test', description='Test your English listening comprehension with 5 questions covering both multiple choice and typing answers.', is_active=True)
print(f'✅ Created ListeningTest: {test.title}')

questions = {}
questions[16] = AudioQuestion.objects.create(
    id=16,
    test=test,
    order=1,
    question_type='MCQ',
    audio_filename='audio1.mp3',
    transcript='Students are advised to reach the classroom on time. Late entry is not allowed.',
    question_text='What is the main message of the audio?',
    explanation='The audio clearly states that students must be on time and late entry is not allowed, emphasizing punctuality.',
    correct_answer_text=None,
    alternative_answers=adapt_json_field(AudioQuestion, 'alternative_answers', None),
    keywords=adapt_json_field(AudioQuestion, 'keywords', '[]'),
)
print('✅ Added Listening Q1: MCQ')

questions[17] = AudioQuestion.objects.create(
    id=17,
    test=test,
    order=2,
    question_type='MCQ',
    audio_filename='audio2.mp3',
    transcript='The practical examination will be conducted on Thursday at ten thirty in the morning.',
    question_text='At what time will the practical examination begin?',
    explanation='The examination starts at 10:30 AM on Thursday.',
    correct_answer_text=None,
    alternative_answers=adapt_json_field(AudioQuestion, 'alternative_answers', None),
    keywords=adapt_json_field(AudioQuestion, 'keywords', '[]'),
)
print('✅ Added Listening Q2: MCQ')

questions[18] = AudioQuestion.objects.create(
    id=18,
    test=test,
    order=3,
    question_type='TYPING',
    audio_filename='audio3.mp3',
    transcript='First, read the instructions carefully. Then answer all the questions in sequence.',
    question_text='What should be done before answering the questions?',
    explanation='You should read the instructions carefully before starting to answer.',
    correct_answer_text='read the instructions carefully',
    alternative_answers=adapt_json_field(AudioQuestion, 'alternative_answers', '["Read the instructions carefully", "READ THE INSTRUCTIONS CAREFULLY", "Read The Instructions Carefully", "read instructions carefully", "Read instructions carefully", "READ INSTRUCTIONS CAREFULLY", "read the instructions carefully.", "Read the instructions carefully.", "READ THE INSTRUCTIONS CAREFULLY.", "read instructions carefully.", "Read instructions carefully.", "READ INSTRUCTIONS CAREFULLY.", "read the instructions", "Read the instructions", "READ THE INSTRUCTIONS", "read instructions", "Read instructions", "READ INSTRUCTIONS", "read carefully", "Read carefully", "READ CAREFULLY", "read the instructions.", "Read the instructions.", "READ THE INSTRUCTIONS.", "read instructions.", "Read instructions.", "READ INSTRUCTIONS.", "read carefully.", "Read carefully.", "READ CAREFULLY.", "you should read the instructions carefully", "You should read the instructions carefully", "YOU SHOULD READ THE INSTRUCTIONS CAREFULLY", "you must read the instructions carefully", "You must read the instructions carefully", "YOU MUST READ THE INSTRUCTIONS CAREFULLY", "first read the instructions", "First read the instructions", "FIRST READ THE INSTRUCTIONS", "read the instructions first", "Read the instructions first", "READ THE INSTRUCTIONS FIRST", "before answering read the instructions", "Before answering read the instructions", "BEFORE ANSWERING READ THE INSTRUCTIONS", "read the instructions before answering", "Read the instructions before answering", "READ THE INSTRUCTIONS BEFORE ANSWERING", "follow the instructions", "Follow the instructions", "FOLLOW THE INSTRUCTIONS", "follow instructions", "Follow instructions", "FOLLOW INSTRUCTIONS", "read them carefully", "Read them carefully", "READ THEM CAREFULLY"]'),
    keywords=adapt_json_field(AudioQuestion, 'keywords', '[]'),
)
print('✅ Added Listening Q3: TYPING')

questions[19] = AudioQuestion.objects.create(
    id=19,
    test=test,
    order=4,
    question_type='TYPING',
    audio_filename='audio4.mp3',
    transcript='The report was detailed and informative. However, it lacked clarity in some sections.',
    question_text='Is the speaker fully satisfied with the report? Why?',
    explanation='The speaker is not fully satisfied because the report lacked clarity in some sections despite being detailed.',
    correct_answer_text='no, because it lacked clarity',
    alternative_answers=adapt_json_field(AudioQuestion, 'alternative_answers', '["no", "No", "NO", "no.", "No.", "NO.", "not satisfied", "Not satisfied", "NOT SATISFIED", "not satisfied.", "Not satisfied.", "NOT SATISFIED.", "not fully satisfied", "Not fully satisfied", "NOT FULLY SATISFIED", "not fully satisfied.", "Not fully satisfied.", "NOT FULLY SATISFIED.", "no because it lacked clarity", "No because it lacked clarity", "NO BECAUSE IT LACKED CLARITY", "no, because it lacked clarity", "No, because it lacked clarity", "NO, BECAUSE IT LACKED CLARITY", "no because it lacked clarity.", "No because it lacked clarity.", "NO BECAUSE IT LACKED CLARITY.", "no, because it lacked clarity.", "No, because it lacked clarity.", "NO, BECAUSE IT LACKED CLARITY.", "it lacked clarity", "It lacked clarity", "IT LACKED CLARITY", "lacked clarity", "Lacked clarity", "LACKED CLARITY", "it lacked clarity.", "It lacked clarity.", "IT LACKED CLARITY.", "lacked clarity.", "Lacked clarity.", "LACKED CLARITY.", "it was unclear", "It was unclear", "IT WAS UNCLEAR", "unclear", "Unclear", "UNCLEAR", "it was unclear.", "It was unclear.", "IT WAS UNCLEAR.", "unclear.", "Unclear.", "UNCLEAR.", "the speaker is not satisfied because it lacked clarity", "The speaker is not satisfied because it lacked clarity", "THE SPEAKER IS NOT SATISFIED BECAUSE IT LACKED CLARITY", "he is not satisfied because it was unclear", "He is not satisfied because it was unclear", "HE IS NOT SATISFIED BECAUSE IT WAS UNCLEAR", "she is not satisfied due to lack of clarity", "She is not satisfied due to lack of clarity", "SHE IS NOT SATISFIED DUE TO LACK OF CLARITY", "detailed but not clear", "Detailed but not clear", "DETAILED BUT NOT CLEAR", "informative but unclear", "Informative but unclear", "INFORMATIVE BUT UNCLEAR", "the report was detailed but lacked clarity", "The report was detailed but lacked clarity", "THE REPORT WAS DETAILED BUT LACKED CLARITY", "not clear enough", "Not clear enough", "NOT CLEAR ENOUGH", "clarity was missing", "Clarity was missing", "CLARITY WAS MISSING", "some sections were unclear", "Some sections were unclear", "SOME SECTIONS WERE UNCLEAR"]'),
    keywords=adapt_json_field(AudioQuestion, 'keywords', '[]'),
)
print('✅ Added Listening Q4: TYPING')

questions[20] = AudioQuestion.objects.create(
    id=20,
    test=test,
    order=5,
    question_type='TYPING',
    audio_filename='audio5.mp3',
    transcript='She had prepared well for the interview. Still, nervousness prevented her from answering confidently.',
    question_text='What affected her performance during the interview?',
    explanation='Her nervousness affected her performance, preventing her from answering confidently despite good preparation.',
    correct_answer_text='nervousness',
    alternative_answers=adapt_json_field(AudioQuestion, 'alternative_answers', '[\n  "nervousness",\n  "Nervousness",\n  "NERVOUSNESS",\n  "nerves",\n  "Nerves",\n  "NERVES",\n  "anxiety",\n  "Anxiety",\n  "ANXIETY",\n  "stress",\n  "Stress",\n  "STRESS",\n  "tension",\n  "Tension",\n  "TENSION",\n  "nervousness.",\n  "Nervousness.",\n  "NERVOUSNESS.",\n  "nerves.",\n  "Nerves.",\n  "NERVES.",\n  "anxiety.",\n  "Anxiety.",\n  "ANXIETY.",\n  "stress.",\n  "Stress.",\n  "STRESS.",\n  "tension.",\n  "Tension.",\n  "TENSION.",\n  "she was nervous",\n  "She was nervous",\n  "SHE WAS NERVOUS",\n  "she was nervous.",\n  "She was nervous.",\n  "SHE WAS NERVOUS.",\n  "she was anxious",\n  "She was anxious",\n  "SHE WAS ANXIOUS",\n  "she was anxious.",\n  "She was anxious.",\n  "SHE WAS ANXIOUS.",\n  "her nervousness",\n  "Her nervousness",\n  "HER NERVOUSNESS",\n  "her nervousness.",\n  "Her nervousness.",\n  "HER NERVOUSNESS.",\n  "her anxiety",\n  "Her anxiety",\n  "HER ANXIETY",\n  "her anxiety.",\n  "Her anxiety.",\n  "HER ANXIETY.",\n  "she felt nervous",\n  "She felt nervous",\n  "SHE FELT NERVOUS",\n  "she felt nervous.",\n  "She felt nervous.",\n  "SHE FELT NERVOUS.",\n  "felt nervous",\n  "Felt nervous",\n  "FELT NERVOUS",\n  "felt nervous.",\n  "Felt nervous.",\n  "FELT NERVOUS.",\n  "nervousness affected her",\n  "Nervousness affected her",\n  "NERVOUSNESS AFFECTED HER",\n  "nerves affected her",\n  "Nerves affected her",\n  "NERVES AFFECTED HER",\n  "anxiety affected her",\n  "Anxiety affected her",\n  "ANXIETY AFFECTED HER",\n  "she was too nervous to answer confidently",\n  "She was too nervous to answer confidently",\n  "SHE WAS TOO NERVOUS TO ANSWER CONFIDENTLY",\n  "nervousness prevented her from answering confidently",\n  "Nervousness prevented her from answering confidently",\n  "NERVOUSNESS PREVENTED HER FROM ANSWERING CONFIDENTLY",\n  "her nervousness affected her performance",\n  "Her nervousness affected her performance",\n  "HER NERVOUSNESS AFFECTED HER PERFORMANCE",\n  "she couldn\'t answer confidently because of nervousness",\n  "She couldn\'t answer confidently because of nervousness",\n  "SHE COULDN\'T ANSWER CONFIDENTLY BECAUSE OF NERVOUSNESS",\n  "lack of confidence",\n  "Lack of confidence",\n  "LACK OF CONFIDENCE",\n  "she lacked confidence",\n  "She lacked confidence",\n  "SHE LACKED CONFIDENCE",\n  "self doubt",\n  "Self doubt",\n  "SELF DOUBT",\n  "stage fright",\n  "Stage fright",\n  "STAGE FRIGHT",\n  "performance anxiety",\n  "Performance anxiety",\n  "PERFORMANCE ANXIETY",\n  "interview nerves",\n  "Interview nerves",\n  "INTERVIEW NERVES"\n]'),
    keywords=adapt_json_field(AudioQuestion, 'keywords', '[]'),
)
print('✅ Added Listening Q5: TYPING')

AnswerOption.objects.create(id=49, question=questions[16], text='Students should leave early', is_correct=False)
AnswerOption.objects.create(id=50, question=questions[16], text='Students must be punctual', is_correct=True)
AnswerOption.objects.create(id=51, question=questions[16], text='Class is cancelled', is_correct=False)
AnswerOption.objects.create(id=52, question=questions[16], text='Late entry is allowed', is_correct=False)
AnswerOption.objects.create(id=53, question=questions[17], text='10:00', is_correct=False)
AnswerOption.objects.create(id=54, question=questions[17], text='10:30', is_correct=True)
AnswerOption.objects.create(id=55, question=questions[17], text='11:00', is_correct=False)
AnswerOption.objects.create(id=56, question=questions[17], text='9:30', is_correct=False)
print('✅ Added MCQ answer options')
print('🎉 Listening pretest question bank restored successfully.')
