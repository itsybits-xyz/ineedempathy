Gameplay:

JOINS:

* User (Baylee) creates a room and joins in.
* Baylee is placed in waiting room. 
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
    state: Enum["WRITING", "GUESSING", "RESULTS", "WAITING", "TRANSITION"]
    room: room_id
    users: List[user_ids]
    stories: List[story_ids]
    progress: {user_id: {completed: 4, pending: 3}, user_id2: {completed: 5, pending: 2}}
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

* Ping the clients periodically to check if they're active.
* Game state is WAITING.
* Server sends
{
    state: "WAITING",
    room: room_id,
    users: [1, 2, 3]
    stories: []
    progress: {1: {completed: 0, pending: 0}, 2: {completed: 0, pending: 0}, 3: {completed: 0, pending: 0}}
}

* Client sends next step:
* Game state is WRITING.
* Server sends
{
    state: "WRITING",
    room: room_id,
    users: [1, 2, 3]
    stories: []
    progress: {1: {completed: 0, pending: 1}, 2: {completed: 0, pending: 1}, 3: {completed: 0, pending: 1}}
}

* Baylee (user 1) submits a story (Story ID 23 is assigned by the DB).
* Server sends the following payload to

User 1
{
    state: "WRITING",    # WAITING so client does nothing.
    room: room_id,
    users: [1, 2, 3]
    stories: [] 
    progress: {1: {completed: 1, pending: 0}, 2: {completed: 0, pending: 1}, 3: {completed: 0, pending: 1}}
}

User 2 & 3
{
    state: "WRITING",    # WRITING so client still keeps the text box open.
    room: room_id,
    users: [1, 2, 3]
    stories: []
    progress: {1: {completed: 1, pending: 0}, 2: {completed: 0, pending: 1}, 3: {completed: 0, pending: 1}}
}

* Amjith (user 2) submits a story (Story ID 31 is assigned by the DB).
* Princess (user 3) submits a story (Story ID 33 is assigned by the DB).
* Server sends the following payload to everyone.

User 1, 2, 3
{
    state: "WAITING",
    room: room_id,
    users: [1, 2, 3]
    stories: []
    progress: {1: {completed: 1, pending: 0}, 2: {completed: 1, pending: 0}, 3: {completed: 1, pending: 0}}
}

* Baylee clicks on next step.
* Since all the users in the room are done, the server transitions to the next step. 
* Game state is now GUESSING.
* Amjith (2) story was selected first for guessing.
* Server sends the following payload

User 2

{
    state: "WAITING",
    room: room_id,
    users: [1, 2, 3]
    stories: [31]  
    progress: {1: {completed: 0, pending: 1}, 2: {completed: 0, pending: 0}, 3: {completed: 0, pending: 1}}
}

User 1 & 3

{
    state: "GUESSING",
    room: room_id,
    users: [1, 2, 3]
    stories: [31]
    progress: {1: {completed: 0, pending: 1}, 2: {completed: 0, pending: 0}, 3: {completed: 0, pending: 1}}
}

* Baylee submits a guess.
* Server sends the following

User 1 & 2
{
    state: "WAITING",
    room: room_id,
    users: [1, 2, 3]
    stories: [31]  
    progress: {1: {completed: 1, pending: 0}, 2: {completed: 0, pending: 0}, 3: {completed: 0, pending: 1}}
}
User 3
{
    state: "GUESSING",
    room: room_id,
    users: [1, 2, 3]
    stories: [31]  
    progress: {1: {completed: 1, pending: 0}, 2: {completed: 0, pending: 0}, 3: {completed: 0, pending: 1}}
}

* Princess becomes inactive.
* Amjith clicks next step.
* Server sends the following to all users (except Amjith)

User 1 & 3
{
    state: NEXT_STEP
}

* Client displays a CONFIRM button to all users.
* Baylee presses CONFIRM.
* Game transitions to next step.
* Server sends the following:

User 1 & 2
{
    state: "RESULTS",
    room: room_id,
    users: [1, 2],
    stories: [31],
    progress: {1: {results: [45]}, 2: {}}
}

* Client displays the results for all the users.
* Amjith clicks next step.
* Server sends

User 1 & 2
{
    state: NEXT_STEP
}

* Baylee confirms.
* Now back to guessing.
* Server sends Princess' story for guessing

{
    state: "GUESSING",
    room: room_id,
    users: [1, 2],
    stories: [33], 
    progress: {1: {completed: 0, pending: 1}, 2: {completed: 0, pending: 1}}
}

* Continues....
