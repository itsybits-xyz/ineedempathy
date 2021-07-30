from ..backend.crud import crud
from ..backend.schemas import CardCreate

crud.add_card(
    CardCreate(
        display_name='Compersion',
        name='Compersion',
        type='feeling',
        level=1,
        definition='an empathetic state of happiness and joy experienced when another individual (often a partner) experiences happiness and joy.'
    )
)
