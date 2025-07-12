"""
Auditor de Atendimento - Interface Web
Aplicação Streamlit para análise de qualidade de atendimento
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import tempfile
import os
import sys
from pathlib import Path

# Adiciona o diretório auditor ao path
sys.path.append(str(Path(__file__).parent / "auditor"))

from auditor.analisador import AnalisadorAtendimento
from auditor.criterios import CriteriosAvaliacao


def main():
    """Função principal da aplicação Streamlit"""
    
    # Configuração da página
    st.set_page_config(
        page_title="Auditor de Atendimento",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Título principal
    st.title("🎯 Auditor de Atendimento")
    st.markdown("### Sistema automatizado para análise de qualidade de atendimento ao cliente")
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Como usar")
        st.markdown("""
        1. **Faça upload** de um arquivo .txt com a conversa
        2. **Formato esperado**: `[HH:MM:SS] Autor: Mensagem`
        3. **Clique em Analisar** para gerar o relatório
        4. **Visualize** os resultados e gráficos
        """)
        
        st.header("📝 Exemplo de formato")
        st.code("""
[09:00:15] Cliente: Olá, preciso de ajuda
[09:00:25] Atendente: Olá! Como posso ajudá-lo?
[09:00:45] Cliente: Tenho um problema
[09:01:00] Atendente: Entendo, vou verificar
        """)
        
        st.header("🔗 Links")
        st.markdown("[GitHub](https://github.com/mathgallina/auditoriadeatendimento)")
        st.markdown("[Documentação](https://github.com/mathgallina/auditoriadeatendimento#readme)")
    
    # Área principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📤 Upload do Arquivo")
        
        # Upload do arquivo
        uploaded_file = st.file_uploader(
       "Escolha um arquivo .txt ou .pdf com a conversa",
       type=['txt', 'pdf'],
       help="Arraste um arquivo ou clique para selecionar"
   )
        # Botão de análise
        if uploaded_file is not None:
            if st.button("🔍 Analisar Conversa", type="primary"):
                with st.spinner("Analisando conversa..."):
                    resultado = analisar_arquivo_upload(uploaded_file)
                    if resultado:
                        exibir_resultados(resultado)
    
    with col2:
        st.header("📊 Estatísticas Rápidas")
        
        # Carregar arquivo de exemplo se disponível
        if os.path.exists("exemplos/exemplo_conversa.txt"):
            if st.button("📖 Testar com Exemplo"):
                with st.spinner("Analisando exemplo..."):
                    resultado = analisar_arquivo_local("exemplos/exemplo_conversa.txt")
                    if resultado:
                        exibir_resultados(resultado)


def analisar_arquivo_upload(uploaded_file):
    try:
        if uploaded_file.name.lower().endswith('.pdf'):
            if PyPDF2 is None:
                st.error("PyPDF2 não está instalado. Adicione 'PyPDF2' ao requirements.txt.")
                return None
            texto = extrair_texto_pdf(uploaded_file)
            if not texto.strip():
                st.error("Não foi possível extrair texto do PDF. Verifique se o PDF não é escaneado/imagem.")
                return None
            # Salva texto extraído em arquivo temporário
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as tmp_file:
                tmp_file.write(texto)
                tmp_file_path = tmp_file.name
            analisador = AnalisadorAtendimento()
            resultado = analisador.analisar_conversa(tmp_file_path)
            os.unlink(tmp_file_path)
            return resultado
        else:
            # TXT normal
            try:
                content = uploaded_file.getvalue().decode('utf-8')
            except UnicodeDecodeError:
                content = uploaded_file.getvalue().decode('latin1')
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as tmp_file:
                tmp_file.write(content)
                tmp_file_path = tmp_file.name
            analisador = AnalisadorAtendimento()
            resultado = analisador.analisar_conversa(tmp_file_path)
            os.unlink(tmp_file_path)
            return resultado
    except Exception as e:
        st.error(f"❌ Erro ao analisar arquivo: {e}")
        return None


def analisar_arquivo_local(arquivo_path):
    """Analisa um arquivo local"""
    try:
        analisador = AnalisadorAtendimento()
        resultado = analisador.analisar_conversa(arquivo_path)
        return resultado
    except Exception as e:
        st.error(f"❌ Erro ao analisar arquivo: {e}")
        return None


def exibir_resultados(resultado):
    """Exibe os resultados da análise de forma visual"""
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="❤️ Empatia",
            value=f"{resultado['avaliacoes']['empatia']:.1f}/10",
            delta=None
        )
    
    with col2:
        st.metric(
            label="⏰ Tempo de Resposta",
            value=f"{resultado['avaliacoes']['tempo_resposta']:.1f}/10",
            delta=None
        )
    
    with col3:
        st.metric(
            label="🏆 Média Final",
            value=f"{resultado['avaliacoes']['media_final']:.1f}/10",
            delta=None
        )
    
    with col4:
        st.metric(
            label="💬 Total Mensagens",
            value=resultado['total_mensagens'],
            delta=None
        )
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de pizza das avaliações
        fig_pizza = go.Figure(data=[go.Pie(
            labels=['Empatia', 'Tempo de Resposta'],
            values=[
                resultado['avaliacoes']['empatia'],
                resultado['avaliacoes']['tempo_resposta']
            ],
            hole=0.4,
            marker_colors=['#FF6B6B', '#4ECDC4']
        )])
        fig_pizza.update_layout(
            title="📊 Distribuição das Avaliações",
            showlegend=True
        )
        st.plotly_chart(fig_pizza, use_container_width=True)
    
    with col2:
        # Gráfico de barras das estatísticas
        stats_data = {
            'Métrica': ['Cliente', 'Atendente', 'Palavras Positivas', 'Respostas Lentas'],
            'Quantidade': [
                resultado['mensagens_cliente'],
                resultado['mensagens_atendente'],
                resultado['palavras_positivas'],
                resultado['respostas_lentas']
            ]
        }
        df_stats = pd.DataFrame(stats_data)
        
        fig_barras = px.bar(
            df_stats,
            x='Métrica',
            y='Quantidade',
            color='Quantidade',
            title="📈 Estatísticas da Conversa",
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_barras, use_container_width=True)
    
    # Detalhes da análise
    st.header("🔍 Detalhes da Análise")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Informações Gerais")
        st.write(f"**Data/Hora da Análise:** {resultado['data_analise']}")
        st.write(f"**Duração Total:** {resultado['duracao_total']}")
        st.write(f"**Tempo Médio de Resposta:** {resultado['tempo_medio_resposta']:.1f} segundos")
        
        # Barra de progresso para a média final
        media_final = resultado['avaliacoes']['media_final']
        st.write(f"**Média Final:** {media_final:.1f}/10")
        st.progress(media_final / 10)
    
    with col2:
        st.subheader("💡 Recomendações")
        
        if media_final >= 8:
            st.success("🎉 Excelente atendimento! Continue assim!")
        elif media_final >= 6:
            st.info("👍 Bom atendimento, mas há espaço para melhorias.")
        elif media_final >= 4:
            st.warning("⚠️ Atendimento regular. Foque em melhorar a empatia e agilidade.")
        else:
            st.error("🚨 Atendimento precisa de melhorias significativas.")
        
        if resultado['respostas_lentas'] > 0:
            st.warning(f"⏰ Reduzir tempo de resposta (encontradas {resultado['respostas_lentas']} respostas lentas)")
        
        if resultado['palavras_positivas'] < 3:
            st.info("💬 Aumentar uso de palavras positivas e empáticas")
    
    # Critérios utilizados
    with st.expander("📊 Critérios de Avaliação"):
        criterios = CriteriosAvaliacao()
        
        st.subheader("Palavras Positivas Reconhecidas")
        palavras = criterios.get_palavras_positivas()
        st.write(", ".join(palavras[:10]) + "...")
        
        st.subheader("Limites de Tempo de Resposta")
        limites = criterios.get_tempo_limites()
        for categoria, tempo in limites.items():
            st.write(f"**{categoria.title()}:** ≤ {tempo} segundos")
        
        st.subheader("Pesos da Avaliação")
        pesos = criterios.get_pesos()
        st.write(f"**Empatia:** {pesos['empatia']*100:.0f}%")
        st.write(f"**Tempo de Resposta:** {pesos['tempo_resposta']*100:.0f}%")


if __name__ == "__main__":
    main() 
