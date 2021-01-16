Gameplay:

JOINS:

* User (Baylee) creates a room and joins in.
* Baylee is places in waiting room. 
* Baylee sends invite to others.
* Amjith joins the room, also placed in WAITING room.
* Princess joins the room, also placed in WAITING room.
* Sempi joins the room, also placed in WAITING room.

STARTS:

* Baylee starts the game.
* Everyone is moved to the game room.
* Every user is asked to write a story.
* Every user name gets a little asterisk next to it denoting we're waiting for that user to finish.
* Princess finishes their story and submits. 
* Princess is now in WAITING state. Asterisk is removed from Princess status.
* Baylee and Amjith submit their stories. They both go to WAITING state.
* Sempi goes inactive.
* Baylee initiates next step. 
* Amjith and Princess approve. 
* Everyone moves to guessing state except Sempi.
* Sempi is sent back to waiting room.
* Everyone in the game room is presented with Baylee's story (randomly chosen).
* Everyone submits their guesses except Baylee (no guessing on your own stories).
* When all guesses are presented, everyone gets a reveal button when presses, shows the results.
* Next Amjith's story is presented to everyone.
* Baylee guesses. 
* Princess left to get a treat before guessing.
* Amjith initiates next step. 
* Baylee approves. 
* Princess is moved to waiting room.
* Both Amjith and Baylee get a notification that Sempi wants to join the room. 
* Either one can admit Sempi to join.
* Amjith, Baylee and Sempi are presented with Princess' story.
* When all of them have presented their guesses. 
* They all get a reveal button to see the results.
* Since there are no more stories without guesses, everyone automatically gets a writing prompt. (Results from previous round is still on top).
* Game continues.....




Client UI should be dumb. Server should do the complex logic. 

Server sends a payload with the following:

{
    state: Enum["WRITING", "GUESSING", "WAITING"]
    room: room_id
    users: List[user_ids]
    stories: List[story_ids]
    progress: {user_id: {completed: 4, pending: 3, total: 7}, user_id2: {completed: 5, pending: 2, total: 7}}
}

Client will show the following information to the user: 

* Display the current state in big heading letters
* List of all users in the room and their current progress
* If state is WRITING:
    * List of stories will be empty
    * Show a textbox to type in the story
* Else:
    * Display the first story from the list.
    * If state is GUESSING:
        * Ask for a guess
    * Elif state is WAITING:
        * Do nothing

Server will construct the payload as follows:


