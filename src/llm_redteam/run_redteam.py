
import os

from dotenv import load_dotenv
from deepteam import red_team

from llm_redteam.callback import model_callback
from llm_redteam.nvidia_models import NvidiaModel
from llm_redteam.redteam_config import get_vulnerabilities


load_dotenv()


def main():

    if not os.getenv("NVIDIA_API_KEY"):
        raise RuntimeError("NVIDIA_API_KEY missing in .env")

    print("=" * 60)
    print("FIRST LLM RED-TEAM ASSESSMENT")
    print("=" * 60)

    model_name = os.getenv("NVIDIA_MODEL")
    print(f"NVIDIA model: {model_name}")

    simulator = NvidiaModel()
    evaluator = NvidiaModel()

    vulnerabilities = get_vulnerabilities(
        simulator=simulator,
        evaluator=evaluator,
    )

    print("\nVulnerabilities:")
    for vulnerability in vulnerabilities:
        print(f"- {vulnerability.get_name()}")

    print("\nStarting assessment...")
    print("Target: http://127.0.0.1:8000/chat")

    risk_assessment = red_team(
        model_callback=model_callback,
        vulnerabilities=vulnerabilities,
        # Use the NVIDIA adapter for both attack simulation and evaluation;
        # otherwise DeepTeam falls back to its default OpenAI models.
        simulator_model=simulator,
        evaluation_model=evaluator,
        attacks_per_vulnerability_type=1,
    )

    print("\nAssessment finished.")
    print(risk_assessment.overview)

    os.makedirs("reports", exist_ok=True)

    risk_assessment.save(to="./reports/")

    print("\nReports saved to ./reports/")


if __name__ == "__main__":
    main()
