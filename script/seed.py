from typing import List
from backend import crud
from backend.schemas import CardCreate
from backend.deps import get_db
from backend.models import Story, Scene, Guess

db = next(get_db())


def upsert_story(display_name: str, scenes: List[Scene]) -> Story:
    story = crud.upsert_story(
        db=db,
        display_name=display_name,
        scenes=scenes
    )

    i = 0
    for scene in scenes:
        i += 1
        db_scene = crud.upsert_scene(
            db=db,
            story_id=story.id,
            noun=scene.get('noun'),
            position=i,
            description=scene.get('description')
        )

        crud.upsert_guess(
            db=db,
            story_id=story.id,
            scene_id=db_scene.id,
            card_id=scene.get('feeling_id')
        )
        crud.upsert_guess(
            db=db,
            story_id=story.id,
            scene_id=db_scene.id,
            card_id=scene.get('need_id')
        )
    return story

def upsert_card(display_name, name, type, level, definition, definition_source):
    return crud.upsert_card(
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


def add_feeling(display_name, name, level, definition, definition_source):
    return upsert_card(display_name, name, 'feeling', level, definition, definition_source)


def add_need(display_name, name, level, definition, definition_source):
    return upsert_card(display_name, name, 'need', level, definition, definition_source)


# Feeling level 1
angry = add_feeling(
    'Angry',
    'angry',
    1,
    'Feeling or showing strong annoyance, displeasure, or hostility; full of anger.',
    'https://www.lexico.com/en/definition/angry',
)
happy = add_feeling(
    'Happy',
    'happy',
    1,
    'Having a sense of confidence in or satisfaction with (a person, arrangement, or situation)',
    'https://www.lexico.com/en/definition/happy',
)
sad = add_feeling(
    'Sad',
    'sad',
    1,
    'Feeling or showing sorrow; unhappy.',
    'https://www.lexico.com/en/definition/sad',
)
scared = add_feeling(
    'Scared',
    'scared',
    1,
    'Fearful; frightened.',
    'https://www.lexico.com/en/definition/scared',
)

# Feelings level 2
# cold, compersion
cold = add_feeling(
    'Cold',
    'cold',
    4,
    'Lacking affection or warmth of feeling; unemotional.',
    'https://www.lexico.com/en/definition/cold',
)
compersion = add_feeling(
    'Compersion',
    'compersion',
    4,
    'Compersion is an empathetic state of happiness and joy experienced when another individual experiences happiness and joy.',
    'https://www.definitions.net/definition/compersion',
)
confused = add_feeling(
    'Confused',
    'confused',
    2,
    'unable to think clearly; bewildered.',
    'https://www.lexico.com/en/definition/confused',
)
embarrassed = add_feeling(
    'Embarrassed',
    'embarrassed',
    2,
    'Feeling or showing embarrassment.',
    'https://www.lexico.com/en/definition/embarrassed',
)
jealous = add_feeling(
    'Jealous',
    'jealous',
    2,
    'Feeling or showing envy of someone or their achievements and advantages.',
    'https://www.lexico.com/en/definition/jealous',
)
lonely = add_feeling(
    'Lonely',
    'lonely',
    2,
    'affected with, characterized by, or causing a depressing feeling of being alone; lonesome.',
    'https://www.dictionary.com/browse/affected',
)
tired = add_feeling(
    'Tired',
    'tired',
    2,
    'drained of strength and energy : fatigued often to the point of exhaustion',
    'https://www.merriam-webster.com/dictionary/tired',
)

# Feelings level 3
affectionate = add_feeling(
    'Affectionate',
    'affectionate',
    3,
    'Readily feeling or showing fondness or tenderness.',
    'https://www.lexico.com/en/definition/affectionate',
)
anxious = add_feeling(
    'Anxious',
    'anxious',
    3,
    'Experiencing worry, unease, or nervousness, typically about an imminent event or something with an uncertain outcome.',
    'https://www.lexico.com/en/definition/anxious',
)
empowered = add_feeling(
    'Empowered',
    'empowered',
    3,
    'Having been given the power to make choices relevant to one\'s situation',
    'https://en.wiktionary.org/wiki/empowered',
)
encouraged = add_feeling(
    'Encouraged',
    'encouraged',
    3,
    'to stimulate by assistance, approval, etc.',
    'https://www.dictionary.com/browse/encouraged',
)
excited = add_feeling(
    'Excited',
    'excited',
    3,
    'Very enthusiastic and eager.',
    'https://www.lexico.com/en/definition/excited',
)
frustrated = add_feeling(
    'Frustrated',
    'frustrated',
    3,
    'Prevented from progressing, succeeding, or being fulfilled.',
    'https://www.lexico.com/en/definition/frustrated',
)
hurt = add_feeling(
    'Hurt',
    'hurt',
    3,
    'to feel or suffer bodily or mental pain or distress:',
    'https://www.dictionary.com/browse/hurt',
)
hopeless = add_feeling(
    'Hopeless',
    'hopeless',
    3,
    'having no expectation of good or success',
    'https://www.merriam-webster.com/dictionary/hopeless',
)
irritable = add_feeling(
    'Irritable',
    'irritable',
    3,
    'Easily exasperated or excited.',
    'https://en.wiktionary.org/wiki/irritable',
)
overwhelmed = add_feeling(
    'Overwhelmed',
    'overwhelmed',
    3,
    'completely overcome in mind or feeling',
    'https://www.dictionary.com/browse/overwhelmed',
)
puzzled = add_feeling(
    'Puzzled',
    'puzzled',
    3,
    'Unable to understand; perplexed.',
    'https://www.lexico.com/en/definition/puzzled',
)

# Feelings level 4
annoyed = add_feeling(
    'Annoyed',
    'annoyed',
    4,
    'feeling or showing angry irritation',
    'https://www.merriam-webster.com/dictionary/annoyed',
)
centered = add_feeling(
    'Centered',
    'centered',
    4,
    'emotionally stable and secure',
    'https://www.merriam-webster.com/dictionary/centered',
)
depressed = add_feeling(
    'Depressed',
    'depressed',
    4,
    'low in spirits',
    'https://www.merriam-webster.com/dictionary/depressed',
)
disappointed = add_feeling(
    'Disappointed',
    'disappointed',
    4,
    'depressed or discouraged by the failure of one\'s hopes or expectations',
    'https://www.dictionary.com/browse/disappointed',
)
discouraged = add_feeling(
    'Discouraged',
    'discouraged',
    4,
    'Having lost confidence or enthusiasm; disheartened.',
    'https://www.lexico.com/en/definition/discouraged',
)
engaged = add_feeling(
    'Engaged',
    'engaged',
    4,
    'involved in an activity',
    'https://www.merriam-webster.com/dictionary/engaged',
)
fidgety = add_feeling(
    'Fidgety',
    'fidgety',
    4,
    'Inclined to fidget; restless or uneasy.',
    'https://www.lexico.com/en/definition/fidgety',
)
fulfilled = add_feeling(
    'Fulfilled',
    'fulfilled',
    4,
    'Satisfied or happy because of fully developing one\'s abilities or character.',
    'https://www.lexico.com/en/definition/fulfilled',
)
grateful = add_feeling(
    'Grateful',
    'grateful',
    4,
    'warmly or deeply appreciative of kindness or benefits received; thankful:',
    'https://www.dictionary.com/browse/grateful',
)
impatient = add_feeling(
    'Impatient',
    'impatient',
    4,
    'restless in desire or expectation; eagerly desirous.',
    'https://www.dictionary.com/browse/impatient',
)
insecure = add_feeling(
    'Insecure',
    'insecure',
    4,
    'not confident or certain; uneasy; anxious:',
    'https://www.dictionary.com/browse/insecure',
)
inspired = add_feeling(
    'Inspired',
    'inspired',
    4,
    'aroused, animated, or imbued with the spirit to do something',
    'https://www.dictionary.com/browse/inspired',
)
joyful = add_feeling(
    'Joyful',
    'joyful',
    4,
    'Feeling, expressing, or causing great pleasure and happiness.',
    'https://www.lexico.com/en/definition/joyful',
)
peaceful = add_feeling(
    'Peaceful',
    'peaceful',
    4,
    'Free from disturbance; tranquil.',
    'https://www.lexico.com/en/definition/peaceful',
)
secure = add_feeling(
    'Secure',
    'secure',
    4,
    'Fixed or fastened so as not to give way, become loose, or be lost.',
    'https://www.lexico.com/en/definition/secure',
)
startled = add_feeling(
    'Startled',
    'startled',
    4,
    'Feeling or showing sudden shock or alarm.',
    'https://www.lexico.com/en/definition/startled',
)
uncomfortable = add_feeling(
    'Uncomfortable',
    'uncomfortable',
    4,
    'Causing or feeling slight pain or physical discomfort.',
    'https://www.lexico.com/en/definition/uncomfortable',
)
upset = add_feeling(
    'Upset',
    'upset',
    4,
    'Unhappy, disappointed, or worried.',
    'https://www.lexico.com/en/definition/upset',
)
vulnerable = add_feeling(
    'Vulnerable',
    'vulnerable',
    4,
    'More or most likely to be exposed to the chance of being attacked or harmed, either physically or emotionally. ',
    'https://en.wiktionary.org/wiki/vulnerable',
)
hopeful = add_feeling(
    'Hopeful',
    'hopeful',
    4,
    'promising advantage or success',
    'https://www.dictionary.com/browse/hopeful',
)

# Needs Level 1
connection = add_need(
    'Connection',
    'connection',
    1,
    'A feeling of understanding and ease of communication between two or more people.',
    'https://en.wiktionary.org/wiki/connection',
)
harmony = add_need(
    'Harmony',
    'harmony',
    1,
    'a consistent, orderly, or pleasing arrangement of parts; congruity.',
    'https://www.dictionary.com/browse/harmony',
)
reassurance = add_need(
    'Reassurance',
    'reassurance',
    1,
    'The action of removing someone\'s doubts or fears.',
    'https://www.lexico.com/en/definition/reassurance',
)
support = add_need(
    'Support',
    'support',
    1,
    'To verify; to make good; to substantiate; to establish; to sustain.',
    'https://en.wiktionary.org/wiki/support',
)

# Needs level 2
appreciation = add_need(
    'Appreciation',
    'appreciation',
    2,
    'Recognition and enjoyment of the good qualities of someone or something.',
    'https://www.lexico.com/en/definition/appreciation',
)
autonomy = add_need(
    'Autonomy',
    'autonomy',
    2,
    'The capacity to make an informed, uncoerced decision.',
    'https://en.wiktionary.org/wiki/autonomy',
)
celebration = add_need(
    'Celebration',
    'celebration',
    2,
    'The act, process of showing appreciation, gratitude and/or remembrance, notably as a social event.',
    'https://en.wiktionary.org/wiki/celebration',
)
honesty = add_need(
    'Honesty',
    'honesty',
    2,
    'fairness and straightforwardness of conduct',
    'https://www.merriam-webster.com/dictionary/honesty',
)
space = privacy = add_need(
    'Privacy/Space',
    'privacy_space',
    2,
    'the quality or state of being apart from company or observation',
    'https://www.merriam-webster.com/dictionary/privacy',
)

# Needs level 3
advice = add_need(
    'Advice',
    'advice',
    3,
    'an opinion or recommendation offered as a guide to action, conduct, etc.',
    'https://www.dictionary.com/browse/advice',
)
affection = add_need(
    'Affection',
    'affection',
    3,
    'a feeling of liking and caring for someone or something',
    'https://www.merriam-webster.com/dictionary/affection',
)
care = add_need(
    'Care',
    'care',
    3,
    'The provision of what is necessary for the health, welfare, maintenance, and protection of someone or something.',
    'https://www.lexico.com/en/definition/care',
)
community = add_need(
    'Community',
    'community',
    3,
    'A feeling of fellowship with others, as a result of sharing common attitudes, interests, and goals.',
    'https://www.lexico.com/en/definition/community',
)
cooperation = add_need(
    'Cooperation',
    'cooperation',
    3,
    'The process of working together to the same end.',
    'https://www.lexico.com/en/definition/cooperation',
)
hope = add_need(
    'Hope',
    'hope',
    3,
    'expectation and desire for a certain thing to happen.',
    'https://www.lexico.com/en/definition/hope',
)
mourning = add_need(
    'Mourning',
    'mourning',
    3,
    'to feel or express sorrow or grief.',
    'https://www.dictionary.com/browse/mourn',
)
play = add_need(
    'Play',
    'play',
    3,
    'Engage in activity for enjoyment and recreation rather than a serious or practical purpose.',
    'https://www.lexico.com/en/definition/play',
)
safety = add_need(
    'Safety',
    'safety',
    3,
    'The condition of being protected from or unlikely to cause danger, risk, or injury.',
    'https://www.lexico.com/en/definition/safety',
)
self_expression = add_need(
    'Self Expression',
    'selfexpression',
    3,
    'The expression of one\'s feelings, thoughts, or ideas, especially in writing, art, music, or dance.',
    'https://www.lexico.com/en/definition/self-expression',
)
understanding = add_need(
    'Understanding',
    'understanding',
    3,
    'Sympathetically aware of other people\'s feelings; tolerant and forgiving.',
    'https://www.lexico.com/en/definition/understanding',
)

# Needs level 4
acceptance = add_need(
    'Acceptance',
    'acceptance',
    4,
    'The action or process of being received as adequate or suitable, typically to be admitted into a group.',
    'https://www.lexico.com/en/definition/acceptance',
)
beauty = add_need(
    'Beauty',
    'beauty',
    4,
    'A combination of qualities, such as shape, color, or form, that pleases the aesthetic senses, especially the sight.',
    'https://www.lexico.com/en/definition/beauty',
)
belonging = add_need(
    'Belonging',
    'belonging',
    4,
    'An affinity for a place or situation.',
    'https://www.lexico.com/en/definition/belonging',
)
challenge = add_need(
    'Challenge',
    'challenge',
    4,
    'A difficult task, especially one that the person making the attempt finds more enjoyable because of that difficulty.',
    'https://en.wiktionary.org/wiki/challenge',
)
compassion = add_need(
    'Compassion',
    'compassion',
    4,
    'Deep awareness of the suffering of another, coupled with the wish to relieve it. ',
    'https://en.wiktionary.org/wiki/compassion',
)
competence = add_need(
    'Competence',
    'competence',
    4,
    'The ability to do something successfully or efficiently.',
    'https://www.lexico.com/en/definition/Competence',
)
consideration = add_need(
    'Consideration',
    'consideration',
    4,
    'A fact or a motive taken into account in deciding or judging something.',
    'https://www.lexico.com/en/definition/consideration',
)
contribution = add_need(
    'Contribution',
    'contribution',
    4,
    'Something given or offered that adds to a larger whole.',
    'https://en.wiktionary.org/wiki/contribution',
)
creativity = add_need(
    'Creativity',
    'creativity',
    4,
    'The ability to use imagination to produce a novel idea or product.',
    'https://en.wiktionary.org/wiki/creativity',
)
ease = add_need(
    'Ease',
    'ease',
    4,
    'Absence of difficulty or effort.',
    'https://www.lexico.com/en/definition/Absence',
)
empathy = add_need(
    'Empathy',
    'empathy',
    4,
    'The ability to understand and share the feelings (and needs) of another.',
    'https://www.lexico.com/en/definition/empathy',
)
exercise = add_need(
    'Exercise',
    'exercise',
    4,
    'A process or activity carried out for a specific purpose, especially one concerned with a specified area or skill.',
    'https://www.lexico.com/en/definition/exercise',
)
freedom = add_need(
    'Freedom',
    'freedom',
    4,
    'The power or right to act, speak, or think as one wants without hindrance or restraint.',
    'https://www.lexico.com/en/definition/freedom',
)
learning = add_need(
    'Learning',
    'learning',
    4,
    'The acquisition of knowledge or skills through experience, study, or by being taught.',
    'https://www.lexico.com/en/definition/learning',
)
mutuality = add_need(
    'Mutuality',
    'mutuality',
    4,
    'The sharing of a feeling, action, or relationship between two or more parties.',
    'https://www.lexico.com/en/definition/mutuality',
)
order = add_need(
    'Order',
    'order',
    4,
    'The arrangement or disposition of people or things in relation to each other according to a particular sequence, pattern, or method.',
    'https://www.lexico.com/en/definition/order',
)
peace = add_need(
    'Peace',
    'peace',
    4,
    'Freedom from disturbance; tranquility.',
    'https://www.lexico.com/en/definition/Freedom',
)
respect = add_need(
    'Respect',
    'respect',
    4,
    'Due regard for the feelings, wishes, rights, or traditions of others.',
    'https://www.lexico.com/en/definition/respect',
)
rest = sleep = add_need(
    'Rest or Sleep',
    'rest_sleep',
    4,
    'freedom from activity or labor',
    'https://www.merriam-webster.com/dictionary/rest',
)
be_known = add_need(
    'To Know and Be Known',
    'toknowandbeknown',
    4,
    'To Know and Be Known',
    '',
)
be_seen = add_need(
    'To See and Be Seen',
    'toseeandbeseen',
    4,
    'To See and Be Seen',
    '',
)
trust = add_need(
    'Trust',
    'trust',
    4,
    'confident expectation of something',
    'https://www.lexico.com/en/definition/trust',
)

upsert_story(display_name="Nissa's Beach Adventure", scenes=[
    {
        'description': ' '.join([
            'Nissa wanted to go to the beach with a friend.',
        ]),
        'noun': 'Nissa',
        'feeling_id': hopeful.id,
        'need_id': connection.id
    },
    {
        'description': ' '.join([
            'Nissa asked Mora if they wanted to go. Mora said',
            '"I want to go, but I need to finish a big project at work".',
        ]),
        'noun': 'Mora',
        'feeling_id': hopeful.id,
        'need_id': connection.id
    },
    {
        'description': ' '.join([
            'Nissa sent a group text trying to see if anybody wanted',
            'to go to the beach with them.',
        ]),
        'noun': 'Nissa',
        'feeling_id': inspired.id,
        'need_id': connection.id
    },
    {
        'description': ' '.join([
            'Hazel responded and asked if they could bring their cat.',
            'Her cat loved the beach.',
        ]),
        'noun': 'Hazel',
        'feeling_id': hopeful.id,
        'need_id': reassurance.id
    },
    {
        'description': ' '.join([
            'Nissa, Hazel and the cat all enjoyed a peaceful',
            'sunset at the beach.',
        ]),
        'noun': 'Nissa, Hazel and the cat',
        'feeling_id': peaceful.id,
        'need_id': beauty.id
    }
])

upsert_story(display_name="Isabella's Scary Day", scenes=[
    {
        'description': ' '.join([
            'Isabella is flipping through her phone, and notices',
            'multiple stories about protests in her area.',
        ]),
        'noun': 'Isabella',
        'feeling_id': upset.id,
        'need_id': contribution.id
    },
    {
        'description': ' '.join([
            'Isabella is hesitant to join a protest because of how',
            'unruly they seem to get in the news, but really wants',
            'to join the cause.',
        ]),
        'noun': 'Isabella',
        'feeling_id': insecure.id,
        'need_id': contribution.id
    },
    {
        'description': ' '.join([
            'Mora messages Isabella and tells her about a rally',
            'at the Capitol happening later that day.',
        ]),
        'noun': 'Mora',
        'feeling_id': empowered.id,
        'need_id': support.id
    },
    {
        'description': ' '.join([
            'Isabella and Mora end up going together.',
        ]),
        'noun': 'Isabella and Mora',
        'feeling_id': hopeful.id,
        'need_id': encouraged.id
    }
])

upsert_story(display_name="Jewel's Busy Weekend", scenes=[
    {
        'description': ' '.join([
            'Jewel texted her partner Mora asking if Mora',
            'could teach her how to build a new desk.',
        ]),
        'noun': 'Jewel',
        'feeling_id': insecure.id,
        'need_id': support.id
    },
    {
        'description': ' '.join([
            'When Mora came home from work, they joined Jewel',
            'and the two of them got busy learning everything they',
            'needed to build a desk together.',
        ]),
        'noun': 'Mora',
        'feeling_id': inspired.id,
        'need_id': learning.id
    },
    {
        'description': ' '.join([
            'When they finished building the desk they ordered takeout',
            'and relaxed with their new furniture.',
        ]),
        'noun': 'Jewel and Mora',
        'feeling_id': fulfilled.id,
        'need_id': appreciation.id
    }
])

upsert_story(display_name='Hazel needs a hand', scenes=[
    {
        'description': ' '.join([
            'Hazel woke up to small chirping sounds coming from outside.',
            'She sprung out of bed and ran outside to investigate.',
        ]),
        'noun': 'Hazel',
        'feeling_id': startled.id,
        'need_id': understanding.id
    },
    {
        'description': ' '.join([
            'Hazel discovered the chicken eggs had recently hatched.',
            'Hazel quickly called Jewel to talk about the news.',
        ]),
        'noun': 'Hazel',
        'feeling_id': excited.id,
        'need_id': self_expression.id
    }
])


print('Count: ')
print('Cards', len(crud.get_cards(db)))
print('Story', len(db.query(Story).all()))
print('Scenes', len(db.query(Scene).all()))
print('Guess', len(db.query(Guess).all()))
