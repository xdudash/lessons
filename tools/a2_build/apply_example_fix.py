from pathlib import Path

p = Path('tools/a2_build/generator.py')
text = p.read_text(encoding='utf-8')
start = text.index("    if low in special: return special[low]\n")
end = text.index("\n\ndef tok", start)
new = '''    if low in special: return special[low]
    natural={
      'včera':('Včera som bol doma.','Учора я був удома.'),
      'ráno som':('Ráno som bol doma.','Вранці я був удома.'),
      'potom som':('Potom som išiel domov.','Потім я пішов додому.'),
      'večer som':('Večer som bol doma.','Увечері я був удома.'),
      'minulý víkend':('Minulý víkend som bol doma.','Минулі вихідні я був удома.'),
      'minulý týždeň':('Minulý týždeň som veľa pracoval.','Минулого тижня я багато працював.'),
      'často':('Často chodím pešo.','Я часто ходжу пішки.'),
      'vpravo':('Obchod je vpravo.','Магазин праворуч.'),
      'na rohu':('Stretneme sa na rohu.','Зустрінемося на розі.'),
      'aktívny':('Je aktívny.','Він активний.'),
      'skúsenosť':('To je skúsenosť.','Це досвід.'),
      'pôjdem':('Pôjdem zajtra.','Я піду / поїду завтра.'),
    }
    if low in natural: return natural[low]

    uk_low=uk.lower().strip()
    if ' ' in low:
        parts=low.split()
        if uk_low.startswith(('я ','ми ','він ','вона ','вони ')):
            return (punct(cap(sk)), punct(cap(uk)))
        if low.endswith(' sa'):
            if parts[0].endswith('ť'):
                base=sk[:-3]
                return (f'Chcem sa {base}.', f'Я хочу: {uk}.')
            return (punct(cap(sk)), punct(cap(uk)))
        if low.endswith(' si'):
            if parts[0].endswith('ť'):
                base=sk[:-3]
                return (f'Chcem si {base}.', f'Я хочу: {uk}.')
            return (punct(cap(sk)), punct(cap(uk)))
        if parts[0] in {'budem','budeme','budeš','budete','bude','budú'}:
            return (punct(cap(sk)), punct(cap(uk)))
        if low.endswith('ť') and parts[0].endswith('ť'):
            return (f'Chcem {sk}.', f'Я хочу: {uk}.')
        if any(x in {'som','sme','ste','budem','budeme','budeš','budete','mám','máme','musím','musíme','môžem','môžeme','chcem','chceme'} for x in parts):
            return (punct(cap(sk)), punct(cap(uk)))
        return (punct(cap(sk)), punct(cap(uk)))

    if low.endswith('osť'):
        return (f'To je {sk}.', f'Це {uk}.')
    if low in ADVERBS:
        return (f'{cap(sk)} to zvládnem.', f'{cap(uk)} я з цим упораюся.')
    if low in PLURAL_NOUNS:
        return (f'To sú {sk}.', f'Це {uk}.')
    if low in NEUTER_ADJ or low.endswith(('šie','nejšie')):
        return (f'Je to {sk}.', f'Це {uk}.')
    if low.endswith(('ť','ť?')):
        return (f'Chcem {sk}.', f'Я хочу {uk}.')
    if uk_low.startswith(('я ','ми ','він ','вона ','вони ')):
        return (punct(cap(sk)), punct(cap(uk)))
    if low.endswith(('ý','á','í','ny')):
        return (f'Je {sk}.', f'Він {uk}.')
    return (f'To je {sk}.', f'Це {uk}.')
'''
p.write_text(text[:start] + new + text[end:], encoding='utf-8')
