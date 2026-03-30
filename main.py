from __future__ import annotations

import json
from pathlib import Path

from src.agent import ask_business_insights_agent
from src.sample_data import ensure_sample_data


def main() -> None:
    ensure_sample_data()
    result = ask_business_insights_agent(
        company_id="BIZ-1002",
        user_question="Quais riscos e oportunidades mais importantes deveríamos levar para a diretoria?",
    )
    output_path = Path(__file__).resolve().parent / "data" / "processed" / "business_insights_report.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Agente Insights")
    print(f"runtime_mode: {result['runtime_mode']}")
    print(f"company_id: {result['company_id']}")
    print(f"growth_pct: {result['diagnostics']['growth_pct']}")
    print(f"risk_flags: {', '.join(result['diagnostics']['risk_flags'])}")
    print(f"output_path: {output_path}")


if __name__ == "__main__":
    main()
