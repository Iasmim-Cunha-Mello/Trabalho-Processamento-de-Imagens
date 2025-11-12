### adicionado (perfil de público, nivel de movimento, horário de funcionamento, reserva, recomendação IA, insight surpresa) #alisson



PROMPT_ANALISE_COMPLETA = """
Analise a imagem fornecida e me retorne **apenas** um objeto JSON.
Não inclua "```json" ou qualquer outro texto antes ou depois.

O JSON deve seguir esta estrutura:
{
  "nome_provavel": "O nome exato que você acha que é (ex: 'Starbucks') ou null se não souber",
  "tipo_estabelecimento": "O tipo de estabelecimento (ex: 'Cafeteria', 'Loja de Roupas', 'Restaurante')",
  "descricao_curta": "Uma descrição de 10-15 palavras da cena e do ambiente.",
  "tags_caracteristicas": ["Uma", "lista", "de 3 tags objetivas que descrevem o local"],
  "google_maps_query": "A string de busca ideal para o Google Maps (ex: 'Cafeteria Starbucks')",

  "perfil_de_publico": "Para quem este local parece ser? (ex: 'Famílias', 'Casais', 'Estudantes', 'Profissionais')",
  "nivel_de_movimento": "Qual o nível de movimento/lotação? (ex: 'Baixo', 'Moderado', 'Alto (Horário de Pico)')",
  "horario_funcionamento_estimado": "Baseado no tipo de local, qual o horário de funcionamento provável? (ex: 'Horário comercial', 'Provavelmente até tarde', 'Abre apenas para jantar', 'Provavelmente 24h')",
  "necessita_reserva": "Inferindo do tipo de local e do movimento, é provável que precise de reserva? (ex: 'Provavelmente sim', 'Provavelmente não', 'Não se aplica')",
  "insight_surpresa": "Qual o insight ou detalhe mais surpreendente e útil da imagem? (ex: 'Promoção visível na janela', 'Parece pet-friendly', 'Estacionamento fácil')",
  
  "recomendacao_ia": "Uma recomendação de 1 frase para o usuário, baseada em **todos** os insights (ex: 'Ótimo para famílias, mas parece estar em horário de pico.')"
}
"""
