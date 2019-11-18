"""

Context free grammer language parser.
Usage:

parser = LanguageParser()

parser.parseSentence("I saw the dog")

"""
from rbs import FSAHelperFunctions
from rbs import NealCoverFunctions
from rbs import NeuralCognitiveArchitectureBuilder

class LanguageParser:

    def addGrammerRules(self):
        self.narc.addRule(
            "S<NP+VP",
            [
                (True, "NP", ("?np", "?p1", "?p2"),"np"),
                (True, "VP", ("?vp", "?p2", "?p3"),"vp"),
            ],
            [
                ("assert", ("S", (("+", "?np", "?vp"), "?p1","?p3"))),
                ("retract", "np"),
                ("retract", "vp")
            ]
        )

        self.narc.addRule(
            "NP<ART+NOUN",
            [
                (True, "ART", ("?art", "?p1", "?p2"), "art"),
                (True, "NOUN", ("?noun", "?p2", "?p3"), "noun")
            ],
            [
                ("assert", ("NP", (("+", "?art", "?noun"), "?p1","?p3"))),
                ("retract", "art"),
                ("retract", "noun")
            ]
        )

        self.narc.addRule(
            "NP<NAME",
            [
                (True, "NAME", ("?name", "?p1","?p2"), "name")
            ],
            [
                ("assert", ("NP", ("?name", "?p1","?p2"))),
                ("retract", "name"),
            ]
        )

        self.narc.addRule(
            "VP<VERB+NP",
            [
                (True, "VERB", ("?verb", "?p1","?p2"), "verb"),
                (True, "NP", ("?np" ,"?p2", "?p3"), "np")
            ],
            [
                ("assert", ("VP", (("+", "?verb", "?np"), "?p1","?p3"))),
                ("retract", "verb"),
                ("retract", "np")
            ]
        )
    
    def addArt(self, art):
        self.narc.addRule(
            "art-"+art,
            [
                (True, "WORD", (art.upper(), "?s", "?e"), "word")
            ],
            [
                ("assert", ("ART", (art, "?s", "?e"))),
                ("retract", "word")
            ]
        )
    
    def addNounPhrase(self, np):
        self.narc.addRule(
            "nounphrase-"+np,
            [
                (True, "WORD", (np.upper(), "?s", "?e"), "word")
            ],
            [
                ("assert", ("NP", (np, "?s", "?e"))),
                ("retract", "word")
            ]
        )

    def addVerb(self, verb):
        self.narc.addRule(
            "verb-"+verb,
            [
                (True, "WORD", (verb.upper(), "?s", "?e"), "word")
            ],
            [
                ("assert", ("VERB", (verb, "?s", "?e"))),
                ("retract", "word")
            ]
        )

    def addNoun(self, noun):
        self.narc.addRule(
            "noun-"+noun,
            [
                (True, "WORD", (noun.upper(), "?s", "?e"), "word")
            ],
            [
                ("assert", ("NOUN", (noun, "?s", "?e"))),
                ("retract", "word")
            ]
        )

    def addName(self, name):
        self.narc.addRule(
            "name-"+name,
            [
                (True, "WORD", (name.upper(), "?s", "?e"), "word")
            ],
            [
                ("assert", ("NAME", (name, "?s", "?e"))),
                ("retract", "word")
            ]
        )

    def addLexicon(self):
        # Names
        self.addName("John")

        # Noun Phrases
        self.addNounPhrase("I")

        # Verbs
        self.addVerb("Saw")
        self.addVerb("Ate")

        # Articles
        self.addArt("The")
        self.addArt("A")
        self.addArt("An")

        # Nouns
        self.addNoun("Dog")
        self.addNoun("Cat")

    def __init__(self, sim, simulator):
        self.neal = NealCoverFunctions(simulator, sim)
        self.fsa = FSAHelperFunctions(simulator, sim, self.neal)
        self.narc = NeuralCognitiveArchitectureBuilder(simulator, sim, self.fsa, self.neal).build()
        self.addGrammerRules()
        self.addLexicon()
        
    def parseSentence(self, sentence):
        words = sentence.split(" ")
        for i,word in enumerate(words):
            self.narc.addFact("WORD", (word.upper(),i+1,i+2))
