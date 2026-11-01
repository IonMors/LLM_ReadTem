
from deepteam.vulnerabilities import (
    PromptLeakage,
    PIILeakage,
)


def get_vulnerabilities():
    """
    Define the security risks relevant to our chatbot POC.
    """

    prompt_leakage = PromptLeakage(
        types=["system_prompt"],
    )

    pii_leakage = PIILeakage(
        types=["api_and_database_access"],
    )

    return [
        prompt_leakage,
        pii_leakage,
    ]
