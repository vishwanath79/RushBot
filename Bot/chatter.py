# Natural Language Toolkit: Zen Chatbot
#
# Copyright (C) 2001-2015 NLTK Project
# Author: Amy Holland <amyrh@csse.unimelb.edu.au>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

"""
Zen Chatbot talks in gems of Zen wisdom.

This is a sample conversation with Zen Chatbot:
ZC:    Welcome, my child.
me:    Good afternoon.
ZC:    Ask the question you have come to ask.
me:    How can I achieve enlightenment?
ZC:    How do you suppose?
me:    Through meditation.
ZC:    Form is emptiness, and emptiness form.
me:    How can I empty my mind of worldly troubles?
ZC:    Will an answer to that really help in your search for enlightenment?
me:    Yes.
ZC:    It is better to be right than to be certain.
me:    I seek truth and wisdom.
ZC:    The search for truth is a long journey.
me:    Are you sure?
ZC:    Maybe sure, maybe not sure.


The chatbot structure is based on that of chat.eliza. Thus, it uses
a translation table to convert from question to response
i.e. "I am" --> "you are"

Of course, since Zen Chatbot does not understand the meaning of any words,
responses are very limited. Zen Chatbot will usually answer very vaguely, or
respond to a question by asking a different question, in much the same way
as Eliza.
"""
from __future__ import print_function

from nltk.chat.util import Chat, reflections

# responses are matched top to bottom, so non-specific matches occur later
# for each match, a list of possible responses is provided
responses = (

# Zen Chatbot opens with the line "Welcome, my child." The usual
# response will be a greeting problem: 'good' matches "good morning",
# "good day" etc, but also "good grief!"  and other sentences starting
# with the word 'good' that may not be a greeting
#
    (r'(hello(.*))|(good [a-zA-Z]+)',
    ( "Tell me something, mister",
      "You better do some talkin' Or you better do some walkin' now",
      "We are strangers to each other",
      "I feel the sense of possibilities")),


# "I need" and "I want" can be followed by a thing (eg 'help')
# or an action (eg 'to see you')
#
# This is a problem with this style of response -
# person:    "I need you"
# chatbot:    "me can be achieved by hard work and dedication of the mind"
# i.e. 'you' is not really a thing that can be mapped this way, so this
# interpretation only makes sense for some inputs
#
    (r'i need (.*)',
    ( "Everybody need reverse polarity.",
      "Well, I need what keeps a young man alive",
      "We have no need for ancient ways.")),

    (r'i want (.*)',
    ( "Know your place in life is where you want to be",
      "No one wants to make a terrible choice",
      "Overwhelmed by everything, But wanting more so much-")),


# why questions are separated into three types:
# "why..I"     e.g. "why am I here?" "Why do I like cake?"
# "why..you"    e.g. "why are you here?" "Why won't you tell me?"
# "why..."    e.g. "Why is the sky blue?"
# problems:
#     person:  "Why can't you tell me?"
#     chatbot: "Are you sure I tell you?"
# - this style works for positives (e.g. "why do you like cake?")
#   but does not work for negatives (e.g. "why don't you like cake?")
    (r'why (.*) i (.*)\?',
    ( "You%1%2?",
      "Why, I've seen it everywhere",
      "I guess that's why they call me",
      "And I'm wond'rin' what you're gonna do"
      "Perhaps you only think you%1%2")),

    (r'why (.*) you(.*)\?',
    ( "Why%1 you%2?",
      "%2 I%1",
      "That's why I'm searchin', that's why I'm lookin'",
      "Why, I've seen it everywhere",
      "Why'd you have to make us so uptight?",
      "I'd surely like to know before it's over",
      "Are you sure I%2?")),

    (r'why (.*)\?',
    ( "I cannot tell you why%1.",
      "That's why I'm searchin', that's why I'm lookin'",
      "Why do you think %1?" )),

# e.g. "are you listening?", "are you a duck"
    (r'are you (.*)\?',
    ( "Maybe%1, maybe not%1.",
      "Are you under the illusion (.*)\?",
      "What are you trying to do?",
      "What's the deal? Spin the wheel.",
      "Whether I am%1 or not is God's business.")),

# e.g. "am I a duck?", "am I going to die?"
    (r'am i (.*)\?',
    ( "Perhaps%1, perhaps not%1.",
      "Keep 'em till the end, Whether woman or man",
      "Whether you are%1 or not is not for me to say.")),

# what questions, e.g. "what time is it?"
# problems:
#     person:  "What do you want?"
#    chatbot: "Seek truth, not what do me want."
    (r'what (.*)\?',
    ( "Seek truth, not what%1.",
      "Well, I need what keeps a young man alive",
      "I'm gonna get the message across to you, Some way, some how",
      "What%1 should not concern you.")),

# how questions, e.g. "how do you do?"
    (r'how (.*)\?',
    ( "Someway Somehow",
      "Never need to wonder how or why.",
      "No flow without the other, Oh but how")),

# can questions, e.g. "can you run?", "can you come over here please?"
    (r'can you (.*)\?',
    ( "Down to Brother can you spare-",
      "Maybe I can%1, and maybe I cannot.",
      "Show me don't tell me, You've figured out the score",
      "Who can you believe?")),

# can questions, e.g. "can I have some cake?", "can I know truth?"
    (r'can i (.*)\?',
    ( "We have no need for ancient ways",
      "If you choose not to decide You still have made a choice",
      "Seek truth and you will know if you can%1.")),

# e.g. "It is raining" - implies the speaker is certain of a fact
    (r'it is (.*)',
    ( "Well, the time is right And it is today",
      "What it is ... well, you're not really sure.")),

# e.g. "is there a doctor in the house?"
    (r'is there (.*)\?',
    ( "There is%1 if you believe there is.",
      "Or is there something more?",
      "It is possible that there is%1.")),

# e.g. "is it possible?", "is this true?"
    (r'is(.*)\?',
    ( "%1 is not relevant.",
      "all for the best, or some bizarre test?",
      "Right to the heart of the matter",
      "So much mind on the matter",
      "I guess it doesn't matter")),

# non-specific question
    (r'(.*)\?',
    ( "Do you think %1?",
      "And simple truths Now we're so involved",
      "Truth is false and logic lost Now the fourth dimension is crossed",
      "Let the love of truth shine clear")),

# expression of hate of form "I hate you" or "Kelly hates cheese"
    (r'(.*) (hate[s]?)|(dislike[s]?)|(don\'t like)(.*)',
    ( "Coal-black eyes shimmering with hate.By-Tor and the Snow Dog",
      "Half the world hates What half the world does every day",
      "Whatever the hopeless may say")),

# statement containing the word 'truth'
    (r'(.*) truth(.*)',
    ( "Dreams of youth And simple truths",
      "'I bring Truth and Understanding I bring Wit and Wisdom fair",
      "Any escape might help to smooth The unattractive truth")),

# desire to do an action
# e.g. "I want to go shopping"
    (r'i want to (.*)',
    ( "I just want to find out, baby...",
      "I want to be king now not just one more pawn",
      "You may have to %1.")),

# desire for an object
# e.g. "I want a pony"
    (r'i want (.*)',
    ( "Does your heart truly desire %1?",
      "Some will sell their dreams for small desires Or lose the race to rats",
      "Dreams transport desires Drive you when you're down",
      "I can learn to compromise Anything but my desires",
      "his mind is not for rent To any god or government.")),

# e.g. "I can't wait" or "I can't do this"
    (r'i can\'t (.*)',
    ( "Drive like the wind, Straining the limits of machine and man.",
      "Even love must be limited by time",
      "Learning that we're only immortal - For a limited time")),

# "I think.." indicates uncertainty. e.g. "I think so."
# problem: exceptions...
# e.g. "I think, therefore I am"
    (r'i think (.*)',
    ( "Genetic blends With uncertain ends",
     "I feel the day is all uncertainty",
     "A certain degree of imagination A measure of make-believe")),

# "I feel...emotions/sick/light-headed..."
    (r'i feel (.*)',
    ( "Emotional feedback On a timeless wavelength",
      "Emotion transmitted Emotion received",
      "Strong emotions can tip the scale-",
      "Well, do you see, can't you see, what I'm feeling?",
      "Feeling%1 In a state of grace")),


# exclaimation mark indicating emotion
# e.g. "Wow!" or "No!"
    (r'(.*)!',
    ( "I sense that you are feeling emotional today.",
      "Quiet in conscience, calm in their right",
      "Strong emotions can tip the scale-",
      "But the city is calm in this violent sea")),

# because [statement]
# e.g. "because I said so"
    (r'because (.*)',
    ( "Some reasons will never come clear",
      " For to me all things are new",
      "If%1, what can we do?")),

# yes or no - raise an issue of certainty/correctness
    (r'(yes)|(no)',
    ( "Well, you think that you're right",
      "I feel the day is all uncertainty")),

# sentence containing word 'love'
    (r'(.*)love(.*)',
    ( "What you love is your own power",
      "Even joined in bonds of love",
      "Like lovers and heroes, and the restless part of everyone",
      "Love responds to imagination")),

# sentence containing word 'understand' - r
    (r'(.*)understand(.*)',
    ( "I don't understand these boundaries"
      "All this time we're living and trying to understand",
      "Lean not upon your own understanding",
      "Who can face the knowledge")),

# 'I', 'me', 'my' - person is talking about themself.
# this breaks down when words contain these - eg 'Thyme', 'Irish'
    (r'(.*)(me )|( me)|(my)|(mine)|(i)(.*)',
    ( "Selfishness was wrong, Yet it was for me,",
      "Now there's no more Oak oppression",
      "Live for yourself -- there's no one else",
      "Make it easy on yourself")),

# 'you' starting a sentence
# e.g. "you stink!"
    (r'you (.*)',
    ( "You think you're out of sight.",
      "The world calls you away")),

# say goodbye with some extra Zen wisdom.
    (r'exit',
    ( "Fly by night goodbye my dear.",
      "Turn around and say goodbye",
      "Do we have to say goodbye to the past?")),


# say goodbye with some extra Zen wisdom.
    (r'rush is great',
    ( "Geddy is great.",
      "Forever Alex.",
      "Neil. Enough said."
      "\nEvery year is 2112.")),


# fall through case -
# when stumped, respond with generic zen wisdom
#
    (r'(.*)',
    ( "How can anybody be enlightened?",
      "It's action - reaction -Random interaction.",
      "Everybody need reverse polarity.",
      "Conform or be cast out",
      "A spirit with a vision is a dream",
      "Your meters may overload",
      "glittering prizes and endless compromises ",
      "If we keep our pride Though paradise is lost",
      "Forge their creativity, closer to the heart",
      "choose a ready guide in some celestial voice",
      "They call me the workin' man.",
      "So much style without substance So much stuff without style"))
)

zen_chatbot = Chat(responses, reflections)

def zen_chat():
    print('*'*75)
    print("Zen Chatbot!".center(75))
    print('*'*75)
    print('"Look beyond mere words and letters - look into your mind"'.center(75))
    print("* Talk your way to truth with Zen Chatbot.")
    print("* Type 'quit' when you have had enough.")
    print('*'*75)
    print("Welcome, my child.")

    zen_chatbot.converse()

def demo():
    zen_chat()

if __name__ == "__main__":
    demo()
