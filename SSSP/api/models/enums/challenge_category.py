from enum import Enum


class ChallengeCategory(str, Enum):
    PWN = "PWN"
    REV = "REV"
    FORENSICS = "FORENSICS"
    WEB = "WEB"
    MISC = "MISC"
