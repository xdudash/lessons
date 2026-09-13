from __future__ import annotations

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

UK_SAMPLES = [
    "Яка я людина?",
    "Розширюємо опис характеру, особистості та звичок і вчимося порівнювати себе з іншими.",
    "Чудово. Тепер перенеси ці моделі у власні реальні ситуації.",
    "використовувати цільові слова й фрази теми «Яка я людина?»",
    "застосувати їх у реальній мініситуації",
    "Перенесення в реальну ситуацію",
    "Використовуй модель коротко й точно; спочатку зміст, потім форма.",
    "Що тут сказати найприродніше?",
    "У фразах učím sa, umývam sa, vraciam sa частка sa входить у конструкцію. Український переклад може мати іншу форму.",
]
SK_SAMPLES = ["milý", "sympatický", "veselý", "tichý", "pokojný", "aktívny", "lenivý", "pracovitý", "zaujímavý", "byť taký/á", "učím sa", "teším sa", "stretávam sa", "každý deň"]
MODEL = "facebook/nllb-200-distilled-600M"


def run(samples: list[str], src: str, dst: str):
    tok = AutoTokenizer.from_pretrained(MODEL, src_lang=src)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL)
    model.eval(); bos = tok.convert_tokens_to_ids(dst)
    with torch.inference_mode():
        inp = tok(samples, return_tensors="pt", padding=True, truncation=True, max_length=384)
        out = model.generate(**inp, forced_bos_token_id=bos, max_new_tokens=192, num_beams=4)
    return tok.batch_decode(out, skip_special_tokens=True)


def main():
    en = run(UK_SAMPLES, "ukr_Cyrl", "eng_Latn"); ru = run(UK_SAMPLES, "ukr_Cyrl", "rus_Cyrl")
    for src, e, r in zip(UK_SAMPLES, en, ru): print("UK:",src,"\nEN:",e,"\nRU:",r,"\n---")
    en = run(SK_SAMPLES, "slk_Latn", "eng_Latn"); ru = run(SK_SAMPLES, "slk_Latn", "rus_Cyrl")
    for src, e, r in zip(SK_SAMPLES, en, ru): print("SK:",src,"\nEN:",e,"\nRU:",r,"\n---")

if __name__ == "__main__": main()
