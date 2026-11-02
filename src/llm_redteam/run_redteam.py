
import os

from dotenv import load_dotenv
from deepteam import red_team

from llm_redteam.callback import model_callback
from llm_redteam.redteam_config import get_vulnerabilities
from llm_redteam.nvidia_models import NvidiaModel


load_dotenv()


def main():
    print("=" * 60)
    print("LLM RED TEAMING POC")
    print("=" * 60)

    if not os.getenv("NVIDIA_API_KEY"):
        raise RuntimeError("NVIDIA_API_KEY is missing")

    model = NvidiaModel()

    vulnerabilities = get_vulnerabilities()

    print(f"\nModel: {model.get_model_name()}")
    print("Vulnerabilities:")

    for vulnerability in vulnerabilities:
        print(f"- {vulnerability.get_name()}")

    print("\nStarting assessment...")

    risk_assessment = red_team(
        model_callback=model_callback,
        vulnerabilities=vulnerabilities,
        attacks_per_vulnerability_type=2,
        simulator_model=model,
        evaluation_model=model,
    )

    print("\nAssessment completed.")
    print(risk_assessment.overview)

    os.makedirs("reports", exist_ok=True)
    risk_assessment.save(to="./reports/")

    print("\nReports saved to ./reports/")


if __name__ == "__main__":
    main()
