Empathy Room Interactions

JOINS:

* User (Baylee) creates a room. (CREATE_ROOM)
* Baylee joins the room (entering their name) (JOIN_ROOM)
* Baylee joins the room, nobody is speaker, becomes speaker (JOIN_ROOM)
* Amjith joins the room, speaker is already set, becomes listener (JOIN_ROOM)
* Princess joins the room, speaker is already set, becomes listener (JOIN_ROOM)
* Sempi joins the room, speaker is already set, becomes listener (JOIN_ROOM)
* Speakers list is shown at the bottom
* Listeners list are shown next to their name

STARTS:

* Anybody can add cards to their list (UPSERT LIST)
* Speaker can also pull cards from listener lists
* Speaker can change the speaker (CHANGE_SPEAKER)
    * Changing speakers manually resets the lists

HOOK Listener:

* Listener Sempi adds card to their list (UPSERT LIST)
* Listener Sempi leaves the room via disconnection (LEAVE_ROOM)
    * Sempi goes "offline" and their card list stays

HOOK Empty List Listener:

* Listener Sempi leaves the room via disconnection (LEAVE_ROOM)
    * Sempi disappears from the room
* Sempi joins the room, speaker is already set, becomes listener (JOIN_ROOM)


HOOK Speaker:

* Speaker Amjith adds card to their list (UPSERT)
* Speaker Amjith leaves the room via disconnection (LEAVE_ROOM)
    * New speaker IS chosen
    * Card lists are NOT reset
        * Allows people to get back into the previous state if desired
