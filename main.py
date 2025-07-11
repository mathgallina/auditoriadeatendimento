#!/usr/bin/env python3
"""
Auditor de Atendimento
Sistema para análise automática de qualidade de atendimento ao cliente
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório auditor ao path
sys.path.append(str(Path(__file__).parent / "auditor"))

from auditor.analisador import AnalisadorAtendimento
from auditor.criterios import CriteriosAvaliacao


def main():
    """Função principal do sistema de auditoria"""
    print("🎯 AUDITOR DE ATENDIMENTO")
    print("=" * 50)
    
    # Verifica se foi fornecido um arquivo como argumento
    if len(sys.argv) > 1:
        arquivo_conversa = sys.argv[1]
    else:
        # Tenta usar o arquivo de exemplo
        arquivo_conversa = "exemplos/exemplo_conversa.txt"
    
    # Verifica se o arquivo existe
    if not os.path.exists(arquivo_conversa):
        print(f"❌ Erro: Arquivo '{arquivo_conversa}' não encontrado!")
        print("\n📝 Uso:")
        print("  python main.py [arquivo_conversa.txt]")
        print("\n📁 Exemplo:")
        print("  python main.py exemplos/exemplo_conversa.txt")
        return
    
    try:
        # Inicializa o analisador
        analisador = AnalisadorAtendimento()
        
        # Carrega e analisa a conversa
        print(f"📖 Analisando arquivo: {arquivo_conversa}")
        resultado = analisador.analisar_conversa(arquivo_conversa)
        
        # Exibe o relatório
        exibir_relatorio(resultado)
        
    except Exception as e:
        print(f"❌ Erro durante a análise: {e}")
        return


def exibir_relatorio(resultado):
    """Exibe o relatório de auditoria formatado"""
    print("\n" + "=" * 50)
    print("📊 RELATÓRIO DE AUDITORIA")
    print("=" * 50)
    
    # Informações gerais
    print(f"📅 Data/Hora: {resultado['data_analise']}")
    print(f"⏱️  Duração total: {resultado['duracao_total']}")
    print(f"💬 Total de mensagens: {resultado['total_mensagens']}")
    print(f"👤 Mensagens do cliente: {resultado['mensagens_cliente']}")
    print(f"👨‍💼 Mensagens do atendente: {resultado['mensagens_atendente']}")
    
    # Avaliações
    print("\n" + "-" * 30)
    print("📈 AVALIAÇÕES")
    print("-" * 30)
    
    empatia = resultado['avaliacoes']['empatia']
    tempo_resposta = resultado['avaliacoes']['tempo_resposta']
    media_final = resultado['avaliacoes']['media_final']
    
    print(f"❤️  Empatia: {empatia:.1f}/10")
    print(f"⏰ Tempo de Resposta: {tempo_resposta:.1f}/10")
    print(f"🏆 Média Final: {media_final:.1f}/10")
    
    # Detalhes da análise
    print("\n" + "-" * 30)
    print("🔍 DETALHES")
    print("-" * 30)
    
    print(f"✅ Palavras positivas encontradas: {resultado['palavras_positivas']}")
    print(f"⏱️  Tempo médio de resposta: {resultado['tempo_medio_resposta']:.1f} segundos")
    print(f"🚨 Respostas lentas (>30s): {resultado['respostas_lentas']}")
    
    # Recomendações
    print("\n" + "-" * 30)
    print("💡 RECOMENDAÇÕES")
    print("-" * 30)
    
    if media_final >= 8:
        print("🎉 Excelente atendimento! Continue assim!")
    elif media_final >= 6:
        print("👍 Bom atendimento, mas há espaço para melhorias.")
    elif media_final >= 4:
        print("⚠️  Atendimento regular. Foque em melhorar a empatia e agilidade.")
    else:
        print("🚨 Atendimento precisa de melhorias significativas.")
    
    if resultado['respostas_lentas'] > 0:
        print(f"⏰ Reduzir tempo de resposta (encontradas {resultado['respostas_lentas']} respostas lentas)")
    
    if resultado['palavras_positivas'] < 3:
        print("💬 Aumentar uso de palavras positivas e empáticas")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
