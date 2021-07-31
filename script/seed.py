from backend import crud
from backend.schemas import CardCreate
from backend.deps import get_db

db = next(get_db())


def add_card(display_name, name, type, level, definition):
    return crud.create_card(
        db=db,
        card=CardCreate(
            display_name=display_name,
            name=name,
            type=type,
            level=level,
            definition=definition
        )
    )


def add_feeling(display_name, name):
    return add_card(display_name, name, 'feeling', 1, 'meow')


def add_need(display_name, name):
    return add_card(display_name, name, 'need', 1, 'ruff')


# Seed Data
add_feeling('Affectionate', 'affectionate')
add_feeling('Angry', 'angry')
add_feeling('Annoyed', 'annoyed')
add_feeling('Anxious', 'anxious')
add_feeling('Centered', 'centered')
add_feeling('Confused', 'confused')
add_feeling('Depressed', 'depressed')
add_feeling('Disappointed', 'disappointed')
add_feeling('Discouraged', 'discouraged')
add_feeling('Embarrassed', 'embarrassed')
add_feeling('Empowered', 'empowered')
add_feeling('Encouraged', 'encouraged')
add_feeling('Engaged', 'engaged')
add_feeling('Excited', 'excited')
add_feeling('Fidgety', 'fidgety')
add_feeling('Frustrated', 'frustrated')
add_feeling('Fulfilled', 'fulfilled')
add_feeling('Grateful', 'grateful')
add_feeling('Happy', 'happy')
add_feeling('Hopeful', 'hopeful')
add_feeling('Hopeless', 'hopeless')
add_feeling('Hurt', 'hurt')
add_feeling('Impatient', 'impatient')
add_feeling('Insecure', 'insecure')
add_feeling('Inspired', 'inspired')
add_feeling('Irritable', 'irritable')
add_feeling('Jealous', 'jealous')
add_feeling('Joyful', 'joyful')
add_feeling('Lonely', 'lonely')
add_feeling('Overwhelmed', 'overwhelmed')
add_feeling('Peaceful', 'peaceful')
add_feeling('Puzzled', 'puzzled')
add_feeling('Sad', 'sad')
add_feeling('Scared', 'scared')
add_feeling('Secure', 'secure')
add_feeling('Startled', 'startled')
add_feeling('Tired', 'tired')
add_feeling('Uncomfortable', 'uncomfortable')
add_feeling('Upset', 'upset')
add_feeling('Vulnerable', 'vulnerable')


add_need('Acceptance', 'acceptance')
add_need('Advice', 'advice')
add_need('Affection', 'affection')
add_need('Appreciation', 'appreciation')
add_need('Autonomy', 'autonomy')
add_need('Beauty', 'beauty')
add_need('Belonging', 'belonging')
add_need('Care', 'care')
add_need('Celebration', 'celebration')
add_need('Challenge', 'challenge')
add_need('Community', 'community')
add_need('Compassion', 'compassion')
add_need('Competence', 'competence')
add_need('Connection', 'connection')
add_need('Consideration', 'consideration')
add_need('Contribution', 'contribution')
add_need('Cooperation', 'cooperation')
add_need('Creativity', 'creativity')
add_need('Ease', 'ease')
add_need('Empathy', 'empathy')
add_need('Exercise', 'exercise')
add_need('Freedom', 'freedom')
add_need('Harmony', 'harmony')
add_need('Honesty', 'honesty')
add_need('Hope', 'hope')
add_need('Learning', 'learning')
add_need('Mourning', 'mourning')
add_need('Order', 'order')
add_need('Peace', 'peace')
add_need('Play', 'play')
add_need('Privacy_space', 'privacy_space')
add_need('Reassurance', 'reassurance')
add_need('Respect', 'respect')
add_need('Rest_sleep', 'rest_sleep')
add_need('Safety', 'safety')
add_need('Selfexpression', 'selfexpression')
add_need('Support', 'support')
add_need('Toknowandbeknown', 'toknowandbeknown')
add_need('Toseeandbeseen', 'toseeandbeseen')
add_need('Trust', 'trust')
add_need('Understanding', 'understanding')

print('Card Count: ')
print(len(crud.get_cards(db)))
