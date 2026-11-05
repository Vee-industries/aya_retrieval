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

# Fix 18 (R-083). Chat lines that name a train fact type's topic in passing, without asking about it
# or stating a value: three per type, one good news, one complaint, one neutral. Written to a recipe
# recorded before the build, after a chat line naming a fact type was read as a question (R-082).
MORE_CHAT_FACTS: dict[str, tuple[tuple[str, str], ...]] = {
    "animals": (
        ("{person} says the animals next door finally settled down", "Peace at last."),
        ("my {relation} is fed up with the animals getting out again", "That sounds like a chore."),
        ("{person} spent the morning feeding the animals", "That sounds like a peaceful start."),
    ),
    "baby": (
        ("my {relation} sent me a video of the baby laughing", "That must have made your day."),
        ("{person} says the baby kept the whole house awake", "Oof, everyone must be shattered."),
        ("my {relation} is babysitting all weekend", "That's a full weekend for them."),
    ),
    "band": (
        ("{person} says their band finally got a proper gig", "That's exciting for them."),
        ("my {relation} is annoyed the band keeps skipping rehearsal", "That would wear thin."),
        ("{person} was at band practice till late", "A long night, then."),
    ),
    "birth": (
        ("my {relation} found the hospital bracelet from when they were born", "What a find."),
        ("{person} hates being reminded what year they were born", "Ha, a sore spot then."),
        ("my {relation} was born in the same hospital as me", "That's a funny coincidence."),
    ),
    "boat": (
        ("{person} took me out on the boat and the water was perfect", "That sounds lovely."),
        ("my {relation} says the boat engine died again", "That's a pain."),
        ("{person} is spending the weekend fixing up the boat", "A busy weekend, then."),
    ),
    "car": (
        ("my {relation} finally got the car back from the garage", "That must be a relief."),
        ("{person} is furious someone dented the car", "That's so annoying."),
        ("my {relation} lent me the car for the afternoon", "That was good of them."),
    ),
    "cat": (
        ("{person} says the kitten has learned to open doors", "Ha, trouble ahead."),
        ("my {relation} is cross the cat knocked over a plant", "Cats will be cats."),
        ("{person} was up early because the cat wanted breakfast", "The cat runs that house."),
    ),
    "city": (
        ("my {relation} loves the new city so far", "That's great to hear."),
        ("{person} is finding the city exhausting", "Big places can wear you out."),
        ("my {relation} keeps sending me pictures of the city at night", "They sound settled."),
    ),
    "coffee": (
        ("{person} brought me a coffee without being asked", "That's a kind thing to do."),
        ("my {relation} spilled coffee all over their laptop", "Oh no. Is the laptop okay?"),
        ("{person} and i sat over coffee for ages", "Sounds like a good catch-up."),
    ),
    "dog": (
        ("my {relation} says the dog finally learned to sit", "Good dog! That's progress."),
        ("{person} is worn out from the dog barking all night", "That sounds exhausting."),
        ("my {relation} took the dog to the beach", "I bet the dog loved that."),
    ),
    "festival": (
        ("{person} came back from the festival buzzing", "Sounds like a great time."),
        ("my {relation} says the festival was a mud bath", "That sounds grim."),
        ("{person} is still unpacking after the festival", "That always takes a while."),
    ),
    "floor": (
        ("my {relation} loves the view from their floor", "That's a nice perk."),
        ("{person} is sick of the lift breaking on their floor", "Stairs every day? Rough."),
        ("my {relation} says the neighbours on their floor are friendly", "That helps."),
    ),
    "genre": (
        ("{person} finished the first draft of their novel", "That's a big milestone."),
        ("my {relation} is stuck on a chapter of their novel", "Frustrating. It'll come."),
        ("{person} was reading their novel out loud to me", "How did it sound?"),
    ),
    "hobby": (
        ("my {relation} is loving their new hobby", "That's good to hear."),
        ("{person} spent a fortune on hobby gear and regrets it", "Ouch. That stings."),
        ("my {relation} talks about their hobby nonstop", "They sound hooked."),
    ),
    "injury": (
        ("{person} got the all clear after their injury", "That's great news."),
        ("my {relation} is grumpy about being laid up with the injury", "Healing takes patience."),
        ("{person} has physio twice a week for the injury", "That's a lot of appointments."),
    ),
    "job": (
        ("my {relation} is really enjoying the new job", "That's great to hear."),
        ("{person} says the job is wearing them down", "That sounds tough."),
        ("my {relation} had a long day at the job", "They'll be glad to rest."),
    ),
    "motorbike": (
        ("{person} took the motorbike out for the first sunny ride", "Sounds like a good day."),
        ("my {relation} says the motorbike won't start", "Annoying. Hope it's simple."),
        ("{person} is cleaning the motorbike in the driveway", "A tidy weekend job."),
    ),
    "paint": (
        ("my {relation} loves how the fresh paint turned out", "That must look great."),
        ("{person} got paint all over the carpet", "Oh no. Will it come out?"),
        ("my {relation} spent the weekend choosing paint", "That can take ages."),
    ),
    "phone": (
        ("{person} is thrilled with the new phone", "Nice upgrade."),
        ("my {relation} cracked their phone screen again", "Oh no, not again."),
        ("{person} was glued to the phone all evening", "Something going on?"),
    ),
    "prize": (
        ("my {relation} can't believe they won a prize", "What a nice surprise."),
        ("{person} says the prize is taking up the whole garage", "Ha, a mixed blessing."),
        (
            "my {relation} entered a raffle for a prize at the school fair",
            "Fingers crossed for them.",
        ),
    ),
    "promotion": (
        ("{person} is over the moon about the promotion", "That's brilliant news."),
        ("my {relation} says the promotion came with far too many meetings", "That's the catch."),
        ("{person} starts the new role after the promotion next week", "A fresh start."),
    ),
    "race": (
        ("my {relation} beat their best time in the race", "That's a great result."),
        ("{person} is limping after the race", "Ouch. Hope they rest up."),
        ("my {relation} is training for another race", "They're keen."),
    ),
    "shop": (
        ("{person} says the shop had its busiest day yet", "That's great for them."),
        ("my {relation} is stressed about the rent on the shop", "That's a real worry."),
        ("{person} was stocking shelves at the shop all morning", "A busy morning."),
    ),
    "street": (
        ("my {relation} says their street threw a lovely block party", "That sounds fun."),
        ("{person} is annoyed about the roadworks on their street", "That's a nuisance."),
        ("my {relation} walked me down their street to show me around", "Nice to see it."),
    ),
    "subject": (
        ("{person} says the class finally got the hang of the topic", "That must feel good."),
        ("my {relation} is buried in marking for their class", "A long night, then."),
        ("{person} is planning lessons for their class next term", "Busy, then."),
    ),
}

# Fix 18's control (R-083): the same moods and placeholder split, naming none of the train fact
# types' topics, so a change from adding rows can be told from a change from the fact words.
MORE_CHAT_PLAIN: tuple[tuple[str, str], ...] = (
    ("{person} says the weather finally turned nice", "Good, about time."),
    ("my {relation} is fed up with the rain", "It's been a lot of rain."),
    ("{person} spent the morning tidying up", "A productive start."),
    ("my {relation} sent me a funny voice note", "Ha, what did it say?"),
    ("{person} says the neighbours kept them up", "That sounds exhausting."),
    ("my {relation} is staying in tonight", "A quiet night sounds good."),
    ("{person} finally finished that jigsaw", "Satisfying!"),
    ("my {relation} is annoyed the bus was late again", "That would get to anyone."),
    ("{person} was out in the garden all day", "Sounds like a nice day."),
    ("my {relation} got a lovely letter in the post", "That's a nice surprise."),
    ("{person} is sick of the noise from upstairs", "That would drive me mad."),
    ("my {relation} cooked a big pot of stew", "Sounds hearty."),
    ("{person} was thrilled to see an old friend", "That must have been nice."),
    ("my {relation} is cross about a parking ticket", "That's so annoying."),
    ("{person} spent the evening watching old films", "Sounds cosy."),
    ("my {relation} says the holiday was perfect", "That's lovely to hear."),
    ("{person} missed the train by a minute", "So frustrating."),
    ("my {relation} is sorting out the attic", "That's a big job."),
    ("{person} got a really kind compliment today", "That's nice to hear."),
    ("my {relation} is tired of the long commute", "That's draining."),
    ("{person} went for a swim before work", "That's a good start to a day."),
    ("my {relation} finally fixed the leaky tap", "Nice, one less thing."),
    ("{person} burnt the toast again", "Happens to the best of us."),
    ("my {relation} is having a lazy morning", "Sounds well earned."),
    ("{person} was in a great mood at lunch", "Nice. Something good happen?"),
    ("my {relation} is grumbling about the heating bill", "Bills are brutal lately."),
    ("{person} is clearing out the wardrobe", "That always feels good after."),
    ("my {relation} loved the concert last night", "Sounds like a good night."),
    ("{person} says the queue at the post office was endless", "Ugh, what a wait."),
    ("my {relation} is learning to juggle", "Fun. How is it going?"),
    ("{person} found an old photo album", "That's a nice find."),
    ("my {relation} says the meeting ran two hours over", "That sounds draining."),
    ("{person} went for a long drive to clear their head", "Sometimes that helps."),
    ("my {relation} is excited about the long weekend", "Any plans?"),
    ("{person} lost their keys again", "Oh no. Did they find them?"),
    ("my {relation} is repainting the fence with a friend", "A good weekend job."),
    ("{person} says the new neighbours brought biscuits", "That's a kind welcome."),
    ("my {relation} is stuck at home with a cold", "Poor thing. Hope they feel better."),
    ("{person} is reorganising the kitchen cupboards", "That's satisfying work."),
    ("my {relation} got tickets to the theatre", "That sounds like fun."),
    ("{person} is frustrated with the internet being slow", "That's maddening."),
    ("my {relation} walked by the river this morning", "That sounds peaceful."),
    ("{person} finally got some sleep", "Good, they needed it."),
    ("my {relation} says the dentist visit went badly", "Ouch. Sorry to hear."),
    ("{person} is helping a friend move house", "That's good of them."),
    ("my {relation} had a really good day", "Love that."),
    ("{person} says the roof is leaking", "That's stressful."),
    ("my {relation} is planting bulbs for the spring", "That'll look lovely."),
    ("{person} won the pub quiz", "Brilliant!"),
    ("my {relation} is worried about the exam results", "Waiting is the worst part."),
    ("{person} went to bed early", "Sounds sensible."),
    ("my {relation} says the new café is great", "Good to know."),
    ("{person} is annoyed the shower is cold again", "A rough start to a day."),
    ("my {relation} is knitting a scarf", "Cosy project."),
    ("{person} had the best sandwich of their life", "High praise!"),
    ("my {relation} got soaked on the way home", "Oh no. Did they dry off?"),
    ("{person} is catching up on emails", "Not the most fun job."),
    ("my {relation} is proud of the garden this year", "They should be."),
    ("{person} says the hotel was awful", "That's disappointing."),
    ("my {relation} is watching the match tonight", "Hope their side wins."),
    ("{person} bumped into a teacher from school", "Small world!"),
    ("my {relation} is fed up with the washing machine", "Appliances pick their moment."),
    ("{person} spent the day at the museum", "Sounds like a good day out."),
    ("my {relation} cleared the snow from the drive", "That's hard work."),
    ("{person} is making salads for the week", "Smart planning."),
    ("my {relation} laughed at my terrible joke", "Ha, a good audience."),
    ("{person} is cross they missed the delivery", "That's annoying."),
    ("my {relation} is sorting old receipts", "Thrilling stuff."),
    ("{person} feels great after the weekend away", "Sounds like it did them good."),
    ("my {relation} says the printer jammed all morning", "Printers are the worst."),
    ("{person} is reading on the balcony", "Sounds relaxing."),
    ("my {relation} heard back about the flat and it's good news", "That's great!"),
    ("{person} hates the new timetable", "Change is hard."),
    ("my {relation} is having friends round tonight", "Sounds like fun."),
    ("{person} stayed up too late again", "They'll feel it tomorrow."),
)
