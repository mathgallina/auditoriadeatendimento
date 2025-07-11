"""
Critérios de Avaliação para Auditoria de Atendimento
Define palavras positivas, tempos de resposta e critérios de avaliação
"""

from typing import List, Dict, Any


class CriteriosAvaliacao:
    """Classe que define os critérios para avaliação de atendimento"""
    
    def __init__(self):
        """Inicializa os critérios de avaliação"""
        self.palavras_positivas = [
            "obrigado", "obrigada", "por favor", "vamos resolver", 
            "fico à disposição", "entendo", "compreendo", "claro",
            "certamente", "sem dúvida", "vou ajudar", "posso ajudar",
            "vamos verificar", "vou verificar", "perfeito", "excelente",
            "ótimo", "muito bem", "vamos lá", "tranquilo", "calma",
            "paciência", "vou resolver", "vou cuidar", "fique tranquilo",
            "não se preocupe", "vou fazer o possível", "vou tentar",
            "vou investigar", "vou analisar", "vou verificar"
        ]
        
        self.tempo_resposta_limites = {
            "excelente": 10,  # segundos
            "bom": 20,
            "regular": 30,
            "ruim": 60
        }
        
        self.pesos_avaliacao = {
            "empatia": 0.6,
            "tempo_resposta": 0.4
        }
    
    def get_palavras_positivas(self) -> List[str]:
        """Retorna a lista de palavras positivas"""
        return self.palavras_positivas.copy()
    
    def get_tempo_limites(self) -> Dict[str, int]:
        """Retorna os limites de tempo para avaliação"""
        return self.tempo_resposta_limites.copy()
    
    def get_pesos(self) -> Dict[str, float]:
        """Retorna os pesos para cálculo da média final"""
        return self.pesos_avaliacao.copy()
    
    def calcular_nota_tempo(self, tempo_medio: float) -> float:
        """
        Calcula a nota de tempo de resposta baseada no tempo médio
        
        Args:
            tempo_medio: Tempo médio de resposta em segundos
            
        Returns:
            Nota de 0 a 10
        """
        if tempo_medio <= self.tempo_resposta_limites["excelente"]:
            return 10.0
        elif tempo_medio <= self.tempo_resposta_limites["bom"]:
            return 8.0
        elif tempo_medio <= self.tempo_resposta_limites["regular"]:
            return 6.0
        elif tempo_medio <= self.tempo_resposta_limites["ruim"]:
            return 4.0
        else:
            return 2.0
    
    def calcular_nota_empatia(self, palavras_encontradas: int, total_mensagens: int) -> float:
        """
        Calcula a nota de empatia baseada nas palavras positivas encontradas
        
        Args:
            palavras_encontradas: Número de palavras positivas encontradas
            total_mensagens: Total de mensagens do atendente
            
        Returns:
            Nota de 0 a 10
        """
        if total_mensagens == 0:
            return 0.0
        
        # Calcula a proporção de mensagens com palavras positivas
        proporcao = palavras_encontradas / total_mensagens
        
        # Converte para nota de 0 a 10
        if proporcao >= 0.8:
            return 10.0
        elif proporcao >= 0.6:
            return 8.5
        elif proporcao >= 0.4:
            return 7.0
        elif proporcao >= 0.2:
            return 5.5
        elif proporcao >= 0.1:
            return 4.0
        else:
            return 2.0
    
    def calcular_media_final(self, nota_empatia: float, nota_tempo: float) -> float:
        """
        Calcula a média final ponderada
        
        Args:
            nota_empatia: Nota de empatia (0-10)
            nota_tempo: Nota de tempo de resposta (0-10)
            
        Returns:
            Média final ponderada
        """
        peso_empatia = self.pesos_avaliacao["empatia"]
        peso_tempo = self.pesos_avaliacao["tempo_resposta"]
        
        media_final = (nota_empatia * peso_empatia) + (nota_tempo * peso_tempo)
        return round(media_final, 1) 