from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

Ownership = Literal['NEW','REVIEW','TRANSFER','MASTERY']

@dataclass(frozen=True)
class PlanLesson:
    section: int
    order: int
    lesson_id: str
    title: str
    intent: str
    mapped_targets: tuple[str, ...]

@dataclass(frozen=True)
class OwnedTarget:
    sk: str
    uk: str
    status: Ownership

@dataclass(frozen=True)
class LessonCopy:
    title_uk: str
    intent_uk: str
    target_uk: tuple[str, ...]
