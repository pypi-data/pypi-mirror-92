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

JOINERWORDS = [
"of",
"in",
"to"
]

def appendJoiners(matches, ranges, text, joinerwords):
    if len(joinerwords) == 0:
        return ranges
    joiners = "|".join(["(\s|^)"+stop+"(\s|$)" for stop in joinerwords])
    merged = mergeOverlappingTuples(matches)
    for i in range(len(merged)):
        match = merged[i]
        start = 0
        end = len(text)
        if not re.match("("+joiners+")", text[match[0]:match[1]]):
            continue
        if i > 0:
            start = merged[i-1][1]
        if i < len(merged)-1:
            end = merged[i+1][0]

        # must have text before and after it...
        if start != merged[i][0] and end != merged[i][1]:
            ranges.append((start,end))
    return ranges

def mergeOverlappingTuples(matches):
    if len(matches) == 1:
        return matches
    prev = 0
    res = []
    for i in range(len(matches)-1):
        if matches[i][1] >  matches[i+1][0]:
            continue
        res.append((matches[prev][0], matches[i][1]))
        prev = i+1
    if prev < len(matches):
        res.append((matches[prev][0], matches[-1][1]))
    return res


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


def appendMatches(matches, ranges, text):
    prev = 0
    for match in matches:
        if match[0]> prev:
            ranges.append((prev, match[0]))
        prev = match[1]
    if len(text) > prev:
        ranges.append((prev, len(text)))
    return ranges

def getRangesFromIter(matches):
    ranges = []
    for match in matches:
        ranges.append((match.start(), match.end()))
    return ranges

def appendTopics(matches, ranges, text, topics):

    if len(topics) == 0:
        return ranges
    for match in matches:
        if re.match("("+topics+")", text[match[0]:match[1]]):
            start = match[0]
            end = match[1]
            if text[match[0]].isspace():
                start = start + 1
            if text[match[1]-1].isspace():
                end = end -1
            ranges.append((start, end))
    return ranges


def wildgram(text, stopwords=STOPWORDS, topicwords=TOPICWORDS, include1gram=False, joinerwords=JOINERWORDS):
    # corner case for inappropriate input
    if not isinstance(text, str):
        raise Exception("What you just gave wildgram isn't a string, mate.")
    # if its just whitespace
    if text.isspace():
        return [], []

    prog,topics = figureOutRegex(stopwords, topicwords)
    ranges = []
    matches = getRangesFromIter(prog.finditer(text.lower(),overlapped=True))
    ranges = appendMatches(matches, ranges, text)
    ranges = appendTopics(matches, ranges, text, topics)
    ranges =appendJoiners(matches, ranges, text, joinerwords)

    if include1gram:
        prog1gram,_ = figureOutRegex(stopwords,[], 1)
        matches = getRangesFromIter(prog1gram.finditer(text.lower(), overlapped=True))
        ranges = appendMatches(matches, ranges, text)
        ranges =appendJoiners(matches, ranges, text, joinerwords)

    ranges = list(set(ranges))
    ranges =sorted(ranges, key=lambda x: x[0])
    tokens = []
    for snippet in ranges:
        tokens.append(text[snippet[0]:snippet[1]])


    return tokens, ranges
