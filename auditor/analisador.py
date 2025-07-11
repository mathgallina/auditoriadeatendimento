"""
Analisador de Atendimento
Classe principal para análise de conversas e geração de relatórios
"""

import re
import datetime
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass

from .criterios import CriteriosAvaliacao


@dataclass
class Mensagem:
    """Representa uma mensagem da conversa"""
    timestamp: str
    autor: str
    conteudo: str
    hora: Optional[datetime.time] = None
    
    def __post_init__(self):
        """Extrai a hora do timestamp após a inicialização"""
        if self.timestamp:
            self.hora = self._extrair_hora()
    
    def _extrair_hora(self) -> datetime.time:
        """Extrai a hora do timestamp [HH:MM:SS]"""
        match = re.search(r'\[(\d{2}):(\d{2}):(\d{2})\]', self.timestamp)
        if match:
            hora, minuto, segundo = map(int, match.groups())
            return datetime.time(hora, minuto, segundo)
        return None


class AnalisadorAtendimento:
    """Classe principal para análise de atendimento"""
    
    def __init__(self):
        """Inicializa o analisador com critérios de avaliação"""
        self.criterios = CriteriosAvaliacao()
    
    def analisar_conversa(self, arquivo_conversa: str) -> Dict[str, Any]:
        """
        Analisa uma conversa e retorna o resultado da auditoria
        
        Args:
            arquivo_conversa: Caminho para o arquivo de conversa
            
        Returns:
            Dicionário com resultados da análise
        """
        # Carrega e processa as mensagens
        mensagens = self._carregar_mensagens(arquivo_conversa)
        
        # Separa mensagens por autor
        mensagens_cliente = [m for m in mensagens if m.autor.lower() == "cliente"]
        mensagens_atendente = [m for m in mensagens if m.autor.lower() == "atendente"]
        
        # Analisa palavras positivas
        palavras_positivas = self._contar_palavras_positivas(mensagens_atendente)
        
        # Analisa tempo de resposta
        tempo_medio, respostas_lentas = self._analisar_tempo_resposta(
            mensagens_cliente, mensagens_atendente
        )
        
        # Calcula durações
        duracao_total = self._calcular_duracao_total(mensagens)
        
        # Calcula avaliações
        nota_empatia = self.criterios.calcular_nota_empatia(
            palavras_positivas, len(mensagens_atendente)
        )
        nota_tempo = self.criterios.calcular_nota_tempo(tempo_medio)
        media_final = self.criterios.calcular_media_final(nota_empatia, nota_tempo)
        
        # Monta resultado
        resultado = {
            "data_analise": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "duracao_total": duracao_total,
            "total_mensagens": len(mensagens),
            "mensagens_cliente": len(mensagens_cliente),
            "mensagens_atendente": len(mensagens_atendente),
            "palavras_positivas": palavras_positivas,
            "tempo_medio_resposta": tempo_medio,
            "respostas_lentas": respostas_lentas,
            "avaliacoes": {
                "empatia": nota_empatia,
                "tempo_resposta": nota_tempo,
                "media_final": media_final
            }
        }
        
        return resultado
    
    def _carregar_mensagens(self, arquivo_conversa: str) -> List[Mensagem]:
        """
        Carrega e processa as mensagens do arquivo
        
        Args:
            arquivo_conversa: Caminho para o arquivo
            
        Returns:
            Lista de objetos Mensagem
        """
        mensagens = []
        
        try:
            with open(arquivo_conversa, 'r', encoding='utf-8') as arquivo:
                linhas = arquivo.readlines()
            
            for linha in linhas:
                linha = linha.strip()
                if not linha:
                    continue
                
                # Padrão: [HH:MM:SS] Autor: Mensagem
                match = re.match(r'(\[\d{2}:\d{2}:\d{2}\])?\s*([^:]+):\s*(.+)', linha)
                if match:
                    timestamp = match.group(1) or ""
                    autor = match.group(2).strip()
                    conteudo = match.group(3).strip()
                    
                    mensagem = Mensagem(timestamp, autor, conteudo)
                    mensagens.append(mensagem)
        
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo '{arquivo_conversa}' não encontrado")
        except Exception as e:
            raise Exception(f"Erro ao ler arquivo: {e}")
        
        return mensagens
    
    def _contar_palavras_positivas(self, mensagens_atendente: List[Mensagem]) -> int:
        """
        Conta palavras positivas nas mensagens do atendente
        
        Args:
            mensagens_atendente: Lista de mensagens do atendente
            
        Returns:
            Número de palavras positivas encontradas
        """
        palavras_positivas = self.criterios.get_palavras_positivas()
        total_encontradas = 0
        
        for mensagem in mensagens_atendente:
            conteudo_lower = mensagem.conteudo.lower()
            for palavra in palavras_positivas:
                if palavra.lower() in conteudo_lower:
                    total_encontradas += 1
                    break  # Conta apenas uma vez por mensagem
        
        return total_encontradas
    
    def _analisar_tempo_resposta(
        self, mensagens_cliente: List[Mensagem], 
        mensagens_atendente: List[Mensagem]
    ) -> Tuple[float, int]:
        """
        Analisa o tempo de resposta entre cliente e atendente
        
        Args:
            mensagens_cliente: Lista de mensagens do cliente
            mensagens_atendente: Lista de mensagens do atendente
            
        Returns:
            Tupla com (tempo_medio, respostas_lentas)
        """
        tempos_resposta = []
        respostas_lentas = 0
        
        # Combina todas as mensagens ordenadas por timestamp
        todas_mensagens = mensagens_cliente + mensagens_atendente
        todas_mensagens.sort(key=lambda m: m.hora or datetime.time(0, 0, 0))
        
        ultima_mensagem_cliente = None
        
        for mensagem in todas_mensagens:
            if mensagem.autor.lower() == "cliente":
                ultima_mensagem_cliente = mensagem
            elif mensagem.autor.lower() == "atendente" and ultima_mensagem_cliente:
                # Calcula tempo entre mensagem do cliente e resposta do atendente
                tempo_resposta = self._calcular_diferenca_tempo(
                    ultima_mensagem_cliente.hora, mensagem.hora
                )
                
                if tempo_resposta is not None:
                    tempos_resposta.append(tempo_resposta)
                    
                    # Conta respostas lentas (>30 segundos)
                    if tempo_resposta > 30:
                        respostas_lentas += 1
        
        # Calcula tempo médio
        tempo_medio = sum(tempos_resposta) / len(tempos_resposta) if tempos_resposta else 0
        
        return tempo_medio, respostas_lentas
    
    def _calcular_diferenca_tempo(self, hora1: Optional[datetime.time], hora2: Optional[datetime.time]) -> Optional[float]:
        """
        Calcula a diferença em segundos entre dois horários
        
        Args:
            hora1: Primeiro horário
            hora2: Segundo horário
            
        Returns:
            Diferença em segundos ou None se inválido
        """
        if not hora1 or not hora2:
            return None
        
        # Converte para segundos
        segundos1 = hora1.hour * 3600 + hora1.minute * 60 + hora1.second
        segundos2 = hora2.hour * 3600 + hora2.minute * 60 + hora2.second
        
        return segundos2 - segundos1
    
    def _calcular_duracao_total(self, mensagens: List[Mensagem]) -> str:
        """
        Calcula a duração total da conversa
        
        Args:
            mensagens: Lista de todas as mensagens
            
        Returns:
            String formatada com a duração
        """
        if not mensagens:
            return "00:00:00"
        
        # Ordena por timestamp
        mensagens_ordenadas = sorted(
            mensagens, 
            key=lambda m: m.hora or datetime.time(0, 0, 0)
        )
        
        primeira = mensagens_ordenadas[0].hora
        ultima = mensagens_ordenadas[-1].hora
        
        if not primeira or not ultima:
            return "00:00:00"
        
        # Calcula diferença
        segundos_total = self._calcular_diferenca_tempo(primeira, ultima)
        
        if segundos_total is None or segundos_total < 0:
            return "00:00:00"
        
        # Converte para formato HH:MM:SS
        horas = segundos_total // 3600
        minutos = (segundos_total % 3600) // 60
        segundos = segundos_total % 60
        
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}" 