from __future__ import annotations

import json
from typing import Any

from .sample_data import load_snapshot


def get_business_snapshot(company_id: str) -> dict[str, Any]:
    """Retorna o snapshot canônico do negócio para o período analisado."""
    return load_snapshot(company_id)


def compute_growth_diagnostics(company_id: str) -> dict[str, Any]:
    """Calcula crescimento, retenção e eficiência comercial básica."""
    snapshot = load_snapshot(company_id)
    revenue_current = float(snapshot["revenue_current"])
    revenue_previous = float(snapshot["revenue_previous"])
    growth_pct = round(((revenue_current - revenue_previous) / revenue_previous) * 100, 2)
    customers = int(snapshot["active_customers"])
    revenue_per_customer = round(revenue_current / max(customers, 1), 2)
    support_load_per_customer = round(float(snapshot["support_tickets"]) / max(customers, 1), 3)

    flags: list[str] = []
    if growth_pct < 0:
        flags.append("receita_em_contracao")
    elif growth_pct >= 10:
        flags.append("crescimento_acelerado")
    if float(snapshot["churn_pct"]) >= 6:
        flags.append("churn_elevado")
    if float(snapshot["marketing_cac"]) >= 1000:
        flags.append("cac_pressurizado")
    if support_load_per_customer >= 2:
        flags.append("carga_suporte_alta")
    if float(snapshot["on_time_delivery_pct"]) < 90:
        flags.append("eficiencia_operacional_baixa")

    return {
        "company_id": company_id,
        "growth_pct": growth_pct,
        "revenue_per_customer": revenue_per_customer,
        "support_load_per_customer": support_load_per_customer,
        "risk_flags": flags,
    }


def identify_business_risks(company_id: str) -> dict[str, Any]:
    """Traduz indicadores em leitura executiva de risco e oportunidade."""
    snapshot = load_snapshot(company_id)
    diagnostics = compute_growth_diagnostics(company_id)

    risks: list[str] = []
    opportunities: list[str] = []

    if "receita_em_contracao" in diagnostics["risk_flags"]:
        risks.append("queda de receita com pressão competitiva e necessidade de retenção")
    if "churn_elevado" in diagnostics["risk_flags"]:
        risks.append("erosão de base ativa e risco de perda de LTV")
    if "cac_pressurizado" in diagnostics["risk_flags"]:
        risks.append("aquisição menos eficiente e payback potencialmente alongado")
    if "eficiencia_operacional_baixa" in diagnostics["risk_flags"]:
        risks.append("sinal de fricção operacional que pode impactar satisfação")

    if diagnostics["growth_pct"] > 0 and float(snapshot["nps"]) >= 45:
        opportunities.append("crescimento com boa percepção do cliente")
    if float(snapshot["gross_margin_pct"]) >= 65:
        opportunities.append("margem saudável para reinvestimento seletivo")
    if float(snapshot["churn_pct"]) <= 3:
        opportunities.append("retenção forte como base para expansão de receita")

    return {
        "company_id": company_id,
        "risks": risks,
        "opportunities": opportunities,
    }


def generate_executive_insights(company_id: str) -> str:
    """Gera uma narrativa executiva sintética e grounded no snapshot."""
    snapshot = load_snapshot(company_id)
    diagnostics = compute_growth_diagnostics(company_id)
    risk_map = identify_business_risks(company_id)

    headline = (
        f"{snapshot['company_name']} em {snapshot['period']}: crescimento de {diagnostics['growth_pct']}% "
        f"com margem bruta de {snapshot['gross_margin_pct']}%."
    )
    risk_text = "; ".join(risk_map["risks"]) if risk_map["risks"] else "sem riscos críticos imediatos"
    opp_text = (
        "; ".join(risk_map["opportunities"])
        if risk_map["opportunities"]
        else "espaço para melhorar retenção, eficiência e monetização"
    )
    return f"{headline} Principais riscos: {risk_text}. Principais oportunidades: {opp_text}."


def suggest_business_actions(company_id: str) -> dict[str, Any]:
    """Propõe ações executivas priorizadas a partir das flags encontradas."""
    snapshot = load_snapshot(company_id)
    diagnostics = compute_growth_diagnostics(company_id)

    actions: list[str] = []
    if "churn_elevado" in diagnostics["risk_flags"]:
        actions.append("priorizar análise de churn cohort e atacar causas de cancelamento nas contas em risco")
    if "cac_pressurizado" in diagnostics["risk_flags"]:
        actions.append("revisar mix de canais e eficiência do funil para reduzir CAC incremental")
    if "carga_suporte_alta" in diagnostics["risk_flags"]:
        actions.append("identificar tickets repetitivos e melhorar onboarding ou autosserviço")
    if "eficiencia_operacional_baixa" in diagnostics["risk_flags"]:
        actions.append("endereçar gargalos operacionais que afetam prazo e experiência")
    if "crescimento_acelerado" in diagnostics["risk_flags"]:
        actions.append("proteger qualidade de atendimento enquanto escala aquisição")
    if not actions:
        actions.append("manter disciplina operacional e testar alavancas de expansão sobre a base atual")

    return {
        "company_id": company_id,
        "priority_actions": actions[:3],
        "board_message": (
            f"Prioridade executiva para {snapshot['company_name']}: equilibrar crescimento, retenção e eficiência."
        ),
    }


def build_fallback_report(company_id: str, user_question: str) -> dict[str, Any]:
    snapshot = get_business_snapshot(company_id)
    diagnostics = compute_growth_diagnostics(company_id)
    risks = identify_business_risks(company_id)
    insights = generate_executive_insights(company_id)
    actions = suggest_business_actions(company_id)

    final_message = (
        f"Pergunta executiva: {user_question}\n\n"
        f"Snapshot:\n{json.dumps(snapshot, ensure_ascii=False, indent=2)}\n\n"
        f"Diagnóstico:\n{json.dumps(diagnostics, ensure_ascii=False, indent=2)}\n\n"
        f"Mapa de risco e oportunidade:\n{json.dumps(risks, ensure_ascii=False, indent=2)}\n\n"
        f"Insight executivo:\n{insights}\n\n"
        f"Ações recomendadas:\n{json.dumps(actions, ensure_ascii=False, indent=2)}"
    )

    return {
        "company_id": company_id,
        "snapshot": snapshot,
        "diagnostics": diagnostics,
        "risks_and_opportunities": risks,
        "executive_insight": insights,
        "recommended_actions": actions,
        "final_message": final_message,
    }
