
from deepteam.vulnerabilities import (
    PromptLeakage,
    PIILeakage,
)


def get_vulnerabilities():
    """
    Define the security risks relevant to our chatbot POC.
    """

    prompt_leakage = PromptLeakage(
        # "system_prompt" was renamed in deepteam — use "instructions" instead.
        # Valid types: "secrets_and_credentials", "instructions",
        #              "guard_exposure", "permissions_and_roles"
        types=["instructions"],
    )

    pii_leakage = PIILeakage(
        types=["api_and_database_access"],
    )

    return [
        prompt_leakage,
        pii_leakage,
    ]
