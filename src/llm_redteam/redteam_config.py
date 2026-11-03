
from deepteam.vulnerabilities import PromptLeakage, PIILeakage


def get_vulnerabilities(simulator, evaluator):

    return [
        PromptLeakage(
            # DeepTeam 1.0.10 uses "instructions" for system-prompt leakage.
            types=["instructions"],
            simulator_model=simulator,
            evaluation_model=evaluator,
            async_mode=False,
        ),
        PIILeakage(
            types=["api_and_database_access"],
            simulator_model=simulator,
            evaluation_model=evaluator,
            async_mode=False,
        ),
    ]
