# Elen Golightly 9.3.26
# making a custom recogniser to look for key words in variable labels

from presidio_analyzer import Pattern, PatternRecognizer, AnalyzerEngine

#(?i) makes it case insensitivee
#identify patterns
word_patterns_CUSTOM = [
    Pattern(
        name="name",
        regex =r"(?i)(?:^|\W)name(?:$|\W)",
        score=0.9),
    Pattern(
        name="DOB",
        regex =r"(?i)(?:^|\W)dob(?:$|\W)",
        score=0.9),
    Pattern(
        name="DOD",
        regex =r"(?i)(?:^|\W)dod(?:$|\W)",
        score=0.9),
    Pattern(
        name="age",
        regex =r"(?i)(?:^|[_\W])age(?:$|[_\W])",
        score=0.9),
    Pattern(
        name="job",
        regex =r"(?i)(?:^|\W)job(?:$|\W)",
        score=0.9),
    Pattern(
        name="dob2",
        regex =r"(?i)(?:^|\W)birth(?:$|\W)",
        score=0.9),
    Pattern(
        name="dod2",
        regex =r"(?i)(?:^|\W)death(?:$|\W)",
        score=0.9),
    Pattern(
        name="School",
        regex =r"(?i)(?:^|\W)school(?:$|\W)",
        score=0.9)
]


#create pattern recogniser

class keyword_recogniser(PatternRecognizer):
    def __init__(self):
        super().__init__(supported_entity="KEYWORD_DETECTION", patterns=word_patterns_CUSTOM) 
        
