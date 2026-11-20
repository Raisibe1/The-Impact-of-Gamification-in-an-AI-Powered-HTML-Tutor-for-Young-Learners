"""Refactored from the supplied CodeVerse API.py; route contracts are preserved."""
# Private assessment answer keys. Never import into frontend code.
BENCHMARK_MCQ_KEY = dict(enumerate(
    (
        "BACBA"
        "BCABC"
        "ABCBA"
        "CBACB"
        "ACBAC"
        "BACAB"
        "ACBAC"
        "ABACB"
    ),
    start=1
))

_PRE_ANSWERS = {
    "2": "B", "3": "B", "4": "A", "5": "C", "6": "B",
    "7": "A", "8": "C", "9": "B", "10": "A", "11": "A",
}
_PRE_BACKGROUNDS = {
    'Yes, I have built my own web pages before.',
    'Yes, but I have only seen it or tried it a tiny bit.',
    'No, I have never done HTML before.',
}

# Only the backend has this key. Matches the original 50-question final exam.
_FINAL_MCQ_ANSWERS = {
    1:'B', 2:'A', 3:'C', 4:'B', 5:'A',
    6:'B', 7:'C', 8:'A', 9:'B', 10:'C',
    11:'A', 12:'B', 13:'C', 14:'B', 15:'A',
    16:'C', 17:'B', 18:'A', 19:'C', 20:'B',
    21:'A', 22:'C', 23:'B', 24:'A', 25:'C',
    26:'B', 27:'A', 28:'C', 29:'A', 30:'B',
    31:'A', 32:'C', 33:'B', 34:'A', 35:'C',
    36:'A', 37:'B', 38:'A', 39:'C', 40:'B'
}

def calculate_final_assessment_score(mcq_score: int, practical_marks: dict[int, int]):
    if type(mcq_score) is not int or not 0 <= mcq_score <= 40:
        raise ValueError('MCQ score must be an integer between 0 and 40')
    if set(practical_marks) != set(range(41, 51)):
        raise ValueError('Exactly 10 practical marks are required')
    if any(type(v) is not int or v not in (0, 1) for v in practical_marks.values()):
        raise ValueError('Each question receives 0 or 1 mark')
    practical = sum(practical_marks.values())
    return {'mcq_score': mcq_score, 'practical_score': practical,
            'total_score': mcq_score + practical, 'maximum_score': 50,
            'percentage': round((mcq_score + practical) / 50 * 100, 2)}
