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


def add_feeling(name):
    return add_card(name, name, 'feeling', 1, 'meow')


def add_need(name):
    return add_card(name, name, 'need', 1, 'ruff')


# Seed Data
add_feeling('affectionate')
add_feeling('angry')
add_feeling('annoyed')
add_feeling('anxious')
add_feeling('centered')
add_feeling('confused')
add_feeling('depressed')
add_feeling('disappointed')
add_feeling('discouraged')
add_feeling('embarrassed')
add_feeling('empowered')
add_feeling('encouraged')
add_feeling('engaged')
add_feeling('excited')
add_feeling('fidgety')
add_feeling('frustrated')
add_feeling('fulfilled')
add_feeling('grateful')
add_feeling('happy')
add_feeling('hopeful')
add_feeling('hopeless')
add_feeling('hurt')
add_feeling('impatient')
add_feeling('insecure')
add_feeling('inspired')
add_feeling('irritable')
add_feeling('jealous')
add_feeling('joyful')
add_feeling('lonely')
add_feeling('overwhelmed')
add_feeling('peaceful')
add_feeling('puzzled')
add_feeling('sad')
add_feeling('scared')
add_feeling('secure')
add_feeling('startled')
add_feeling('tired')
add_feeling('uncomfortable')
add_feeling('upset')
add_feeling('vulnerable')


add_need('acceptance')
add_need('advice')
add_need('affection')
add_need('appreciation')
add_need('autonomy')
add_need('beauty')
add_need('belonging')
add_need('care')
add_need('celebration')
add_need('challenge')
add_need('community')
add_need('compassion')
add_need('competence')
add_need('connection')
add_need('consideration')
add_need('contribution')
add_need('cooperation')
add_need('creativity')
add_need('ease')
add_need('empathy')
add_need('exercise')
add_need('freedom')
add_need('harmony')
add_need('honesty')
add_need('hope')
add_need('learning')
add_need('mourning')
add_need('order')
add_need('peace')
add_need('play')
add_need('privacy_space')
add_need('reassurance')
add_need('respect')
add_need('rest_sleep')
add_need('safety')
add_need('selfexpression')
add_need('support')
add_need('toknowandbeknown')
add_need('toseeandbeseen')
add_need('trust')
add_need('understanding')

print('Card Count: ')
print(len(crud.get_cards(db)))
