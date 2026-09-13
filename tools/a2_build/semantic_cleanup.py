from pathlib import Path

PATH = Path('tools/a2_build/semantic_profiles.py')
REPLACEMENTS = {
    'Žiaľ, prídem zajtra namiesto dnes.': ('Žiaľ, prídem zajtra, nie dnes.', 'На жаль, я прийду завтра, не сьогодні.'),
    'Na poslednej zastávke vystúpte a urobte prestup na iný spoj.': ('Na poslednej zastávke vystúpte a prestúpte na iný spoj.', 'На кінцевій зупинці вийдіть і пересядьте на інший рейс.'),
    'Choďte smerom k centru, odtiaľ pokračujte rovno a potom tadiaľ cez námestie.': ('Choďte smerom k centru, odtiaľ pokračujte rovno cez námestie.', 'Ідіть у напрямку центру, звідти продовжуйте прямо через площу.'),
    'Bol som hladný, ale po večeri som sýty; teraz môžem pokojne večerať s rodinou.': ('Bol som hladný, ale po večeri som sýty; teraz môžem pokojne oddychovať.', 'Я був голодний, але після вечері ситий; тепер можу спокійно відпочити.'),
    'Tento je lacnejší, tamten drahší, ale dnes je naň zľava a akcia.': ('Tento je lacnejší, tamten drahší, ale dnes je naň zľava, lebo je v akcii.', 'Цей дешевший, той дорожчий, але сьогодні на нього знижка, бо він в акції.'),
    'Keď bude vybavenie hotové, budem mať všetko vybavené.': ('Keď to vybavím, budem mať všetko hotové.', 'Коли я це владнаю, у мене все буде готово.'),
    'Chcem sa naučiť všetko na úlohu a dostať dobrú známku.': ('Chcem sa naučiť všetko na skúšku a dostať dobrú známku.', 'Я хочу вивчити все до іспиту й отримати добру оцінку.'),
    'V škole aj v práci získavam skúsenosť a mám rôzne povinnosti.': ('V škole aj v práci získavam skúsenosti a mám rôzne povinnosti.', 'У школі й на роботі я здобуваю досвід і маю різні обов’язки.'),
    'Nabudúce môžeme sa stretnúť v sobotu.': ('Nabudúce sa môžeme stretnúť v sobotu.', 'Наступного разу можемо зустрітися в суботу.'),
    'Zajtra snáď budem schopný pracovať; dnes som ešte neschopný práce.': ('Zajtra snáď budem schopný pracovať; dnes ešte nie som schopný pracovať.', 'Сподіваюся, завтра зможу працювати; сьогодні я ще не можу працювати.'),
    'Záleží na situácii; niekedy je skôr lepšia rýchlejšia možnosť.': ('Záleží na situácii; niekedy je lepšia rýchlejšia možnosť.', 'Це залежить від ситуації; іноді кращим є швидший варіант.'),
    'Určite potrebujeme riešenie, nie zlý nápad bez plánu.': ('Určite potrebujeme dobré riešenie a jasný plán.', 'Нам точно потрібне хороше рішення й чіткий план.'),
    'Podľa mňa by som radšej zvolil druhú možnosť.': ('Ja by som radšej zvolil druhú možnosť.', 'Я б радше обрав другий варіант.'),
}


def main() -> None:
    text = PATH.read_text(encoding='utf-8')
    lines = text.splitlines()
    found = set()
    out = []
    for line in lines:
        changed = False
        for old_sk, (new_sk, new_uk) in REPLACEMENTS.items():
            if f"('{old_sk}'," in line:
                indent = line[:len(line) - len(line.lstrip())]
                out.append(f"{indent}('{new_sk}', '{new_uk}'),")
                found.add(old_sk)
                changed = True
                break
        if not changed:
            out.append(line)
    missing = set(REPLACEMENTS) - found
    if missing:
        raise SystemExit(f'missing semantic cleanup targets: {sorted(missing)}')
    PATH.write_text('\n'.join(out) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
