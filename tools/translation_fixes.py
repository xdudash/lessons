from __future__ import annotations

import re

EXACT: dict[str, dict[str, str]] = {
    "Що тут сказати найприродніше?": {"en": "What sounds most natural here?", "ru": "Что здесь звучит естественнее всего?"},
    "З’єднай слова або фрази з точними значеннями.": {"en": "Match the words or phrases with their exact meanings.", "ru": "Соедини слова или фразы с точными значениями."},
    "Заповни пропуски словами з банку.": {"en": "Fill in the blanks using the word bank.", "ru": "Заполни пропуски словами из банка."},
    "Склади словацьке речення за українським змістом.": {"en": "Build the Slovak sentence that matches the Ukrainian meaning.", "ru": "Составь словацкое предложение по украинскому смыслу."},
    "Розташуй репліки в логічній послідовності.": {"en": "Put the lines in a logical order.", "ru": "Расположи реплики в логической последовательности."},
    "Обери всі цільові одиниці цього уроку.": {"en": "Select all target items from this lesson.", "ru": "Выбери все целевые единицы этого урока."},
    "Прочитай короткий контекст і знайди точну інформацію.": {"en": "Read the short context and find the exact information.", "ru": "Прочитай короткий контекст и найди точную информацию."},
    "З’єднай цільову одиницю з її значенням.": {"en": "Match the target item with its meaning.", "ru": "Соедини целевую единицу с её значением."},
    "Передай цей зміст словацькою, використавши модель уроку.": {"en": "Express this meaning in Slovak using the lesson pattern.", "ru": "Передай этот смысл по-словацки, используя модель урока."},
    "Перевір кілька тверджень про значення.": {"en": "Check the statements about meaning.", "ru": "Проверь несколько утверждений о значении."},
    "Яка відповідь точно передає потрібний зміст повідомлення?": {"en": "Which answer conveys the intended message accurately?", "ru": "Какой ответ точно передаёт нужный смысл сообщения?"},
    "Розташуй слова в природному порядку.": {"en": "Put the words in a natural order.", "ru": "Расположи слова в естественном порядке."},
}

LEXICAL: dict[str, dict[str, str]] = {
    "як / ніж": {"en": "as / than", "ru": "как / чем"},
    "цікавий": {"en": "interesting", "ru": "интересный"},
    "активний": {"en": "active", "ru": "активный"},
    "веселий": {"en": "cheerful", "ru": "весёлый"},
    "спокійний": {"en": "calm", "ru": "спокойный"},
    "тихий": {"en": "quiet", "ru": "тихий"},
    "лінивий": {"en": "lazy", "ru": "ленивый"},
    "працьовитий": {"en": "hardworking", "ru": "трудолюбивый"},
    "двоюрідний брат": {"en": "cousin", "ru": "двоюродный брат"},
    "одружений": {"en": "married", "ru": "женатый"},
    "іноді": {"en": "sometimes", "ru": "иногда"},
    "часто": {"en": "often", "ru": "часто"},
    "дядько": {"en": "uncle", "ru": "дядя"},
    "менше": {"en": "less", "ru": "меньше"},
    "подруга": {"en": "female friend", "ru": "подруга"},
    "друг": {"en": "friend", "ru": "друг"},
}

MEANING_RE = re.compile(r"^Що означає «([^»]+)»\?$")
CONTEXT_RE = re.compile(r"^Що означає виділена одиниця в контексті: «([^»]+)»\?$")
FILL_RE = re.compile(r"^Впиши словацькою: «([^»]+)»\.$")
TRUE_FALSE_RE = re.compile(r"^Правда чи ні\? «([^»]+)» означає «([^»]+)»\.$")
CHOOSE_RE = re.compile(r"^Обери точну словацьку одиницю для значення «([^»]+)»\.$")
REPLY_RE = re.compile(r"^Яка репліка передає зміст «([^»]+)»\?$")
QUOTE_RE = re.compile(r"«([^»]+)»")
CYR = re.compile(r"[А-Яа-яЁёІіЇїЄєҐґ]")


def lexical(target: str, text: str) -> str | None:
    item = LEXICAL.get(text)
    return item.get(target) if item else None


def fixed_translation(target: str, source: str) -> str | None:
    exact = EXACT.get(source)
    if exact:
        return exact[target]
    m = MEANING_RE.match(source)
    if m and not CYR.search(m.group(1)):
        return f"What does «{m.group(1)}» mean?" if target == "en" else f"Что означает «{m.group(1)}»?"
    m = CONTEXT_RE.match(source)
    if m and not CYR.search(m.group(1)):
        return f"What does the highlighted item mean in context: «{m.group(1)}»?" if target == "en" else f"Что означает выделенная единица в контексте: «{m.group(1)}»?"
    m = FILL_RE.match(source)
    if m and lexical(target, m.group(1)):
        prefix = "Write in Slovak" if target == "en" else "Напиши по-словацки"
        return f"{prefix}: «{lexical(target, m.group(1))}»."
    m = TRUE_FALSE_RE.match(source)
    if m and lexical(target, m.group(2)):
        if target == "en": return f"True or false? «{m.group(1)}» means «{lexical(target, m.group(2))}»."
        return f"Правда или нет? «{m.group(1)}» означает «{lexical(target, m.group(2))}»."
    return None


def _quoted_translation(machine: str) -> str | None:
    q = QUOTE_RE.findall(machine)
    return q[-1] if q else None


def normalize_translation(target: str, source: str, machine: str) -> str:
    fixed = fixed_translation(target, source)
    if fixed: return fixed
    m = FILL_RE.match(source)
    if m:
        inner = lexical(target, m.group(1)) or _quoted_translation(machine)
        if inner:
            prefix = "Write in Slovak" if target == "en" else "Напиши по-словацки"
            return f"{prefix}: «{inner}»."
    m = TRUE_FALSE_RE.match(source)
    if m:
        inner = lexical(target, m.group(2)) or _quoted_translation(machine)
        if inner:
            if target == "en": return f"True or false? «{m.group(1)}» means «{inner}»."
            return f"Правда или нет? «{m.group(1)}» означает «{inner}»."
    m = CHOOSE_RE.match(source)
    if m:
        inner = lexical(target, m.group(1)) or _quoted_translation(machine)
        if inner:
            if target == "en": return f"Choose the exact Slovak item for the meaning «{inner}»."
            return f"Выбери точную словацкую единицу для значения «{inner}»."
    m = REPLY_RE.match(source)
    if m:
        inner = _quoted_translation(machine)
        if inner:
            if target == "en": return f"Which line conveys the meaning «{inner}»?"
            return f"Какая реплика передаёт смысл «{inner}»?"
    return machine
