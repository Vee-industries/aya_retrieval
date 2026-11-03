"""More ways the friend says they have forgotten a fact, for the train pool only (fix 6).

Each train fact template has one indirect phrasing of its own. These add three more each, mostly
statements with no question mark, so training shows that talk about forgetting is a request for
the fact. None uses an idiom from the probe pool ("drawing a blank", "blanking", "tip of my tongue",
"cannot think"), so the probe still measures phrasings the model has not seen. The held-out pool's
phrasings were not read.

Keyed by the template's own ``indirect`` phrasing, which is unique in the train pool.
"""

from __future__ import annotations

MORE_INDIRECT: dict[str, tuple[str, ...]] = {
    "i can't remember what my {relation}'s dog is called": (
        "my {relation}'s dog's name just won't come to me",
        "i had my {relation}'s dog's name a second ago and now it's gone",
        "the dog my {relation} adopted, its name has gone clean out of my head",
    ),
    "i forget where my {relation} is moving": (
        "my {relation} told me where they're moving and i've lost it",
        "the city my {relation} is moving to has slipped my mind",
        "i keep mixing up where my {relation} is going",
    ),
    "remind me what my {relation} does for work": (
        "my {relation}'s new job has gone right out of my head",
        "i'm useless, i can't say what my {relation} does now",
        "someone asked about my {relation}'s work and i had nothing",
    ),
    "i keep forgetting what my {relation} drives": (
        "the car my {relation} bought won't come back to me",
        "i was telling a friend about my {relation}'s car and lost the model",
        "my {relation}'s auction car, i can't for the life of me recall it",
    ),
    "i was trying to think of what my {relation} does on weekends": (
        "my {relation}'s weekend thing has completely escaped me",
        "i had my {relation}'s new hobby in my head this morning",
        "what my {relation} took up lately has gone fuzzy",
    ),
    "the name of my {relation}'s kitten escapes me": (
        "my {relation}'s kitten has a name and i've lost it",
        "i wanted to ask after my {relation}'s kitten but the name's gone",
        "the kitten's name, my {relation}'s one, won't surface",
    ),
    "i had my {relation}'s street written down somewhere": (
        "my {relation}'s new street has gone right out of my head",
        "i'm sending a card to my {relation} and can't recall the street",
        "where my {relation} lives now just won't come to me",
    ),
    "not sure what kind of phone my {relation} went with": (
        "the phone my {relation} switched to has slipped my mind",
        "my {relation} told me which phone they got and i've lost it",
        "i keep confusing which phone my {relation} has now",
    ),
    "the name of my {relation}'s band is gone from my head": (
        "my {relation}'s band name just won't come to me",
        "i wanted to look up my {relation}'s band but i lost the name",
        "the band my {relation} plays in, i had it a minute ago",
    ),
    "i want to send a gift but i forget my {relation}'s baby's name": (
        "my {relation}'s baby's name has gone out of my head",
        "i'm writing a card for my {relation}'s baby and the name won't come",
        "the name my {relation} picked for the baby escapes me now",
    ),
    "i keep meaning to visit my {relation}'s shop, what kind was it again": (
        "the shop my {relation} opened, i can't recall what it sells",
        "my {relation}'s new shop has slipped my mind",
        "i was going to send people to my {relation}'s shop and lost what kind it is",
    ),
    "i meant to congratulate my {relation} but what was the race": (
        "the race my {relation} finished has gone right out of my head",
        "i want to say well done to my {relation} and the race won't come to me",
        "my {relation} ran something on sunday and i've lost which",
    ),
    "i should ask how my {relation} is healing, what was it they broke": (
        "what my {relation} broke skiing has slipped my mind",
        "i'm calling my {relation} later and can't recall the injury",
        "my {relation} hurt something skiing and i've lost what",
    ),
    "what my {relation}'s boat is called has slipped away from me": (
        "my {relation}'s boat name won't come to me",
        "i wanted to tell someone the name of my {relation}'s boat and it's gone",
        "the boat my {relation} owns, its name has gone fuzzy",
    ),
    "i'm at the cafe and i can't recall my {relation}'s usual": (
        "my {relation}'s coffee order has gone out of my head",
        "i'm ordering for my {relation} and the drink won't come to me",
        "what my {relation} always orders has slipped my mind",
    ),
    "my {relation}'s birthday month is on the edge of my memory": (
        "when my {relation} was born has gone right out of my head",
        "i'm planning something for my {relation} and the month won't come",
        "the month my {relation} was born escapes me",
    ),
    "there was something my {relation} won, what was that": (
        "the raffle prize my {relation} won has slipped my mind",
        "my {relation} won something silly and i've lost what",
        "i was laughing about my {relation}'s prize and now it's gone",
    ),
    "i was telling someone about my {relation}'s novels, what genre are they": (
        "the kind of books my {relation} writes has gone out of my head",
        "my {relation}'s novels, the genre won't come to me",
        "i keep losing what my {relation} writes at night",
    ),
    "i'm trying to picture my {relation}'s house, what colour is it": (
        "the colour of my {relation}'s house has slipped my mind",
        "my {relation} repainted and i've lost the colour",
        "what colour my {relation}'s place is now won't come to me",
    ),
    "i'm in the lobby and i've lost my {relation}'s floor": (
        "my {relation}'s floor number has gone right out of my head",
        "i'm in the lift and can't recall which floor my {relation} is on",
        "the floor my {relation} rents on escapes me",
    ),
    "my {relation} teaches something at the high school but what": (
        "what my {relation} teaches has slipped my mind",
        "my {relation}'s subject at the high school won't come to me",
        "i was asked what my {relation} teaches and i had nothing",
    ),
    "the animals my {relation} keeps, i can never remember what they are": (
        "what my {relation} keeps in the yard has gone out of my head",
        "my {relation}'s animals, i've lost what they are",
        "the creatures in my {relation}'s yard escape me",
    ),
    "my {relation} is off to some festival and i forget which": (
        "the festival my {relation} got tickets to has slipped my mind",
        "my {relation}'s festival plans won't come back to me",
        "i've lost which festival my {relation} is going to",
    ),
    "i can't place the bike my {relation} rides": (
        "the bike my {relation} rides to work has gone out of my head",
        "my {relation}'s bike, the make won't come to me",
        "i keep losing what my {relation} rides",
    ),
    "my {relation} got a new title and i've lost track of it": (
        "my {relation}'s promotion, the title escapes me",
        "what my {relation} got promoted to has slipped my mind",
        "i want to congratulate my {relation} and the new role won't come to me",
    ),
}
