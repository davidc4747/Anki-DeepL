from dataclasses import dataclass
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

_DEEPL_AUTH = ""


def translate_phrases(
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
        "Authorization": _DEEPL_AUTH,
    }
    conn.request("POST", "/v2/translate", payload, headers)
    raw = conn.getresponse().read().decode("utf-8")
    data = json.loads(raw)

    if data.get("message"):
        raise RuntimeError(f'DeepL Tanslation failed: {data.get("message")}')
    else:
        return [t.get("text") for t in data.get("translations")]


@dataclass
class DeepLUsageResponse:
    character_count: int
    character_limit: int


def deepl_usage() -> DeepLUsageResponse:
    conn = http.client.HTTPSConnection("api-free.deepl.com")
    payload = ""
    headers = {"Authorization": _DEEPL_AUTH}
    conn.request("GET", "/v2/usage", payload, headers)
    raw = conn.getresponse().read().decode("utf-8")
    data = json.loads(raw)
    return DeepLUsageResponse(
        character_count=data.get("character_count"),
        character_limit=data.get("character_limit"),
    )
