from __future__ import annotations

import os
from typing import Any

from .tools import (
    build_fallback_report,
    compute_growth_diagnostics,
    generate_executive_insights,
    get_business_snapshot,
    identify_business_risks,
    suggest_business_actions,
)


def _build_llamaindex_agent(model_name: str = "gpt-4.1-mini"):
    if not os.getenv("OPENAI_API_KEY"):
        return None

    try:
        from llama_index.core.agent.workflow import FunctionAgent
        from llama_index.core.tools import FunctionTool
        from llama_index.llms.openai import OpenAI
    except Exception:
        return None

    llm = OpenAI(model=model_name, api_key=os.getenv("OPENAI_API_KEY"))
    tools = [
        FunctionTool.from_defaults(fn=get_business_snapshot),
        FunctionTool.from_defaults(fn=compute_growth_diagnostics),
        FunctionTool.from_defaults(fn=identify_business_risks),
        FunctionTool.from_defaults(fn=generate_executive_insights),
        FunctionTool.from_defaults(fn=suggest_business_actions),
    ]
    system_prompt = (
        "Você é um agente de geração de insights para negócio. Sempre use as ferramentas para consultar o "
        "snapshot, interpretar crescimento, riscos e recomendar ações. Não invente números nem benchmark externos."
    )
    return FunctionAgent(
        tools=tools,
        llm=llm,
        system_prompt=system_prompt,
    )


def ask_business_insights_agent(
    company_id: str,
    user_question: str,
    model_name: str = "gpt-4.1-mini",
) -> dict[str, Any]:
    agent = _build_llamaindex_agent(model_name=model_name)
    if agent is None:
        report = build_fallback_report(company_id=company_id, user_question=user_question)
        return {"runtime_mode": "deterministic_fallback", **report}

    prompt = (
        f"company_id={company_id}\n"
        f"user_question={user_question}\n"
        "Gere um diagnóstico executivo, principais riscos, oportunidades e ações prioritárias."
    )
    try:
        response = agent.run(prompt)
        final_text = str(response)
    except Exception:
        report = build_fallback_report(company_id=company_id, user_question=user_question)
        return {"runtime_mode": "deterministic_fallback", **report}

    report = build_fallback_report(company_id=company_id, user_question=user_question)
    report["final_message"] = final_text or report["final_message"]
    return {"runtime_mode": "llamaindex_agent", **report}
