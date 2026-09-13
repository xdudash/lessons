from __future__ import annotations

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

SAMPLES = [
    "Яка я людина?",
    "Розширюємо опис характеру, особистості та звичок і вчимося порівнювати себе з іншими.",
    "Чудово. Тепер перенеси ці моделі у власні реальні ситуації.",
    "використовувати цільові слова й фрази теми «Яка я людина?»",
    "застосувати їх у реальній мініситуації",
    "Перенесення в реальну ситуацію",
    "Використовуй модель коротко й точно; спочатку зміст, потім форма.",
    "милий",
    "симпатичний",
    "веселий",
    "лінивий",
    "працьовитий",
    "бути таким/такою",
    "Впиши словацькою: «як / ніж».",
    "Що тут сказати найприродніше?",
    "У фразах učím sa, umývam sa, vraciam sa частка sa входить у конструкцію. Український переклад може мати іншу форму.",
    "Одна частотна фраза робить рутину зрозумілою.",
]

MODEL = "facebook/nllb-200-distilled-600M"

def run(target_code: str):
    tok = AutoTokenizer.from_pretrained(MODEL, src_lang="ukr_Cyrl")
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL)
    model.eval()
    bos = tok.convert_tokens_to_ids(target_code)
    with torch.inference_mode():
        inp = tok(SAMPLES, return_tensors="pt", padding=True, truncation=True, max_length=384)
        out = model.generate(**inp, forced_bos_token_id=bos, max_new_tokens=192, num_beams=4)
    return tok.batch_decode(out, skip_special_tokens=True)


def main():
    en = run("eng_Latn")
    ru = run("rus_Cyrl")
    for src, e, r in zip(SAMPLES, en, ru):
        print("UK:", src)
        print("EN:", e)
        print("RU:", r)
        print("---")

if __name__ == "__main__": main()
