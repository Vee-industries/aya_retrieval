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


# Fix 8: more ways the friend states each fact. Each train fact template has one statement, so the
# model saw every fact in one wording and learned to match words; these add three more each, with
# different words for the fact itself ("has a new pup called" beside "adopted a dog named"). Every
# one opens the way an existing train statement opens, so no opening can match a sealed pool's
# (a test enforces it). Keyed by the template's own statement, which is unique in the train pool.
MORE_STATEMENTS: dict[str, tuple[str, ...]] = {
    "my {relation} {person} adopted a dog named {value} last month": (
        "my {relation} {person} has a new pup called {value}",
        "{person} is my {relation} and their rescue dog goes by {value}",
        "you know my {relation} {person}? the dog they brought home is {value}",
    ),
    "my {relation} {person} is moving to {value} in the spring": (
        "my {relation} {person} is relocating to {value} after winter",
        "news from my {relation} {person}: they're packing up for {value}",
        "{person} is my {relation} and they've found a flat in {value} for next year",
    ),
    "my {relation} {person} just started work as a {value}": (
        "my {relation} {person} got hired as a {value}",
        "news from my {relation} {person}: they're working as a {value} now",
        "apparently my {relation} {person} trained up to be a {value}",
    ),
    "my {relation} {person} bought a {value} from an auction": (
        "my {relation} {person} won a bid on a {value}",
        "so {person} (my {relation}) is driving a {value} these days",
        "you know my {relation} {person}? they picked up a {value} cheap at a sale",
    ),
    "my {relation} {person} has taken up {value} on weekends": (
        "my {relation} {person} spends saturdays doing {value} now",
        "news from my {relation} {person}: they've got really into {value}",
        "{person} is my {relation} and their new hobby is {value}",
    ),
    "{person} is my {relation} and just got a kitten called {value}": (
        "my {relation} {person} brought home a kitten and named it {value}",
        "news from my {relation} {person}: the new kitten is {value}",
        "so {person} (my {relation}) has a tiny cat now, {value}",
    ),
    "you know my {relation} {person}? they live on {value} now": (
        "my {relation} {person} moved over to {value}",
        "{person} is my {relation} and their new address is on {value}",
        "news from my {relation} {person}: they've settled on {value}",
    ),
    "so {person} (my {relation}) finally switched to a {value}": (
        "my {relation} {person} got rid of the old phone for a {value}",
        "{person} is my {relation} and they're on a {value} now",
        "apparently my {relation} {person} upgraded to a {value}",
    ),
    "talked to {person} today, my {relation}, who plays bass in {value}": (
        "my {relation} {person} is in a band called {value}",
        "news from my {relation} {person}: {value} has a gig with them on bass",
        "{person} is my {relation} and they play bass for {value}",
    ),
    "my {relation}, {person}, had a baby and named them {value}": (
        "my {relation} {person} welcomed a little one called {value}",
        "news from my {relation} {person}: the baby's name is {value}",
        "{person} is my {relation} and they called their newborn {value}",
    ),
    "news from my {relation} {person}: they opened a {value} shop": (
        "my {relation} {person} runs a {value} store now",
        "{person} is my {relation} and they've launched a {value} business",
        "apparently my {relation} {person} got the keys to a {value} place in town",
    ),
    "apparently my {relation} {person} finished a {value} on sunday": (
        "my {relation} {person} crossed the line at a {value} this weekend",
        "{person} is my {relation} and they completed a {value} on sunday",
        "news from my {relation} {person}: they got through a whole {value}",
    ),
    "{person}, the {relation} i keep talking about, broke a {value} skiing": (
        "my {relation} {person} fractured a {value} on the slopes",
        "news from my {relation} {person}: a ski fall cracked their {value}",
        "{person} is my {relation} and they hurt their {value} skiing, it's broken",
    ),
    "{person} is my {relation}, and their boat is called {value}": (
        "my {relation} {person} named their boat {value}",
        "news from my {relation} {person}: the little sailboat is {value}",
        "you know my {relation} {person}? {value} is painted on the side of their boat",
    ),
    "for the record my {relation} {person} only ever orders a {value}": (
        "my {relation} {person} always gets a {value} at the cafe",
        "{person} is my {relation} and a {value} is their usual",
        "so {person} (my {relation}) won't drink anything but a {value}",
    ),
    "i just learned {person} was born in {value}, and that's my {relation}": (
        "my {relation} {person} has a birthday in {value}",
        "{person} is my {relation} and they were born in {value}",
        "news from my {relation} {person}: their birthday month is {value}",
    ),
    "you'll laugh, my {relation} {person} won a {value} in a raffle": (
        "my {relation} {person} took home a {value} from a prize draw",
        "{person} is my {relation} and they just won a {value} in a raffle",
        "news from my {relation} {person}: the raffle prize was a {value}",
    ),
    "my {relation}, {person}, writes {value} novels at night": (
        "my {relation} {person} is working on a {value} book",
        "{person} is my {relation} and they write {value} fiction in the evenings",
        "news from my {relation} {person}: another {value} manuscript is done",
    ),
    "drove past {person}'s place, my {relation}, it's been painted {value}": (
        "my {relation} {person} repainted the house {value}",
        "{person} is my {relation} and their walls are {value} now",
        "news from my {relation} {person}: the whole house is {value} this year",
    ),
    "{person} is my {relation}, and they rent on the {value} floor": (
        "my {relation} {person} lives up on the {value} floor",
        "news from my {relation} {person}: their flat is on the {value} floor",
        "you know my {relation} {person}? their place is on the {value} floor",
    ),
    "you know my {relation} {person}? they teach {value} at the high school": (
        "my {relation} {person} is a {value} teacher",
        "{person} is my {relation} and they take the {value} classes at the school",
        "news from my {relation} {person}: they're running the {value} department",
    ),
    "so {person} (my {relation}) keeps {value} in the yard": (
        "my {relation} {person} looks after {value} out back",
        "{person} is my {relation} and they've got {value} in the garden",
        "news from my {relation} {person}: the {value} got out of the yard again",
    ),
    "news from my {relation} {person}: they got tickets to {value}": (
        "my {relation} {person} is going to {value} this summer",
        "{person} is my {relation} and they've booked {value}",
        "apparently my {relation} {person} landed passes for {value}",
    ),
    "apparently my {relation} {person} rides a {value} to work": (
        "my {relation} {person} commutes on a {value}",
        "{person} is my {relation} and their bike is a {value}",
        "news from my {relation} {person}: they bought a {value} for getting around",
    ),
    "talked to {person} today, my {relation}, now promoted to {value}": (
        "my {relation} {person} got bumped up to {value}",
        "{person} is my {relation} and their new title is {value}",
        "news from my {relation} {person}: they made {value} this week",
    ),
}


# Fix 9: more ways the friend just talks about someone. The train pool has six chat lines, so
# the model saw few lines that name a person without asking for a fact, and none about how a
# person is behaving or feeling; trained harder, it began to answer such lines with a stored fact
# (R-055). These add 48, in the train pool's own voice. Statement rows take base's reply with no
# tool in sight, so the reply here is a reference only. No four-word run of any line appears in a
# sealed pool's or the probe's chat lines (a test enforces it).
MORE_CHAT: tuple[tuple[str, str], ...] = (
    ("my {relation} seems really quiet these days", "Quiet in a worrying way, or just busy?"),
    ("{person} was in a funny mood at dinner", "Funny how? Did something happen?"),
    ("my {relation} keeps cancelling on me", "That's frustrating. Is something going on?"),
    ("{person} snapped at me this morning", "Ouch. Do you know what set them off?"),
    ("i think my {relation} is avoiding me", "What makes you think so?"),
    ("{person} seemed off when i saw them", "Off in what way?"),
    ("my {relation} hasn't been sleeping well", "That's rough. Is something keeping them up?"),
    ("{person} was unusually cheerful today", "Nice. Any idea why?"),
    ("my {relation} is stressed out about work", "Sounds tough. Is it a busy stretch?"),
    ("{person} has gone very quiet in the group chat", "Maybe they're busy. Have you checked in?"),
    ("my {relation} was in tears on the phone", "Oh no. Are they okay?"),
    ("{person} keeps sighing whenever i bring it up", "Sounds like a sore spot. What's it about?"),
    ("saturday works for my {relation} to visit", "Are you up for it?"),
    ("{person} and i are planning a trip", "Fun! Where are you thinking?"),
    ("i promised my {relation} i'd help them move", "That's good of you. When is it?"),
    ("{person} invited me to a party", "Are you going to go?"),
    (
        "my {relation} will be staying with me all week",
        "A whole week! Are you looking forward to it?",
    ),
    ("thinking of surprising {person} with a visit", "That would be a nice surprise."),
    ("i owe my {relation} a thank-you card", "Better late than never."),
    ("{person} asked me to be their plus one", "Ooh. Are you going to say yes?"),
    ("my {relation} never answers their phone", "That's annoying. Maybe try a text?"),
    ("{person} was late again", "How late this time?"),
    ("my {relation} keeps giving me advice i didn't ask for", "That can wear thin. Do you say so?"),
    ("{person} talked through the whole film", "Ugh, that would drive me mad."),
    ("my {relation} ate the last of my leftovers", "The nerve! Did they own up?"),
    ("{person} left me on read", "That's never a great feeling."),
    ("my {relation} keeps sending me memes at midnight", "Ha. Do you send any back?"),
    ("{person} cancelled our plans at the last minute", "That's disappointing. Did they say why?"),
    ("my {relation} dropped by unannounced", "A nice surprise or an awkward one?"),
    ("{person} made me laugh so hard today", "Love that. What did they say?"),
    ("finally patched things up with my {relation}", "I'm glad. That must be a relief."),
    ("had a big argument with {person}", "I'm sorry. Do you want to talk about it?"),
    ("my {relation} sent me a photo from their holiday", "Nice! Where are they?"),
    ("{person} cooked dinner for everyone tonight", "That's kind of them. Was it good?"),
    ("my {relation} gave me a lift to work", "Handy. That's a nice favour."),
    ("{person} lent me a book", "Is it any good so far?"),
    ("my {relation} came round to watch the match", "Who were you rooting for?"),
    ("{person} helped me fix my bike", "Nice. Is it riding well now?"),
    ("i miss my {relation}", "That's hard. When did you last see them?"),
    ("{person} really gets on my nerves sometimes", "What do they do that bugs you?"),
    ("i'm a bit worried about my {relation}", "What's worrying you?"),
    ("{person} is the funniest person i know", "They sound like great company."),
    ("i feel bad about how i treated my {relation}", "It's good you're thinking about it."),
    ("{person} always knows how to cheer me up", "Everyone needs someone like that."),
    ("things are better between me and my {relation}", "That's good to hear."),
    ("i keep thinking about what {person} said", "It stuck with you. What did they say?"),
    ("my {relation} is nervous about tomorrow", "Fingers crossed for them."),
    ("{person} is going through a hard time", "I'm sorry to hear that. Can you help at all?"),
)
