"""An independent test pool, written by a fresh agent from a brief, sealed like ``heldout``.

No one on the project read it before the final runs (RECORDS R-039). It shares no people,
relations, values or subjects with the other pools, which a test enforces. Read it only with
``--final``.
"""

# ruff: noqa: E501  (written text, kept as its author wrote it)

from aya_retrieval.pools import FactTemplate, Pool, SmallTalkMood

INDEPENDENT = Pool(
    people=(
        "Imogen",
        "Rafael",
        "Theo",
        "Saoirse",
        "Bastian",
        "Leila",
        "Quentin",
        "Marisol",
        "Ezra",
        "Ottilie",
        "Jasper",
        "Niamh",
    ),
    relations=(
        "landlady",
        "flatmate",
        "stepdad",
        "godmother",
        "grandad",
        "physio",
        "hairdresser",
        "bandmate",
        "choirmate",
        "stepson",
    ),
    facts={
        "food_reaction": FactTemplate(
            values=("cashews", "almonds", "mango", "eggplant", "pistachios", "lupin"),
            statement=(
                "so the whole dinner thing got cancelled which honestly fine, but the reason is {person} "
                "ended up in urgent care again, yeah my {relation}, turns out the sauce had {value} in it "
                "and nobody checked, swelled right up, they're ok now but wow what a night"
            ),
            same_words="wait what was {person} allergic to again",
            new_words="whats the thing my {relation} cant eat without puffing up like a balloon",
            indirect="ok i totally forgot what sets my {relation} off food wise and i'm meant to cook for them sunday",
            confirm="did i ever mention what my {relation} has to stay away from at restaurants",
            query="{who} allergic food reaction",
            answer="{person}, your {relation}, is allergic to {value}.",
        ),
        "puppy_name": FactTemplate(
            values=("Pudding", "Bramble", "Toffee", "Nutmeg", "Crumble", "Muffin"),
            statement=(
                "anyway after all that rain i walked past the park and guess who's out there throwing a "
                "frisbee, {person} obviously, and the new puppy my {relation} got is called {value} and it "
                "kept stealing other people's shoes, i nearly died laughing"
            ),
            same_words="hey whats the name of {person}'s dog",
            new_words="what did my {relation} end up calling the little furball",
            indirect="i keep forgetting what my {relation} named that new pup and it's getting awkward",
            confirm="did i ever tell you what my {relation} called their puppy",
            query="{who} dog puppy name",
            answer="{person}'s puppy is called {value}.",
        ),
        "vehicle": FactTemplate(
            values=(
                "silver Prius",
                "black Jetta",
                "white Mazda",
                "grey Outback",
                "blue Fiesta",
                "green Mini",
            ),
            statement=(
                "work was dead so i left early, popped into the garage for my tyres, and who's at the next "
                "bay but my {relation}, picking up a {value} they just bought second hand, {person} "
                "seemed weirdly proud of it tbh"
            ),
            same_words="what does {person} drive these days",
            new_words="what's my {relation} rolling around in now, the one they got second hand",
            indirect="so i forgot what my {relation} bought and now i cant spot them in the pickup line lol",
            confirm="did i ever say what my {relation} picked up at that garage",
            query="{who} bought car second hand",
            answer="{person} drives a {value}.",
        ),
        "occupation": FactTemplate(
            values=(
                "optometrist",
                "locksmith",
                "pharmacist",
                "dental hygienist",
                "air traffic controller",
                "sommelier",
            ),
            statement=(
                "big catch up at the cafe today, the barista remembered my order which was nice, and "
                "{person} was there too, they finally got hired as a {value} after all those interviews, "
                "my {relation} is over the moon and wont shut up about the training"
            ),
            same_words="what does {person} do for work now",
            new_words="what did my {relation} finally get hired as after all those interviews",
            indirect="honestly forgot what my {relation} does all day now and they'll ask if i remember",
            confirm="did i ever mention the new gig my {relation} landed",
            query="{who} new job hired as",
            answer="{person} works as a {value}.",
        ),
        "move": FactTemplate(
            values=("Ljubljana", "Tallinn", "Krakow", "Gdansk", "Bilbao", "Valletta"),
            statement=(
                "the farewell drinks went late, my feet are killing me, but it's real now, my {relation} "
                "is packing up the whole flat and moving to {value} next month, {person} says the rent "
                "is half of here so who can blame them"
            ),
            same_words="where's {person} moving to again",
            new_words="which city is my {relation} relocating to, the cheap rent one",
            indirect="i forgot where my {relation} is heading next month and i'm supposed to help pack",
            confirm="did i ever tell you where my {relation} is moving",
            query="{who} moving city next month",
            answer="{person} is moving to {value}.",
        ),
        "music_played": FactTemplate(
            values=("bassoon", "clarinet", "mandolin", "viola", "flute", "French horn"),
            statement=(
                "so the community hall had that open evening, too many folding chairs and terrible tea, "
                "and {person} got up on stage and played the {value} like a pro, i never knew my "
                "{relation} had it in them, everyone clapped for ages"
            ),
            same_words="what does {person} play again",
            new_words="what was my {relation} making all that noise with up on the stage at the hall",
            indirect="i forgot what my {relation} was playing that night and they keep bringing it up",
            confirm="did i ever mention what my {relation} played at the open evening",
            query="{who} played on stage music",
            answer="{person} plays the {value}.",
        ),
    },
    subjects=(
        "the leaky tap",
        "my umbrella",
        "the crossword",
        "my sourdough starter",
        "the doorbell",
        "the microwave",
        "my wallet",
        "the school run",
        "my houseplants",
        "the noisy pipes",
        "the smoke alarm",
        "my alarm clock",
        "the window blinds",
        "the shower",
        "my sunglasses",
        "my backpack",
        "the train strike",
        "my haircut",
        "the jigsaw",
        "the roadworks",
        "my lunchbox",
        "the duvet",
        "the curtains",
        "my socks",
        "the lightbulb",
        "the ice cream van",
        "my inbox",
        "the heatwave",
        "the pothole",
        "my running shoes",
        "the bike lane",
        "the mattress",
        "my notebook",
        "the bathroom scale",
        "the hoover",
    ),
    moods=(
        SmallTalkMood(
            user_lines=(
                "ugh {subject} is acting up again",
                "cant believe {subject} chose today of all days",
                "so {subject} has officially given up on me",
                "{subject} is driving me up the wall honestly",
                "not to complain but {subject} is the worst right now",
            ),
            replies=(
                "oh no, that sounds really annoying",
                "ugh, the timing on these things is always terrible",
                "that's rough, hope it sorts itself out soon",
                "sounds like a proper headache, sorry",
                "oof, {subject} again? what a pain",
                "honestly that would wind me up too",
                "classic, it always goes wrong when you need it",
                "ah man, want to vent about it?",
                "that's so frustrating, i'm sorry",
                "ugh, some days nothing cooperates",
                "hang in there, it'll calm down",
                "yikes, that's a lot to deal with",
            ),
        ),
        SmallTalkMood(
            user_lines=(
                "finally sorted {subject} this morning",
                "small win today, {subject} is all good now",
                "weirdly happy about {subject} today",
                "ok {subject} actually went fine for once",
                "honestly {subject} made my morning lol",
            ),
            replies=(
                "nice, love a small win",
                "ha, that's great to hear",
                "good stuff, sometimes the little things count",
                "glad that went your way for once",
                "that's lovely, enjoy it",
                "yes! a good start to the day",
                "love that for you",
                "see, things do work out sometimes",
                "nice one, you earned that",
                "ha, celebrate the tiny victories",
                "oh good, one less thing to worry about",
                "that's the kind of news i like",
            ),
        ),
        SmallTalkMood(
            user_lines=(
                "random thought but {subject} always reminds me of being a kid",
                "was thinking about {subject} on the walk home",
                "do you ever just stare at {subject} and zone out",
                "{subject} got me thinking about how fast the year went",
                "kinda nostalgic about {subject} today no idea why",
            ),
            replies=(
                "funny how ordinary stuff can do that",
                "ha, i get that, little things stick with you",
                "that's a nice thought actually",
                "the year really has flown by",
                "i love those random moments",
                "it's odd what sets the memories off",
                "ha, i do that all the time",
                "sounds like a thoughtful sort of day",
                "time is strange like that",
                "aw, that's kind of sweet",
                "ha, deep thoughts on a weekday",
                "i know exactly that feeling",
            ),
        ),
    ),
    acknowledgements=(
        "oh nice, thanks for telling me",
        "ha, good to know",
        "wow, that's big news",
        "noted, sounds like a lot going on",
        "oh fun, love hearing that",
        "huh, didn't see that coming",
        "aw that's sweet",
        "oh nice one",
        "ooh, how exciting",
        "ha, that's so them",
        "oh really, since when",
        "good for them honestly",
        "huh, interesting",
        "well that's a turn up",
        "oh cool, glad you told me",
        "ha, love that",
        "oh wow, ok then",
        "right, makes sense",
    ),
    statements=(
        (
            "{person} my {relation} is coming round saturday to help paint the hallway",
            "nice, extra hands make that go way quicker",
        ),
        (
            "had a long phone call with my {relation} last night, mostly about nothing",
            "those are sometimes the best calls",
        ),
        ("{person} sent me the funniest meme this morning", "ha, a good meme can save a whole day"),
        (
            "my {relation} keeps saying we should do a picnic before it gets cold",
            "you should, the weather won't hold forever",
        ),
        (
            "bumped into {person} at the shops, we chatted for ages by the bread",
            "classic, you pop out for one thing and lose an hour",
        ),
        (
            "{person} my {relation} is finally on holiday this week, so jealous",
            "hope they get some proper rest",
        ),
        (
            "{person} keeps texting me pictures of clouds for some reason",
            "ha, honestly that sounds relaxing",
        ),
        ("my {relation} said hi by the way", "aw, say hi back from me"),
        (
            "going for a walk with {person} later if the rain holds off",
            "fingers crossed for dry skies",
        ),
        (
            "my {relation} and i watched a terrible film last night, loved it",
            "the worst films are often the most fun",
        ),
        (
            "{person} is doing a big spring clean and roped me in",
            "at least it goes faster with two",
        ),
        (
            "my {relation} wants to start a book club and i'm not sure i'll keep up",
            "you could just go for the snacks at first",
        ),
    ),
    unknown_replies=(
        "hmm, i don't think you've ever told me that",
        "you haven't mentioned that to me as far as i know",
        "i don't have that one, you never said",
        "that hasn't come up between us, i think",
    ),
)
