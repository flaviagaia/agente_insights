from __future__ import annotations

import streamlit as st

from src.agent import ask_business_insights_agent
from src.sample_data import load_snapshots


st.set_page_config(page_title="Agente de Insights para Negócio", layout="wide")
st.title("Agente de Insights para Negócio")
st.caption("MVP com LlamaIndex Agents para diagnóstico executivo, riscos, oportunidades e ações prioritárias.")

snapshots = load_snapshots()
options = snapshots.set_index("company_id")["company_name"].to_dict()

with st.sidebar:
    st.header("Stack Técnica")
    st.markdown(
        """
        - `LlamaIndex Agents` para orquestração baseada em tools
        - `FunctionAgent` como runtime previsto
        - `FunctionTool` para encapsular leitura analítica do negócio
        - fallback determinístico para execução local
        - `Streamlit` para inspeção técnica e visualização do output
        """
    )
    st.header("Camadas do MVP")
    st.markdown(
        """
        - snapshot do negócio
        - diagnóstico de crescimento e eficiência
        - leitura de risco e oportunidade
        - recomendação executiva
        """
    )

company_id = st.selectbox(
    "Selecione a empresa",
    options=list(options.keys()),
    format_func=lambda cid: f"{cid} - {options[cid]}",
)

question = st.text_area(
    "Pergunta executiva",
    value="Quais são os principais sinais do trimestre e o que deveríamos priorizar agora?",
    height=120,
)

if st.button("Executar agente", type="primary"):
    result = ask_business_insights_agent(company_id=company_id, user_question=question)

    c1, c2, c3 = st.columns(3)
    c1.metric("Runtime mode", result["runtime_mode"])
    c2.metric("Crescimento", f"{result['diagnostics']['growth_pct']:.2f}%")
    c3.metric("Receita por cliente", f"R$ {result['diagnostics']['revenue_per_customer']:.2f}")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Mensagem final", "Diagnóstico", "Riscos e oportunidades", "Snapshot estruturado"]
    )
    with tab1:
        st.markdown(result["final_message"])
    with tab2:
        st.subheader("Insight executivo")
        st.write(result["executive_insight"])
        st.json(result["diagnostics"])
    with tab3:
        st.json(result["risks_and_opportunities"])
        st.json(result["recommended_actions"])
    with tab4:
        st.json(result["snapshot"])

st.divider()
st.subheader("Arquitetura resumida")
st.code(
    """Executivo -> LlamaIndex FunctionAgent -> tools analíticas -> insight executivo final
             \\-> fallback determinístico local (sem OPENAI_API_KEY / sem runtime LlamaIndex)""",
    language="text",
)
