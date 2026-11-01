"""The made-up words conversations are built from, in three pools that share no content.

``train`` also serves development checks, on seeds training never used. ``heldout`` is read only by
the final runs: its people, subjects, facts, questions and small talk appear nowhere in ``train``.
``probe`` is development material the adapter never trained on, so a check can tell a learned habit
from memorised templates without opening ``heldout``. It never enters a training set.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FactTemplate:
    """One kind of fact, the ways to ask for it, and how a good answer and search read."""

    values: tuple[str, ...]
    statement: str
    same_words: str
    new_words: str
    indirect: str
    confirm: str
    query: str
    answer: str


@dataclass(frozen=True)
class SmallTalkMood:
    """User lines and fitting replies; every line takes a ``{subject}``."""

    user_lines: tuple[str, ...]
    replies: tuple[str, ...]


@dataclass(frozen=True)
class Pool:
    """Everything one conversation is built from."""

    people: tuple[str, ...]
    relations: tuple[str, ...]
    facts: dict[str, FactTemplate]
    subjects: tuple[str, ...]
    moods: tuple[SmallTalkMood, ...]
    acknowledgements: tuple[str, ...]
    statements: tuple[tuple[str, str], ...]
    unknown_replies: tuple[str, ...]


TRAIN = Pool(
    people=("Dana", "Marc", "Priya", "Tomas", "Lena", "Omar", "Greta", "Yusuf", "Nell", "Ivan"),
    relations=("sister", "brother", "neighbour", "cousin", "coworker", "aunt", "uncle", "roommate"),
    facts={
        "dog": FactTemplate(
            values=("Pepper", "Rusty", "Biscuit", "Juno", "Waffles", "Clover"),
            statement="my {relation} {person} adopted a dog named {value} last month",
            same_words="what is the name of the dog {person} adopted",
            new_words="what do they call that pup over at my {relation}'s place",
            indirect="i can't remember what my {relation}'s dog is called",
            confirm="did i ever tell you about my {relation}'s dog",
            query="{who} dog name",
            answer="Your {relation} {person}'s dog is called {value}.",
        ),
        "city": FactTemplate(
            values=("Lisbon", "Oslo", "Tbilisi", "Valparaiso", "Hobart", "Quebec City"),
            statement="my {relation} {person} is moving to {value} in the spring",
            same_words="which city is {person} moving to",
            new_words="where is my {relation} headed once winter is over",
            indirect="i forget where my {relation} is moving",
            confirm="did i mention my {relation}'s move",
            query="{who} moving city",
            answer="Your {relation} {person} is moving to {value}.",
        ),
        "job": FactTemplate(
            values=(
                "welder",
                "paramedic",
                "surveyor",
                "pastry chef",
                "court reporter",
                "beekeeper",
            ),
            statement="my {relation} {person} just started work as a {value}",
            same_words="what job did {person} start",
            new_words="what does my {relation} do for a living these days",
            indirect="remind me what my {relation} does for work",
            confirm="did i tell you about my {relation}'s new job",
            query="{who} new job",
            answer="Your {relation} {person} works as a {value}.",
        ),
        "car": FactTemplate(
            values=("green Corolla", "red Civic", "blue Tacoma", "white Forester", "grey Golf"),
            statement="my {relation} {person} bought a {value} from an auction",
            same_words="what car did {person} buy at the auction",
            new_words="what's my {relation} driving around in now",
            indirect="i keep forgetting what my {relation} drives",
            confirm="have i told you about my {relation}'s car",
            query="{who} car auction",
            answer="Your {relation} {person} bought a {value}.",
        ),
        "hobby": FactTemplate(
            values=("pottery", "curling", "birdwatching", "fencing", "glassblowing", "bouldering"),
            statement="my {relation} {person} has taken up {value} on weekends",
            same_words="what has {person} taken up on weekends",
            new_words="how does my {relation} keep busy on saturdays",
            indirect="i was trying to think of what my {relation} does on weekends",
            confirm="did i bring up my {relation}'s new hobby",
            query="{who} weekend hobby",
            answer="Your {relation} {person} has taken up {value}.",
        ),
    },
    subjects=(
        "the bus",
        "my knee",
        "the garden",
        "that show",
        "the fridge",
        "the rain",
        "my phone",
        "the bakery",
        "the laundry",
        "my desk",
        "the snow",
        "the printer",
        "the kettle",
        "my bike",
        "the roof",
        "the wifi",
        "the parking lot",
        "my coffee",
        "the dishwasher",
        "the mail",
        "the gym",
        "my back",
        "the stairs",
        "the furnace",
        "the groceries",
        "my glasses",
        "the bank",
        "the dentist",
        "the lawn",
        "the recycling",
        "my laptop",
        "the elevator",
    ),  # fmt: skip
    moods=(
        SmallTalkMood(
            user_lines=(
                "{subject} was acting up again today",
                "ugh, {subject} is driving me up the wall",
                "{subject} let me down this morning",
                "so {subject} has been a pain all week",
                "i lost an hour to {subject} today",
                "{subject} is getting on my nerves",
            ),
            replies=(
                "That sounds annoying. Hope {subject} settles down soon.",
                "Sorry, {subject} sounds like a real hassle.",
                "That's frustrating. Is {subject} usually like that?",
                "Oof. An hour lost to {subject} is no fun.",
                "I'd be fed up with {subject} too.",
            ),
        ),
        SmallTalkMood(
            user_lines=(
                "{subject} turned out fine in the end",
                "good news, {subject} sorted itself out",
                "i'm actually pretty happy with {subject} lately",
                "{subject} was the best part of my day",
                "no complaints about {subject} this week",
            ),
            replies=(
                "Glad {subject} worked out.",
                "Nice, that's one less thing to think about.",
                "Good to hear {subject} is behaving.",
                "That's a small win. {subject} sounds good.",
                "Love that for you.",
            ),
        ),
        SmallTalkMood(
            user_lines=(
                "i was thinking about {subject} on the way home",
                "not much going on, just dealing with {subject}",
                "anyway, enough about {subject}",
                "someone at work brought up {subject} today",
                "{subject} came up at dinner",
                "funny how {subject} keeps coming up",
            ),
            replies=(
                "What about {subject} got you thinking?",
                "Fair enough, one thing at a time.",
                "Sure, we can move on from {subject}.",
                "Ha, what did they say about {subject}?",
                "It does seem to come up a lot.",
                "Tell me more if you feel like it.",
            ),
        ),
    ),
    acknowledgements=(
        "Thanks for telling me.",
        "Oh, that's nice to hear.",
        "Good to know.",
        "That's a change.",
        "How are they finding it?",
        "That sounds exciting for them.",
    ),
    statements=(
        ("my {relation} called me last night", "That's nice. How are they doing?"),
        ("{person} and i went for a long walk today", "Sounds like a good way to spend the day."),
        ("i haven't seen my {relation} in ages", "That's a long time. Are you hoping to catch up?"),
        ("guess who ran into {person} at the store", "Small world. How did that go?"),
        ("you won't believe what my {relation} said today", "Now I'm curious. What did they say?"),
        ("{person} still owes me twenty bucks", "Ha. Are you going to remind them?"),
    ),
    unknown_replies=(
        "I checked and you haven't told me that.",
        "That hasn't come up in our conversation, so I don't know.",
        "I don't have that from you. What is it?",
    ),
)

HELDOUT = Pool(
    people=("Rosa", "Felix", "Anika", "Bruno", "Mei", "Callum", "Ingrid", "Tariq", "Odile", "Sven"),
    relations=("mother", "father", "nephew", "niece", "landlord", "boss", "friend", "grandmother"),
    facts={
        "instrument": FactTemplate(
            values=("cello", "banjo", "trombone", "accordion", "oboe", "ukulele"),
            statement="{person}, my {relation}, signed up for {value} lessons downtown",
            same_words="which lessons did {person} sign up for downtown",
            new_words="what is my {relation} learning to play",
            indirect="it slipped my mind what my {relation} is learning",
            confirm="i think i told you what my {relation} is learning, didn't i",
            query="{who} lessons instrument",
            answer="{person} signed up for {value} lessons.",
        ),
        "allergy": FactTemplate(
            values=("shellfish", "walnuts", "penicillin", "sesame", "latex", "kiwi"),
            statement="turns out {person}, my {relation}, is allergic to {value}",
            same_words="what is {person} allergic to",
            new_words="what should i keep away from my {relation} when i cook",
            indirect="i need to remember what my {relation} reacts badly to",
            confirm="i told you about my {relation}'s allergy, right",
            query="{who} allergy",
            answer="{person} is allergic to {value}.",
        ),
        "trip": FactTemplate(
            values=("Reykjavik", "Marrakesh", "Cusco", "Hanoi", "Bergen", "Zanzibar"),
            statement="{person}, my {relation}, booked flights to {value} for april",
            same_words="where did {person} book flights to",
            new_words="where's my {relation} off to on holiday",
            indirect="no idea where my {relation} said they were flying",
            confirm="i mentioned my {relation}'s holiday plans, didn't i",
            query="{who} flights holiday",
            answer="{person} booked flights to {value}.",
        ),
        "course": FactTemplate(
            values=("nursing", "marine biology", "carpentry", "accounting", "urban planning"),
            statement="{person}, my {relation}, enrolled in a {value} programme this fall",
            same_words="which programme did {person} enrol in",
            new_words="what is my {relation} studying now",
            indirect="i blanked on what my {relation} went back to school for",
            confirm="pretty sure i told you what my {relation} is studying",
            query="{who} programme studying",
            answer="{person} enrolled in {value}.",
        ),
        "food": FactTemplate(
            values=("pierogi", "ramen", "paella", "tamales", "baklava", "gnocchi"),
            statement="{person}, my {relation}, makes the best {value} i have ever eaten",
            same_words="what does {person} make the best version of",
            new_words="what should i ask my {relation} to cook when we visit",
            indirect="trying to recall the dish my {relation} is famous for",
            confirm="i bragged about my {relation}'s cooking to you, didn't i",
            query="{who} best dish cooking",
            answer="{person} makes the best {value}.",
        ),
    },
    subjects=(
        "the ferry",
        "my shoulder",
        "the balcony",
        "that podcast",
        "the oven",
        "the fog",
        "my tablet",
        "the deli",
        "the ironing",
        "my chair",
        "the hail",
        "the scanner",
        "the toaster",
        "my scooter",
        "the gutters",
        "the router",
        "the driveway",
        "my tea",
        "the washing machine",
        "the parcels",
        "the pool",
        "my wrist",
        "the attic",
        "the boiler",
        "the market",
        "my watch",
        "the post office",
        "the optician",
        "the hedge",
        "the compost",
        "my headphones",
        "the lift",
    ),  # fmt: skip
    moods=(
        SmallTalkMood(
            user_lines=(
                "{subject} gave me grief again",
                "honestly {subject} is wearing me out",
                "{subject} ruined my morning",
                "still fighting with {subject}",
                "wasted half the afternoon on {subject}",
                "{subject} has been nothing but trouble",
            ),
            replies=(
                "Sorry to hear {subject} is giving you grief.",
                "That would wear me out as well.",
                "What a way to start the day. What happened with {subject}?",
                "Still? {subject} sounds stubborn.",
                "Half an afternoon is a lot to give to {subject}.",
            ),
        ),
        SmallTalkMood(
            user_lines=(
                "{subject} finally came through",
                "pleased to say {subject} is behaving",
                "{subject} made my week",
                "had a surprisingly good time with {subject}",
                "{subject} is looking up",
            ),
            replies=(
                "About time {subject} came through.",
                "That's a relief.",
                "Sounds like {subject} really helped.",
                "Good surprises are the best kind.",
                "Happy to hear {subject} is looking up.",
            ),
        ),
        SmallTalkMood(
            user_lines=(
                "was chatting about {subject} earlier",
                "just pottering, sorting out {subject}",
                "moving on from {subject} now",
                "a friend asked me about {subject}",
                "{subject} crossed my mind this afternoon",
                "strange how often i end up talking about {subject}",
            ),
            replies=(
                "Who were you chatting with about {subject}?",
                "That's a calm way to spend the day.",
                "Alright, what's next after {subject}?",
                "What did your friend want to know?",
                "Anything in particular about {subject}?",
                "Some things just keep coming back.",
            ),
        ),
    ),
    acknowledgements=(
        "Noted, thanks.",
        "Well, that's interesting.",
        "I'll keep that in mind.",
        "Sounds like a big step.",
        "How do they feel about it?",
        "What a nice bit of news.",
    ),
    statements=(
        ("my {relation} rang while i was out", "Hope nothing's wrong. Did you ring back?"),
        ("{person} and i had lunch by the water", "That sounds lovely."),
        ("i really ought to visit my {relation}", "Is it a long trip?"),
        ("you'll never guess who i bumped into, {person}", "Oh! How were they?"),
        ("can you believe my {relation} did that", "I'm not sure what happened. What did they do?"),
        ("{person} borrowed my ladder and never brought it back", "Time to ask for it back?"),
    ),
    unknown_replies=(
        "That hasn't come up between us.",
        "You haven't mentioned that to me.",
        "I don't know that one. You'd have to tell me.",
    ),
)

PROBE = Pool(
    people=(
        "Ayaan",
        "Beatriz",
        "Chidi",
        "Dmitri",
        "Esme",
        "Farah",
        "Gustav",
        "Hana",
        "Kofi",
        "Lucia",
    ),
    relations=(
        "teammate",
        "classmate",
        "stepsister",
        "godfather",
        "barber",
        "tutor",
        "mentor",
        "daughter",
    ),
    facts={
        "tattoo": FactTemplate(
            values=("anchor", "swallow", "compass", "lighthouse", "koi", "thistle"),
            statement="{person}, who is my {relation}, got a {value} tattoo last week",
            same_words="what tattoo did {person} get",
            new_words="what's the new ink on my {relation}",
            indirect="drawing a blank on my {relation}'s tattoo",
            confirm="did i say anything about my {relation}'s tattoo",
            query="{who} tattoo",
            answer="{person} got a {value} tattoo.",
        ),
        "fear": FactTemplate(
            values=("spiders", "heights", "pigeons", "thunderstorms", "deep water", "clowns"),
            statement="{person}, who is my {relation}, is terrified of {value}",
            same_words="what is {person} terrified of",
            new_words="what freaks my {relation} out the most",
            indirect="i'm blanking on what my {relation} is scared of",
            confirm="have i ever mentioned what scares my {relation}",
            query="{who} scared fear",
            answer="{person} is terrified of {value}.",
        ),
        "club": FactTemplate(
            values=("rowing", "handball", "lacrosse", "water polo", "badminton", "archery"),
            statement="{person}, who is my {relation}, joined a {value} club this month",
            same_words="which club did {person} join",
            new_words="where does my {relation} go after work these days",
            indirect="it's on the tip of my tongue which club my {relation} joined",
            confirm="did i say which club my {relation} joined",
            query="{who} club joined",
            answer="{person} joined a {value} club.",
        ),
        "crop": FactTemplate(
            values=("tomatoes", "zucchini", "pumpkins", "chillies", "strawberries", "asparagus"),
            statement="{person}, who is my {relation}, grows prize {value} out back",
            same_words="what does {person} grow out back",
            new_words="what's growing behind my {relation}'s house",
            indirect="i cannot think what my {relation} grows",
            confirm="did i ever bring up what my {relation} grows",
            query="{who} grows garden",
            answer="{person} grows prize {value}.",
        ),
        "language": FactTemplate(
            values=("Portuguese", "Swahili", "Korean", "Welsh", "Turkish", "Tagalog"),
            statement="{person}, who is my {relation}, speaks fluent {value}",
            same_words="what language does {person} speak",
            new_words="what can my {relation} speak besides english",
            indirect="i forget which language my {relation} knows",
            confirm="did i mention what language my {relation} speaks",
            query="{who} language speaks",
            answer="{person} speaks fluent {value}.",
        ),
    },
    subjects=(
        "the tram",
        "my ankle",
        "the patio",
        "that novel",
        "the freezer",
        "the wind",
        "my camera",
        "the butcher",
        "the vacuuming",
        "my couch",
        "the sleet",
        "the photocopier",
        "the blender",
        "my skateboard",
        "the chimney",
        "the modem",
        "the garage",
        "my smoothie",
        "the dryer",
        "the courier",
        "the sauna",
        "my neck",
        "the basement",
        "the radiator",
        "the pharmacy",
        "my keys",
        "the library",
        "the vet",
        "the fence",
        "the bins",
        "my charger",
        "the escalator",
    ),  # fmt: skip
    moods=(
        SmallTalkMood(
            user_lines=(
                "{subject} is testing my patience",
                "so fed up with {subject} right now",
                "{subject} messed up my whole plan",
                "another bad day thanks to {subject}",
                "spent all evening sorting out {subject}",
                "{subject} keeps letting me down",
            ),
            replies=(
                "That's rough. What went wrong with {subject}?",
                "Sounds like you've had enough of {subject}.",
                "Ugh, sorry about {subject}.",
                "Plans and {subject} clearly don't mix.",
                "All evening? I hope {subject} is sorted now.",
            ),
        ),
        SmallTalkMood(
            user_lines=(
                "{subject} went better than expected",
                "happy to report {subject} is all good",
                "{subject} cheered me up today",
                "really enjoying {subject} at the moment",
                "{subject} turned a corner this week",
            ),
            replies=(
                "Great, {subject} deserved a good day.",
                "That's lovely to hear.",
                "Nice one. What changed with {subject}?",
                "Enjoy it while it lasts.",
                "Sounds like {subject} is on the up.",
            ),
        ),
        SmallTalkMood(
            user_lines=(
                "was reading about {subject} at lunch",
                "quiet day, mostly {subject}",
                "that's all i've got on {subject}",
                "my mom asked about {subject} again",
                "{subject} popped into my head earlier",
                "weird how much of my week is {subject}",
            ),
            replies=(
                "Anything interesting about {subject}?",
                "Quiet days are underrated.",
                "No problem, what else is new?",
                "What did she want to know about {subject}?",
                "Funny what pops up.",
                "Weeks can go that way.",
            ),
        ),
    ),
    acknowledgements=(
        "Oh wow, okay.",
        "That's cool.",
        "Thanks for the update.",
        "Didn't see that coming.",
        "What do you make of that?",
        "Sounds like quite the news.",
    ),
    statements=(
        ("my {relation} texted me out of nowhere", "Oh? What did the text say?"),
        ("{person} and i grabbed coffee this morning", "Nice. How was it?"),
        ("i should really call my {relation}", "Any special reason?"),
        ("i got stuck talking to {person} for an hour", "An hour! What about?"),
        ("my {relation} has been acting strange lately", "Strange how?"),
        ("{person} forgot my birthday again", "Oof, sorry. Does that happen a lot?"),
    ),
    unknown_replies=(
        "You've never told me that.",
        "I looked and nothing about that came up.",
        "No idea, I don't have that from you.",
    ),
)

POOLS = {"train": TRAIN, "heldout": HELDOUT, "probe": PROBE}
