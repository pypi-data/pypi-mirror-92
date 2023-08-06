# variables


adj_tags = ['JJ', 'JJR', 'JJS']
noun_tags = ['NN', 'NNP', 'NNS', 'NNPS']
verb_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
adverb_tags = ['RB', 'RBR', 'RBS']

# operations
operations = ["dict_replacement", "duplication",
              "punctuations", "punctuation_braces",  
              "random_removal", "split_words",
              "insert_determiner", "change_order",

             ]

# determiners/propositions
determiners = ['a', 'is', 'are', 'an', 'to', 'of', 'on', 'in', 'it',
               'if', 'or', 'was', 'were', 'from', 
              ]

# split words
splitters = {
    "healthcare": "health care",
    "trademark": "trade mark",
    "decision-making": "decision making",
    "health-related": "health related",
    "highlight": "high light",
    "endpoint": "end point",
    "biomarker": "bio marker",
    "without": "with out",
    "meta-analysis": "meta analysis",
    "non-alcoholic": "non alcoholic",
    "understand": "under stand",
    "understood": "under stood",
    "relationship": "relation ship",
    "hypersensitivity": "hyper sensitivity",
    "outcome": "out come",
    "inflammatory": "in flammatory",
    "questionable": "question able",
    "independent": "in dependent",
    "stakeholders": "stake holders",
    "injectable": "inject able",
    "outcomes": "out comes",
    "moderate": "mode rate",
}

splitter_keys = splitters.keys()

# were -> where
# there -> they are

replacements = {
    
    "have": ["has"],
    "has": ["have"],
    "were": ["we are", "we're", "where",],
    "we're": ["were",],
    "where": ["were", "we're", "we are", ],
    "there": ["their", "they're", "they are"],
    "their": ["there", "they're", "they are"],
    "A": ["An", ],
    "An": ["A", ],
    "a": ["an", "as", "are", ],
    "an": ["a", "are", ],
    "its": ["it's", "it is"],
    "it's": ["its"],
    "to": ["too", "on",],
    "too": ["to",],
    "of": ["off",],
    "off": ["of",],
    "once": ["ones", "one's", ],
    "ones": ["once", ],
    "on": ["own", "one"],
    "own": ["on",],
    "effect": ["affect",],
    "affect": ["effect",],
    "effects": ["affects",],
    "affects": ["effects",],
    "by": ["buy", "bye"],
    "buy": ["by", "bye"],
    "here": ["hear", ],
    "hear": ["here", ],
    "this": ["these", ],
    "these": ["this", ],
    "This": ["These", ],
    "These": ["This", ],
    "There": ["Their", ],
    "week": ["weak", ],
    "weak": ["week", ],
    "adopt": ["adept", ],
    "adept": ["adopt", ],
    "except": ["accept", ],

}

replacement_keys = list(replacements.keys())

punctuations = [",", ":", ";", "\'", "-", " ,", " .",
                       " , ", " . ", ", ", ". ", ",.", "..",
                       "...", ".,", "?", " ?"
               ]

punctuation_braces = [')', '(', ' )', ' (', '( ', ') ',
                       ' ( ', ' ) ', ']', '[', ' ]', ' [', '[ ', 
                       '] ', ' [ ', ' ] ', '}', '{', ' }', ' {', 
                       '{ ', '} ', ' { ', ' } ',
                     ]


