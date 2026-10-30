import requests
from bs4 import BeautifulSoup
import json
import time

def varrer_imobiliaria(url_base, nome_imobiliaria):
    print(f"Iniciando varredura em: {nome_imobiliaria}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        resposta = requests.get(url_base, headers=headers)
        resposta.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {nome_imobiliaria}: {e}")
        return []

    soup = BeautifulSoup(resposta.text, 'html.parser')
    imoveis_encontrados = []

    # ATENÇÃO: Substitua as classes HTML abaixo de acordo com o código fonte de cada imobiliária
    cards_imoveis = soup.find_all('div', class_='card-imovel-exemplo') 

    for card in cards_imoveis:
        try:
            titulo_elemento = card.find('h2', class_='titulo-exemplo')
            titulo = titulo_elemento.text.strip() if titulo_elemento else "Sem título"

            bairro_elemento = card.find('span', class_='bairro-exemplo')
            bairro = bairro_elemento.text.strip() if bairro_elemento else "Bairro não informado"

            preco_elemento = card.find('div', class_='preco-exemplo')
            preco = preco_elemento.text.strip() if preco_elemento else "Sob consulta"

            link_elemento = card.find('a', href=True)
            link_original = link_elemento['href'] if link_elemento else ""
            
            if link_original.startswith('/'):
                link_original = "https://www.site-da-imobiliaria.com.br" + link_original

            imoveis_encontrados.append({
                "imobiliaria": nome_imobiliaria,
                "titulo": titulo,
                "bairro": bairro,
                "preco": preco,
                "link": link_original,
                "status": "ativo"
            })
            
        except AttributeError:
            continue

    return imoveis_encontrados

def main():
    # Insira aqui os links verdadeiros das imobiliárias de Chapecó que deseja monitorar
    alvos = [
        {"nome": "SM Santa Maria", "url": "https://www.smsantamaria.com.br/venda/chapeco"},
        {"nome": "Nostra Casa", "url": "https://www.nostracasa.com.br/venda/chapeco"}
    ]
    
    todos_imoveis = []

    for alvo in alvos:
        imoveis = varrer_imobiliaria(alvo['url'], alvo['nome'])
        todos_imoveis.extend(imoveis)
        time.sleep(2) 

    with open('base_radar.json', 'w', encoding='utf-8') as f:
        json.dump(todos_imoveis, f, ensure_ascii=False, indent=4)
        
    print(f"Varredura concluída! {len(todos_imoveis)} imóveis reais capturados e salvos em 'base_radar.json'.")

if __name__ == "__main__":
    main()
