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
        "cat": FactTemplate(
            values=("Mochi", "Tofu", "Pickle", "Sprout", "Noodle", "Marble"),
            statement="{person} is my {relation} and just got a kitten called {value}",
            same_words="what did {person} call the kitten",
            new_words="what's the name of my {relation}'s kitten",
            indirect="the name of my {relation}'s kitten escapes me",
            confirm="did i tell you my {relation} got a kitten",
            query="{who} kitten",
            answer="Your {relation} {person} called the kitten {value}.",
        ),
        "street": FactTemplate(
            values=(
                "Alder Road",
                "Birch Lane",
                "Cedar Court",
                "Elm Terrace",
                "Hazel Drive",
                "Juniper Way",
            ),
            statement="you know my {relation} {person}? they live on {value} now",
            same_words="what street does {person} live on",
            new_words="where do i send a card for my {relation}",
            indirect="i had my {relation}'s street written down somewhere",
            confirm="have i told you what street my {relation} lives on",
            query="{who} street address",
            answer="Your {relation} {person} lives on {value}.",
        ),
        "phone": FactTemplate(
            values=("Pixel", "iPhone", "Nokia", "Galaxy", "Motorola", "Fairphone"),
            statement="so {person} (my {relation}) finally switched to a {value}",
            same_words="what phone did {person} switch to",
            new_words="what's my {relation} using for a phone",
            indirect="not sure what kind of phone my {relation} went with",
            confirm="did i bring up my {relation}'s phone",
            query="{who} phone switched",
            answer="Your {relation} {person} switched to a {value}.",
        ),
        "band": FactTemplate(
            values=("The Lanterns", "Night Bus", "Paper Tigers", "Copper Moon", "Salt Road"),
            statement="talked to {person} today, my {relation}, who plays bass in {value}",
            same_words="what band does {person} play bass in",
            new_words="who does my {relation} gig with",
            indirect="the name of my {relation}'s band is gone from my head",
            confirm="did i ever mention my {relation}'s band",
            query="{who} band bass",
            answer="Your {relation} {person} plays bass in {value}.",
        ),
        "baby": FactTemplate(
            values=("Silas", "Mila", "Arlo", "Nora", "Hugo", "Esther"),
            statement="my {relation}, {person}, had a baby and named them {value}",
            same_words="what did {person} name the baby",
            new_words="what's my {relation}'s little one called",
            indirect="i want to send a gift but i forget my {relation}'s baby's name",
            confirm="have i said anything about my {relation}'s baby",
            query="{who} baby name",
            answer="Your {relation} {person} named the baby {value}.",
        ),
        "shop": FactTemplate(
            values=("florist", "thrift", "comic", "candle", "vintage", "cheese"),
            statement="news from my {relation} {person}: they opened a {value} shop",
            same_words="what kind of shop did {person} open",
            new_words="what does my {relation} sell these days",
            indirect="i keep meaning to visit my {relation}'s shop, what kind was it again",
            confirm="did i tell you what my {relation} opened",
            query="{who} shop opened",
            answer="Your {relation} {person} opened a {value} shop.",
        ),
        "race": FactTemplate(
            values=("half marathon", "triathlon", "5k", "10k", "duathlon", "relay"),
            statement="apparently my {relation} {person} finished a {value} on sunday",
            same_words="what race did {person} finish on sunday",
            new_words="what did my {relation} run at the weekend",
            indirect="i meant to congratulate my {relation} but what was the race",
            confirm="did i mention my {relation}'s race",
            query="{who} race finished",
            answer="Your {relation} {person} finished a {value}.",
        ),
        "injury": FactTemplate(
            values=("collarbone", "thumb", "kneecap", "jaw", "pelvis", "forearm"),
            statement="{person}, the {relation} i keep talking about, broke a {value} skiing",
            same_words="what did {person} break skiing",
            new_words="how did my {relation} get hurt on the slopes",
            indirect="i should ask how my {relation} is healing, what was it they broke",
            confirm="did i say what my {relation} broke",
            query="{who} broke skiing injury",
            answer="Your {relation} {person} broke a {value}.",
        ),
        "boat": FactTemplate(
            values=("Sea Otter", "Blue Heron", "Second Wind", "Lady Grace", "Driftwood"),
            statement="{person} is my {relation}, and their boat is called {value}",
            same_words="what is {person}'s boat called",
            new_words="what name is painted on my {relation}'s boat",
            indirect="what my {relation}'s boat is called has slipped away from me",
            confirm="have i ever told you about my {relation}'s boat",
            query="{who} boat name",
            answer="Your {relation} {person}'s boat is called {value}.",
        ),
        "coffee": FactTemplate(
            values=("flat white", "cortado", "mocha", "macchiato", "americano", "chai latte"),
            statement="for the record my {relation} {person} only ever orders a {value}",
            same_words="what does {person} always order",
            new_words="what should i get my {relation} from the cafe",
            indirect="i'm at the cafe and i can't recall my {relation}'s usual",
            confirm="did i mention my {relation}'s usual order",
            query="{who} usual order cafe",
            answer="Your {relation} {person} only orders a {value}.",
        ),
        "birth": FactTemplate(
            values=("March", "July", "October", "February", "November", "August"),
            statement="i just learned {person} was born in {value}, and that's my {relation}",
            same_words="what month was {person} born in",
            new_words="when should i plan my {relation}'s party",
            indirect="my {relation}'s birthday month is on the edge of my memory",
            confirm="did i ever say when my {relation} was born",
            query="{who} born birthday month",
            answer="Your {relation} {person} was born in {value}.",
        ),
        "prize": FactTemplate(
            values=("canoe", "hot tub", "lawnmower", "telescope", "kayak", "pinball machine"),
            statement="you'll laugh, my {relation} {person} won a {value} in a raffle",
            same_words="what did {person} win in the raffle",
            new_words="what did my {relation} get lucky with",
            indirect="there was something my {relation} won, what was that",
            confirm="did i say what my {relation} won",
            query="{who} raffle won prize",
            answer="Your {relation} {person} won a {value} in a raffle.",
        ),
        "genre": FactTemplate(
            values=("mystery", "romance", "fantasy", "horror", "western", "science fiction"),
            statement="my {relation}, {person}, writes {value} novels at night",
            same_words="what kind of novels does {person} write",
            new_words="what does my {relation} write about",
            indirect="i was telling someone about my {relation}'s novels, what genre are they",
            confirm="have i told you what my {relation} writes",
            query="{who} novels genre",
            answer="Your {relation} {person} writes {value} novels.",
        ),
        "paint": FactTemplate(
            values=("teal", "mustard", "coral", "lavender", "burgundy", "sage green"),
            statement="drove past {person}'s place, my {relation}, it's been painted {value}",
            same_words="what colour did {person} paint the house",
            new_words="how will i spot my {relation}'s house from the road",
            indirect="i'm trying to picture my {relation}'s house, what colour is it",
            confirm="did i mention the colour of my {relation}'s house",
            query="{who} house colour painted",
            answer="Your {relation} {person}'s house is painted {value}.",
        ),
        "floor": FactTemplate(
            values=("third", "ninth", "twelfth", "fifteenth", "seventh", "twentieth"),
            statement="{person} is my {relation}, and they rent on the {value} floor",
            same_words="which floor does {person} rent on",
            new_words="how far up do i go to reach my {relation}'s flat",
            indirect="i'm in the lobby and i've lost my {relation}'s floor",
            confirm="have i said what floor my {relation} lives on",
            query="{who} floor flat rent",
            answer="Your {relation} {person} rents on the {value} floor.",
        ),
        "subject": FactTemplate(
            values=("chemistry", "geometry", "history", "drama", "physics", "economics"),
            statement="you know my {relation} {person}? they teach {value} at the high school",
            same_words="what does {person} teach at the high school",
            new_words="what classes does my {relation} run",
            indirect="my {relation} teaches something at the high school but what",
            confirm="did i say what my {relation} teaches",
            query="{who} teaches high school",
            answer="Your {relation} {person} teaches {value}.",
        ),
        "animals": FactTemplate(
            values=("ferrets", "chickens", "goats", "rabbits", "tortoises", "geckos"),
            statement="so {person} (my {relation}) keeps {value} in the yard",
            same_words="what does {person} keep in the yard",
            new_words="what animals will i meet at my {relation}'s place",
            indirect="the animals my {relation} keeps, i can never remember what they are",
            confirm="have i told you about my {relation}'s animals",
            query="{who} keeps animals yard",
            answer="Your {relation} {person} keeps {value}.",
        ),
        "festival": FactTemplate(
            values=(
                "Glastonbury",
                "Coachella",
                "Burning Man",
                "Lollapalooza",
                "Oktoberfest",
                "Bonnaroo",
            ),
            statement="news from my {relation} {person}: they got tickets to {value}",
            same_words="what did {person} get tickets to",
            new_words="what is my {relation} going to this summer",
            indirect="my {relation} is off to some festival and i forget which",
            confirm="did i mention the tickets my {relation} got",
            query="{who} tickets festival",
            answer="Your {relation} {person} got tickets to {value}.",
        ),
        "motorbike": FactTemplate(
            values=("Ducati", "Harley", "Vespa", "Triumph", "Yamaha", "Kawasaki"),
            statement="apparently my {relation} {person} rides a {value} to work",
            same_words="what does {person} ride to work",
            new_words="what's parked outside my {relation}'s office",
            indirect="i can't place the bike my {relation} rides",
            confirm="did i ever say what my {relation} rides",
            query="{who} rides bike work",
            answer="Your {relation} {person} rides a {value}.",
        ),
        "promotion": FactTemplate(
            values=(
                "manager",
                "supervisor",
                "director",
                "team lead",
                "partner",
                "head of sales",
            ),
            statement="talked to {person} today, my {relation}, now promoted to {value}",
            same_words="what was {person} promoted to",
            new_words="what's my {relation}'s title now",
            indirect="my {relation} got a new title and i've lost track of it",
            confirm="did i tell you about my {relation}'s promotion",
            query="{who} promoted title",
            answer="Your {relation} {person} was promoted to {value}.",
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
        "I searched and there's nothing on that.",
        "No, I don't think you've told me.",
        "I can't find that anywhere in what you've said.",
        "Not that I can see. What's the story?",
        "Nothing on that here. Did you mean someone else?",
        "I don't see it, so I'd only be guessing.",
        "I don't know that one yet.",
        "Haven't heard about that. Tell me about it?",
        "You may not have mentioned it to me.",
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

# Imported last: it builds its pool from the classes above.
from aya_retrieval.pool_independent import INDEPENDENT  # noqa: E402

POOLS["independent"] = INDEPENDENT

# R-066: a development twin of the independent pool, by a fresh agent from its brief. Not sealed.
from aya_retrieval.pool_hard_dev import HARD_DEV  # noqa: E402

POOLS["hard_dev"] = HARD_DEV

# R-069: a wide training pool of new fact types, by a fresh agent. Training only.
from aya_retrieval.pool_wide import WIDE  # noqa: E402

POOLS["wide"] = WIDE
SEALED = ("heldout", "independent")
