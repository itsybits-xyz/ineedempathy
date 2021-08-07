from backend import crud
from backend.schemas import CardCreate
from backend.deps import get_db

db = next(get_db())


def add_card(display_name, name, type, level, definition, definition_source):
    return crud.create_card(
        db=db,
        card=CardCreate(
            display_name=display_name,
            name=name,
            type=type,
            level=level,
            definition=definition,
            definition_source=definition_source
        )
    )


# TODO - once we have all definitions, let's remove default value for
# definition_source
def add_feeling(display_name, name, level, definition, definition_source='about:blank'):
    return add_card(display_name, name, 'feeling', level, definition, definition_source)


# TODO - once we have all definitions, let's remove default value for
# definition_source
def add_need(display_name, name, level, definition, definition_source='about:blank'):
    return add_card(display_name, name, 'need', level, definition, definition_source)


# Sqlite version of `truncate table cards`
db.execute('DELETE FROM cards')

# Feeling level 1
add_feeling(
    'Angry',
    'angry',
    1,
    'Feeling or showing strong annoyance, displeasure, or hostility; full of anger.',
    'https://www.lexico.com/en/definition/angry',
)
add_feeling(
    'Happy',
    'happy',
    1,
    'Having a sense of confidence in or satisfaction with (a person, arrangement, or situation)',
    'https://www.lexico.com/en/definition/happy',
)
add_feeling(
    'Sad',
    'sad',
    1,
    'Feeling or showing sorrow; unhappy.',
    'https://www.lexico.com/en/definition/sad',
)
add_feeling(
    'Scared',
    'scared',
    1,
    'Fearful; frightened.',
    'https://www.lexico.com/en/definition/scared',
)

# Feelings level 2
add_feeling(
    'Confused',
    'confused',
    2,
    'unable to think clearly; bewildered.',
    'https://www.lexico.com/en/definition/confused',
)
add_feeling(
    'Embarrassed',
    'embarrassed',
    2,
    'Feeling or showing embarrassment.',
    'https://www.lexico.com/en/definition/embarrassed',
)
add_feeling(
    'Jealous',
    'jealous',
    2,
    'Feeling or showing envy of someone or their achievements and advantages.',
    'https://www.lexico.com/en/definition/jealous',
)
add_feeling(
    'Lonely',
    'lonely',
    2,
    'affected with, characterized by, or causing a depressing feeling of being alone; lonesome.',
    'https://www.dictionary.com/browse/affected',
)
add_feeling(
    'Tired',
    'tired',
    2,
    'drained of strength and energy : fatigued often to the point of exhaustion',
    'https://www.merriam-webster.com/dictionary/tired',
)

# Feelings level 3
add_feeling(
    'Affectionate',
    'affectionate',
    3,
    'meow',
)
add_feeling(
    'Anxious',
    'anxious',
    3,
    'meow',
)
add_feeling(
    'Empowered',
    'empowered',
    3,
    'meow',
)
add_feeling(
    'Encouraged',
    'encouraged',
    3,
    'meow',
)
add_feeling(
    'Excited',
    'excited',
    3,
    'meow',
)
add_feeling(
    'Frustrated',
    'frustrated',
    3,
    'meow',
)
add_feeling(
    'Hurt',
    'hurt',
    3,
    'meow',
)
add_feeling(
    'Hopeless',
    'hopeless',
    3,
    'meow',
)
add_feeling(
    'Irritable',
    'irritable',
    3,
    'meow',
)
add_feeling(
    'Overwhelmed',
    'overwhelmed',
    3,
    'meow',
)
add_feeling(
    'Puzzled',
    'puzzled',
    3,
    'meow',
)

# Feelings level 4
add_feeling(
    'Annoyed',
    'annoyed',
    4,
    'meow',
)
add_feeling(
    'Centered',
    'centered',
    4,
    'meow',
)
add_feeling(
    'Depressed',
    'depressed',
    4,
    'meow',
)
add_feeling(
    'Disappointed',
    'disappointed',
    4,
    'meow',
)
add_feeling(
    'Discouraged',
    'discouraged',
    4,
    'meow',
)
add_feeling(
    'Engaged',
    'engaged',
    4,
    'meow',
)
add_feeling(
    'Fidgety',
    'fidgety',
    4,
    'meow',
)
add_feeling(
    'Fulfilled',
    'fulfilled',
    4,
    'meow',
)
add_feeling(
    'Grateful',
    'grateful',
    4,
    'meow',
)
add_feeling(
    'Impatient',
    'impatient',
    4,
    'meow',
)
add_feeling(
    'Insecure',
    'insecure',
    4,
    'meow',
)
add_feeling(
    'Inspired',
    'inspired',
    4,
    'meow',
)
add_feeling(
    'Joyful',
    'joyful',
    4,
    'meow',
)
add_feeling(
    'Peaceful',
    'peaceful',
    4,
    'meow',
)
add_feeling(
    'Secure',
    'secure',
    4,
    'meow',
)
add_feeling(
    'Startled',
    'startled',
    4,
    'meow',
)
add_feeling(
    'Uncomfortable',
    'uncomfortable',
    4,
    'meow',
)
add_feeling(
    'Upset',
    'upset',
    4,
    'meow',
)
add_feeling(
    'Vulnerable',
    'vulnerable',
    4,
    'meow',
)
add_feeling(
    'Hopeful',
    'hopeful',
    4,
    'meow',
)

# Needs Level 1
add_need(
    'Connection',
    'connection',
    1,
    'A feeling of understanding and ease of communication between two or more people.',
    'https://en.wiktionary.org/wiki/connection',
)
add_need(
    'Harmony',
    'harmony',
    1,
    'a consistent, orderly, or pleasing arrangement of parts; congruity.',
    'https://www.dictionary.com/browse/harmony',
)
add_need(
    'Reassurance',
    'reassurance',
    1,
    'The action of removing someone\'s doubts or fears.',
    'https://www.lexico.com/en/definition/reassurance',
)
add_need(
    'Support',
    'support',
    1,
    'To verify; to make good; to substantiate; to establish; to sustain.',
    'https://en.wiktionary.org/wiki/support',
)

# Needs level 2
add_need(
    'Appreciation',
    'appreciation',
    2,
    'Recognition and enjoyment of the good qualities of someone or something.',
    'https://www.lexico.com/en/definition/appreciation',
)
add_need(
    'Autonomy',
    'autonomy',
    2,
    'The capacity to make an informed, uncoerced decision.',
    'https://en.wiktionary.org/wiki/autonomy',
)
add_need(
    'Celebration',
    'celebration',
    2,
    'The act, process of showing appreciation, gratitude and/or remembrance, notably as a social event.',
    'https://en.wiktionary.org/wiki/celebration',
)
add_need(
    'Honesty',
    'honesty',
    2,
    'fairness and straightforwardness of conduct',
    'https://www.merriam-webster.com/dictionary/honesty',
)
add_need(
    'Privacy/Space',
    'privacy_space',
    2,
    'the quality or state of being apart from company or observation',
    'https://www.merriam-webster.com/dictionary/privacy',
)

# Needs level 3
add_need(
    'Advice',
    'advice',
    3,
    'meow',
)
add_need(
    'Affection',
    'affection',
    3,
    'meow',
)
add_need(
    'Care',
    'care',
    3,
    'meow',
)
add_need(
    'Community',
    'community',
    3,
    'meow',
)
add_need(
    'Cooperation',
    'cooperation',
    3,
    'meow',
)
add_need(
    'Hope',
    'hope',
    3,
    'meow',
)
add_need(
    'Mourning',
    'mourning',
    3,
    'meow',
)
add_need(
    'Play',
    'play',
    3,
    'meow',
)
add_need(
    'Safety',
    'safety',
    3,
    'meow',
)
add_need(
    'Self Expression',
    'selfexpression',
    3,
    'meow',
)
add_need(
    'Understanding',
    'understanding',
    3,
    'meow',
)

# Needs level 4
add_need(
    'Acceptance',
    'acceptance',
    4,
    'The action or process of being received as adequate or suitable, typically to be admitted into a group.',
    'https://www.lexico.com/en/definition/The',
)
add_need(
    'Beauty',
    'beauty',
    4,
    'A combination of qualities, such as shape, color, or form, that pleases the aesthetic senses, especially the sight.',
    'https://www.lexico.com/en/definition/beauty',
)
add_need(
    'Belonging',
    'belonging',
    4,
    'An affinity for a place or situation.',
    'https://www.lexico.com/en/definition/belonging',
)
add_need(
    'Challenge',
    'challenge',
    4,
    'A difficult task, especially one that the person making the attempt finds more enjoyable because of that difficulty.',
    'https://en.wiktionary.org/wiki/challenge',
)
add_need(
    'Compassion',
    'compassion',
    4,
    'Deep awareness of the suffering of another, coupled with the wish to relieve it. ',
    'https://en.wiktionary.org/wiki/compassion',
)
add_need(
    'Competence',
    'competence',
    4,
    'The ability to do something successfully or efficiently.',
    'https://www.lexico.com/en/definition/Competence',
)
add_need(
    'Consideration',
    'consideration',
    4,
    'A fact or a motive taken into account in deciding or judging something.',
    'https://www.lexico.com/en/definition/consideration',
)
add_need(
    'Contribution',
    'contribution',
    4,
    'Something given or offered that adds to a larger whole.',
    'https://en.wiktionary.org/wiki/contribution',
)
add_need(
    'Creativity',
    'creativity',
    4,
    'The ability to use imagination to produce a novel idea or product.',
    'https://en.wiktionary.org/wiki/creativity',
)
add_need(
    'Ease',
    'ease',
    4,
    'Absence of difficulty or effort.',
    'https://www.lexico.com/en/definition/Absence',
)
add_need(
    'Empathy',
    'empathy',
    4,
    'The ability to understand and share the feelings (and needs) of another.',
    'https://www.lexico.com/en/definition/empathy',
)
add_need(
    'Exercise',
    'exercise',
    4,
    'A process or activity carried out for a specific purpose, especially one concerned with a specified area or skill.',
    'https://www.lexico.com/en/definition/exercise',
)
add_need(
    'Freedom',
    'freedom',
    4,
    'The power or right to act, speak, or think as one wants without hindrance or restraint.',
    'https://www.lexico.com/en/definition/freedom',
)
add_need(
    'Learning',
    'learning',
    4,
    'The acquisition of knowledge or skills through experience, study, or by being taught.',
    'https://www.lexico.com/en/definition/learning',
)
add_need(
    'Order',
    'order',
    4,
    'The arrangement or disposition of people or things in relation to each other according to a particular sequence, pattern, or method.',
    'https://www.lexico.com/en/definition/order',
)
add_need(
    'Peace',
    'peace',
    4,
    'Freedom from disturbance; tranquility.',
    'https://www.lexico.com/en/definition/Freedom',
)
add_need(
    'Respect',
    'respect',
    4,
    'Due regard for the feelings, wishes, rights, or traditions of others.',
    'https://www.lexico.com/en/definition/respect',
)
add_need(
    'Rest or Sleep',
    'rest_sleep',
    4,
    'freedom from activity or labor',
    'https://www.merriam-webster.com/dictionary/rest',
)
add_need(
    'To Know and Be Known',
    'toknowandbeknown',
    4,
    'To Know and Be Known',
    '',
)
add_need(
    'To See and Be Seen',
    'toseeandbeseen',
    4,
    'To See and Be Seen',
    '',
)
add_need(
    'Trust',
    'trust',
    4,
    'confident expectation of something',
    'https://www.dictionary.com/browse/something',
)

print('Card Count: ')
print(len(crud.get_cards(db)))
