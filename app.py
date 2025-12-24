import streamlit as st

# Configuração da página
st.set_page_config(page_title="Calculador de Insulina Seguro", page_icon="💉")

st.title("💉 Calculadora de Insulina")
st.write("Preencha os dados abaixo com atenção.")

# --- SEÇÃO DE CONFIGURAÇÕES MÉDICAS (Pode ser escondida ou fixada) ---
with st.sidebar:
    st.header("⚙️ Configurações Médicas")
    st.info("Estes dados devem ser preenchidos conforme a receita do endocrinologista.")
    alvo = st.number_input("Glicemia Alvo (mg/dL):", value=100)
    fs = st.number_input("Fator de Sensibilidade (FS):", value=50, help="Quanto 1 unidade de insulina baixa sua glicemia")
    icr = st.number_input("Relação Carboidrato (ICR):", value=15, help="Quantas gramas de carbo 1 unidade de insulina cobre")

# --- ENTRADA DE DADOS DO MOMENTO ---
col1, col2 = st.columns(2)

with col1:
    glicemia_atual = st.number_input("Glicemia Atual:", min_value=20, max_value=600, step=1)

with col2:
    carbos_refeicao = st.number_input("Carboidratos (g):", min_value=0, max_value=300, step=1)

# --- LÓGICA DE CÁLCULO ---
def calcular_dose(atual, alvo, fs, carbos, icr):
    # Cálculo de correção (glicemia alta)
    dose_correcao = (atual - alvo) / fs if atual > alvo else 0
    
    # Cálculo para o alimento
    dose_alimento = carbos / icr
    
    return dose_correcao + dose_alimento

# --- EXIBIÇÃO DO RESULTADO ---
if st.button("CALCULAR DOSE AGORA", use_container_width=True):
    # Alerta de Hipoglicemia
    if glicemia_atual < 70:
        st.error("⚠️ ATENÇÃO: Glicemia BAIXA. Não aplique insulina! Coma 15g de carboidrato rápido e reteste em 15 min.")
    else:
        dose_total = calcular_dose(glicemia_atual, alvo, fs, carbos_refeicao, icr)
        
        # Arredondamento para 0.5 (comum em canetas)
        dose_arredondada = round(dose_total * 2) / 2
        
        st.success(f"### Dose Sugerida: **{dose_arredondada} unidades**")
        
        # Detalhamento para conferência
        with st.expander("Ver detalhes do cálculo"):
            st.write(f"Correção: {max(0, (glicemia_atual-alvo)/fs):.2f} u")
            st.write(f"Alimento: {carbos_refeicao/icr:.2f} u")
            st.write(f"Total exato: {dose_total:.2f} u")

st.divider()
st.caption("Aviso: Use este app apenas como auxílio. Sempre confirme com seu médico.")