# Elen Golightly 19.12.25
# making a custom recogniser: dates of birth/death

from presidio_analyzer import Pattern, PatternRecognizer


#identify patterns
date_patterns = [
    Pattern(
        name="dash_date",
        regex=r"\b\d{4}-\d{1,2}-\d{1,2}\b", #xx-xx-yyyy
        score=0.9
    ),
    Pattern(
        name="slash_date",
        regex=r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", #xx/xx/yyyy
        score=0.9
    ),
    Pattern(
        name="yearslash_date",
        regex=r"\b\d{4}/\d{1,2}/\d{1,2}\b", #yyyy/xx/xx
        score=0.9
    ),
    Pattern(
        name="yeardash_date",
        regex=r"\b\d{4}-\d{1,2}-\d{1,2}\b", #yyyy-xx-xx
        score=0.9
    ),
        Pattern(
        name="dot_date",
        regex=r"\b\d{4}.\d{1,2}.\d{1,2}\b", #xx.xx.yyyy
        score=0.9
    ),
    Pattern(
        name="yeardot_date",
        regex=r"\b\d{4}.\d{1,2}.\d{1,2}\b", #yyyy.xx.xx
        score=0.9
    ), 
    Pattern(
        name="dash_shortdate",
        regex=r"\b\d{1,2}-\d{1,2}-\d{1,2}\b", #xx-xx-yy
        score=0.9
    ),
    Pattern(
        name="slash_shortdate",
        regex=r"\b\d{1,2}/\d{1,2}/\d{1,2}\b", #xx/xx/yy
        score=0.9
    ),
    Pattern(
        name="dot_shortdate",
        regex=r"\b\d{1,2}.\d{1,2}.\d{1,2}\b", #xx.xx.yy
        score=0.9
    ),
    Pattern(
        name="yeardash_shortdate",
        regex=r"\b\d{2}-\d{1,2}-\d{1,2}\b", #xx-xx-yy
        score=0.9
    ),
    Pattern(
        name="yearslash_shortdate",
        regex=r"\b\d{2}/\d{1,2}/\d{1,2}\b", #xx/xx/yy
        score=0.9
    ),
    Pattern(
        name="yeardot_shortdate",
        regex=r"\b\d{2}.\d{1,2}.\d{1,2}\b", #xx.xx.yy
        score=0.9
    ),  
    Pattern(
        name="text_month",
        regex = r"""
(?i)                    # case-insensitive
\b                      # word boundary
(?:                     # start first order: Day Month Year
    \d{1,2}             # day
    \s+
    (?:Jan|January|...|Dec|December)
    ,?
    \s+\d{4}
)
|
(?:                     # second order: Month Day Year
    (?:Jan|January|...|Dec|December)
    \s+\d{1,2},?\s+\d{4}
)
|
(?:                     # third order: Year Month Day
    \d{4}\s+(?:Jan|January|...|Dec|December)\s+\d{1,2}
)
\b
""",

        score=0.75
    )
]


#context words
context_words_dobdod = [
    "dob",
    "dod",
    "birth",
    "death"
]


#create pattern recogniser
def get_date_recogniser():
    return PatternRecognizer(
        supported_entity="DOB_DOD_CUSTOM",
        patterns=date_patterns,
        context=context_words_dobdod 
    )
