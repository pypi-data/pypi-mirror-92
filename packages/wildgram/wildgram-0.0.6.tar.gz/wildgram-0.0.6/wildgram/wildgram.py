import regex as re
import string
import os


TOPICWORDS = [
"no",
"not",
"nor",
"due to",
"secondary to",
"s/p",
"ruled out",
"w/o",
"c/b",
"complicated by",
"experience",
"become",
"becomes",
"if",
"denies",
"denied",
"suggests",
"suggest",
"suggested",
"reveal",
"revealed",
"report",
"reported",
"h/o",
"\d+",
"\d+\.\d+",
"will"
"don't",
"aren't",
"couldn't",
"didn't",
"doesn't",
"hadn't",
"hasn't",
"haven't",
"isn't",
"shouldn't",
"wasn't",
"weren't",
"won't",
"wouldn't"
]

STOPWORDS = ['i',
'just',
'should',
"should've",
'can',
'me',
'my',
'myself',
'we',
'our',
'ours',
'ourselves',
'you',
"you're",
"you've",
"you'll",
"you'd",
'your',
'yours',
'yourself',
'yourselves',
'he',
'him',
'his',
'himself',
'she',
"she's",
'her',
'hers',
'herself',
'it',
"it's",
'its',
'itself',
'they',
'them',
'their',
'theirs',
'themselves',
'what',
'which',
'who',
'whom',
'this',
'that',
"that'll",
'these',
'those',
'am',
'is',
'are',
'was',
'were',
'be',
'been',
'being',
'have',
'has',
'had',
'having',
'do',
'does',
'did',
'doing',
'a',
'an',
'the',
'and',
'but',
'if',
'or',
'because',
'as',
'until',
'while',
'at',
'by',
'for',
'with',
'about',
'against',
'between',
'into',
'through',
'during',
'before',
'after',
'above',
'below',
'to',
'from',
'up',
'down',
'in',
'out',
'on',
'off',
'over',
'under',
'again',
'further',
'then',
'once',
'here',
'there',
'when',
'where',
'why',
'how',
'all',
'any',
'both',
'each',
'few',
'more',
'most',
'other',
'some',
'such',
'only',
'own',
'same',
'so',
'than',
'too',
'very',
"vs",
"came back",
"verses",
"could",
"including",
"indicate",
"since",
"towards",
"toward",
"developed",
"develop",
"described",
"describe",
"status",
"represented",
"represent",
"include",
"included",
"includes"
]

def figureOutRegex(stopwords, topicwords, size=2):
    punc = [x for x in string.punctuation]
    regex = '\n|[\s' + "|\\".join(punc)+ ']{'+ str(size)+',}'

    topics = "|".join(["(\s|^)"+stop+"(\s|$)" for stop in topicwords])
    stops = "|".join(["(\s|^)"+stop+"(\s|$)" for stop in stopwords])

    if len(topics) != 0:
        regex = topics +"|" + regex
    if len(stops) != 0:
        regex = stops+'|'+regex

    regex = "("+regex+")"
    prog = re.compile(regex)
    return prog, topics

def splitTextApartByProg(prog, text):
    prev = 0
    count = 0
    ranges = []
    for match in prog.finditer(text.lower(),overlapped=True):
        if match.start() > prev:
            ranges.append((prev, match.start()))
        prev = match.end()
    if len(text) > prev:
        ranges.append((prev, len(text)))
    return ranges

def add1gram(ranges, prog1gram, text):
    if len(ranges) == 0:
        return ranges
    rn = splitTextApartByProg(prog1gram, text[ranges[-1][0]:ranges[-1][1]])
    if len(rn) == 1:
        return ranges
    fin = ranges[-1]
    for r in rn:
        ranges.append((fin[0]+r[0], fin[0]+r[1]))
    return ranges

def wildgram(text, stopwords=STOPWORDS, topicwords=TOPICWORDS, include1gram=False):
    # corner case for inappropriate input
    if not isinstance(text, str):
        raise Exception("What you just gave wildgram isn't a string, mate.")
    # if its just whitespace
    if text.isspace():
        return [], []

    prog,topics = figureOutRegex(stopwords, topicwords)
    if include1gram:
        punc = [x for x in string.punctuation]
        regex = '[\s' + "|\\".join(punc)+ ']{'+ str(1)+',}'
        prog1gram = re.compile(regex)

    prev = 0
    count = 0
    ranges = []
    for match in prog.finditer(text.lower(),overlapped=True):
        if match.start() > prev:
            ranges.append((prev, match.start()))
            # this nonsense deals with 1grams
            if include1gram:
                ranges = add1gram(ranges, prog1gram, text)
            #    print(ranges, "hello")
        prev = match.end()



        # all of this nonsense deals with topic changing words
        if len(topics) == 0:
            continue
        if re.match("("+topics+")", match.group(0)):
            start = match.start()
            end = match.end()
            if text[match.start()].isspace():
                start = start + 1
            if text[match.end()-1].isspace():
                end = end -1
            ranges.append((start, end))
            if include1gram:
                ranges =add1gram(ranges, prog1gram, text)




    if len(text) > prev:
        ranges.append((prev, len(text)))
        if include1gram:
            ranges =add1gram(ranges, prog1gram, text)

    tokens = []
    for snippet in ranges:
        tokens.append(text[snippet[0]:snippet[1]])


    return tokens, ranges
