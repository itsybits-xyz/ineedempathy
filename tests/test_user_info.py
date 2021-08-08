from backend.schemas import UserInfo


def test_toggle_card():
    user_token = 'meow.user'
    user = UserInfo(name=user_token)
    assert len(user.cards) == 0
    user.toggle_card(1)
    assert len(user.cards) == 1
    user.toggle_card(1)
    assert len(user.cards) == 0
    user.toggle_card(2)
    user.toggle_card(3)
    assert len(user.cards) == 2


def test_empty():
    user_token = 'meow.user'
    card_token = 1
    socket_token = 'socket_1'
    user = UserInfo(name=user_token)
    assert user.empty()
    user.toggle_card(card_token)
    assert user.empty()
    user.add_socket(socket_token)
    assert not user.empty()
    user.remove_socket(socket_token)
    assert user.empty()


def test_progress():
    user_1_token = 'meow.user.1'
    user_2_token = 'meow.user.2'
    user_1 = UserInfo(name=user_1_token)
    user_2 = UserInfo(name=user_2_token)
    assert user_1.progress(user_2) == {
        "name": user_1_token,
        "speaker": False,
        "cards": []
    }
    assert user_2.progress(user_2) == {
        "name": user_2_token,
        "speaker": True,
        "cards": []
    }
