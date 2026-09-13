from __future__ import annotations

from llama_cpp import Llama

MODEL_REPO = "42ailab/TranslateGemma-4B-GGUF"
MODEL_FILE = "translategemma-4b-it-Q4_K_M.gguf"

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
    "Впиши словацькою: «як / ніж».",
    "Що тут сказати найприродніше?",
]


def prompt(text: str, target_code: str, target_name: str) -> str:
    return (
        "<start_of_turn>user\n"
        f"You are a professional Ukrainian (uk) to {target_name} ({target_code}) translator. "
        "Your goal is to accurately convey the meaning and nuances of the original Ukrainian text "
        f"while adhering to {target_name} grammar, vocabulary, and cultural sensitivities.\n"
        f"Produce only the {target_name} translation, without any additional explanations or commentary. "
        f"Please translate the following Ukrainian text into {target_name}:\n\n\n{text}"
        "<end_of_turn>\n<start_of_turn>model\n"
    )


def translate(llm: Llama, text: str, target_code: str, target_name: str) -> str:
    response = llm(
        prompt(text, target_code, target_name),
        max_tokens=160,
        temperature=0,
        top_p=1,
        stop=["<end_of_turn>"],
        echo=False,
    )
    return response["choices"][0]["text"].strip()


def main() -> None:
    llm = Llama.from_pretrained(
        repo_id=MODEL_REPO,
        filename=MODEL_FILE,
        n_ctx=2048,
        n_threads=2,
        verbose=False,
    )
    for source in SAMPLES:
        en = translate(llm, source, "en", "English")
        ru = translate(llm, source, "ru", "Russian")
        print("UK:", source, flush=True)
        print("EN:", en, flush=True)
        print("RU:", ru, flush=True)
        print("---", flush=True)


if __name__ == "__main__":
    main()
