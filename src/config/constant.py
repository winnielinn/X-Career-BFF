from enum import Enum


class InterestCategory(Enum):
    INTERESTED_POSITION = 'interested_position'
    SKILL = 'skill'
    TOPIC = 'topic'


class ProfessionCategory(Enum):
    EXPERTISE = 'expertise'
    INDUSTRY = 'industry'


class ExperienceCategory(Enum):
    WORK = 'work'
    EDUCATION = 'education'
    LINK = 'link'


class ScheduleType(Enum):
    ALLOW = 'allow'
    FORBIDDEN = 'forbidden'
