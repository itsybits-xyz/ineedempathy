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


def add_feeling(display_name, name, level, definition):
    return add_card(display_name, name, 'feeling', level, definition)


def add_need(display_name, name, level, definition):
    return add_card(display_name, name, 'need', level, definition)


# Feeling Data
add_feeling('Angry', 'angry', 1, 'meow')
add_feeling('Happy', 'happy', 1, 'meow')
add_feeling('Sad', 'sad', 1, 'meow')
add_feeling('Scared', 'scared', 1, 'meow')

add_feeling('Confused', 'confused', 2, 'meow')
add_feeling('Embarrassed', 'embarrassed', 2, 'meow')
add_feeling('Jealous', 'jealous', 2, 'meow')
add_feeling('Lonely', 'lonely', 2, 'meow')
add_feeling('Tired', 'tired', 2, 'meow')

add_feeling('Affectionate', 'affectionate', 3, 'meow')
add_feeling('Anxious', 'anxious', 3, 'meow')
add_feeling('Empowered', 'empowered', 3, 'meow')
add_feeling('Encouraged', 'encouraged', 3, 'meow')
add_feeling('Excited', 'excited', 3, 'meow')
add_feeling('Frustrated', 'frustrated', 3, 'meow')
add_feeling('Hurt', 'hurt', 3, 'meow')
add_feeling('Hopeless', 'hopeless', 3, 'meow')
add_feeling('Irritable', 'irritable', 3, 'meow')
add_feeling('Overwhelmed', 'overwhelmed', 3, 'meow')
add_feeling('Puzzled', 'puzzled', 3, 'meow')

add_feeling('Annoyed', 'annoyed', 4, 'meow')
add_feeling('Centered', 'centered', 4, 'meow')
add_feeling('Depressed', 'depressed', 4, 'meow')
add_feeling('Disappointed', 'disappointed', 4, 'meow')
add_feeling('Discouraged', 'discouraged', 4, 'meow')
add_feeling('Engaged', 'engaged', 4, 'meow')
add_feeling('Fidgety', 'fidgety', 4, 'meow')
add_feeling('Fulfilled', 'fulfilled', 4, 'meow')
add_feeling('Grateful', 'grateful', 4, 'meow')
add_feeling('Impatient', 'impatient', 4, 'meow')
add_feeling('Insecure', 'insecure', 4, 'meow')
add_feeling('Inspired', 'inspired', 4, 'meow')
add_feeling('Joyful', 'joyful', 4, 'meow')
add_feeling('Peaceful', 'peaceful', 4, 'meow')
add_feeling('Secure', 'secure', 4, 'meow')
add_feeling('Startled', 'startled', 4, 'meow')
add_feeling('Uncomfortable', 'uncomfortable', 4, 'meow')
add_feeling('Upset', 'upset', 4, 'meow')
add_feeling('Vulnerable', 'vulnerable', 4, 'meow')
add_feeling('Hopeful', 'hopeful', 4, 'meow')

# Need Data
add_need('Connection', 'connection', 1, 'meow')
add_need('Harmony', 'harmony', 1, 'meow')
add_need('Reassurance', 'reassurance', 1, 'meow')
add_need('Support', 'support', 1, 'meow')

add_need('Appreciation', 'appreciation', 2, 'meow')
add_need('Autonomy', 'autonomy', 2, 'meow')
add_need('Celebration', 'celebration', 2, 'meow')
add_need('Honesty', 'honesty', 2, 'meow')
add_need('Privacy/Space', 'privacy_space', 2, 'meow')

add_need('Advice', 'advice', 3, 'meow')
add_need('Affection', 'affection', 3, 'meow')
add_need('Care', 'care', 3, 'meow')
add_need('Community', 'community', 3, 'meow')
add_need('Cooperation', 'cooperation', 3, 'meow')
add_need('Hope', 'hope', 3, 'meow')
add_need('Mourning', 'mourning', 3, 'meow')
add_need('Play', 'play', 3, 'meow')
add_need('Safety', 'safety', 3, 'meow')
add_need('Self Expression', 'selfexpression', 3, 'meow')
add_need('Understanding', 'understanding', 3, 'meow')

add_need('Acceptance', 'acceptance', 4, 'meow')
add_need('Beauty', 'beauty', 4, 'meow')
add_need('Belonging', 'belonging', 4, 'meow')
add_need('Challenge', 'challenge', 4, 'meow')
add_need('Compassion', 'compassion', 4, 'meow')
add_need('Competence', 'competence', 4, 'meow')
add_need('Consideration', 'consideration', 4, 'meow')
add_need('Contribution', 'contribution', 4, 'meow')
add_need('Creativity', 'creativity', 4, 'meow')
add_need('Ease', 'ease', 4, 'meow')
add_need('Empathy', 'empathy', 4, 'meow')
add_need('Exercise', 'exercise', 4, 'meow')
add_need('Freedom', 'freedom', 4, 'meow')
add_need('Learning', 'learning', 4, 'meow')
add_need('Order', 'order', 4, 'meow')
add_need('Peace', 'peace', 4, 'meow')
add_need('Respect', 'respect', 4, 'meow')
add_need('Rest/Sleep', 'rest_sleep', 4, 'meow')
add_need('To Know and Be Known', 'toknowandbeknown', 4, 'meow')
add_need('To See and Be Seen', 'toseeandbeseen', 4, 'meow')
add_need('Trust', 'trust', 4, 'meow')

print('Card Count: ')
print(len(crud.get_cards(db)))
