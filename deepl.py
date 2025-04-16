import http.client
import json

# Full Documentation here https://developers.deepl.com/docs/api-reference/translate/openapi-spec-for-text-translation
SOURCE_LANGUAGES = [
    "BG",
    "CS",
    "DA",
    "DE",
    "EL",
    "EN",
    "ES",
    "ET",
    "FI",
    "FR",
    "HU",
    "ID",
    "IT",
    "JA",
    "KO",
    "LT",
    "LV",
    "NB",
    "NL",
    "PL",
    "PT",
    "RO",
    "RU",
    "SK",
    "SL",
    "SV",
    "TR",
    "UK",
    "ZH",
]
TARGET_LANGUAGES = [
    "AR",
    "BG",
    "CS",
    "DA",
    "DE",
    "EL",
    "EN-GB",
    "EN-US",
    "ES",
    "ET",
    "FI",
    "FR",
    "HU",
    "ID",
    "IT",
    "JA",
    "KO",
    "LT",
    "LV",
    "NB",
    "NL",
    "PL",
    "PT-BR",
    "PT-PT",
    "RO",
    "RU",
    "SK",
    "SL",
    "SV",
    "TR",
    "UK",
    "ZH",
    "ZH-HANS",
    "ZH-HANT",
]


def translate_multiple(
    source_lang: str,
    target_lang: str,
    phrases: list[str],
) -> list[str]:
    if not phrases:
        return []

    conn = http.client.HTTPSConnection("api-free.deepl.com")
    payload = json.dumps(
        {
            "source_lang": source_lang,
            "target_lang": target_lang,
            "text": phrases if phrases else [],
        }
    )
    headers = {
        "Content-Type": "application/json",
        "Authorization": "",
    }
    conn.request("POST", "/v2/translate", payload, headers)
    data = json.loads(conn.getresponse().read().decode("utf-8"))
    return [t.get("text") for t in data.get("translations")]
