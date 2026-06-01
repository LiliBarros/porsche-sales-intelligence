import re
import math
import pandas as pd
from datetime import datetime
from word2number import w2n

# Dicionário auxiliar para conversão de estados americanos
US_STATES = {
    'alabama': 'AL', 'alaska': 'AK', 'arizona': 'AZ', 'arkansas': 'AR', 'california': 'CA',
    'colorado': 'CO', 'connecticut': 'CT', 'delaware': 'DE', 'florida': 'FL', 'georgia': 'GA',
    'hawaii': 'HI', 'idaho': 'ID', 'illinois': 'IL', 'indiana': 'IN', 'iowa': 'IA',
    'kansas': 'KS', 'kentucky': 'KY', 'louisiana': 'LA', 'maine': 'ME', 'maryland': 'MD',
    'massachusetts': 'MA', 'michigan': 'MI', 'minnesota': 'MN', 'mississippi': 'MS', 'missouri': 'MO',
    'montana': 'MT', 'nebraska': 'NE', 'nevada': 'NV', 'new hampshire': 'NH', 'new jersey': 'NJ',
    'new mexico': 'NM', 'new york': 'NY', 'north carolina': 'NC', 'north dakota': 'ND', 'ohio': 'OH',
    'oklahoma': 'OK', 'oregon': 'OR', 'pennsylvania': 'PA', 'rhode island': 'RI', 'south carolina': 'SC',
    'south dakota': 'SD', 'tennessee': 'TN', 'texas': 'TX', 'utah': 'UT', 'vermont': 'VT',
    'virginia': 'VA', 'washington': 'WA', 'west virginia': 'WV', 'wisconsin': 'WI', 'wyoming': 'WY',
    'al': 'AL', 'ak': 'AK', 'az': 'AZ', 'ar': 'AR', 'ca': 'CA', 'co': 'CO', 'ct': 'CT', 'de': 'DE',
    'fl': 'FL', 'ga': 'GA', 'hi': 'HI', 'id': 'ID', 'il': 'IL', 'in': 'IN', 'ia': 'IA', 'ks': 'KS',
    'ky': 'KY', 'la': 'LA', 'me': 'ME', 'md': 'MD', 'ma': 'MA', 'mi': 'MI', 'mn': 'MN', 'ms': 'MS',
    'mo': 'MO', 'mt': 'MT', 'ne': 'NE', 'nv': 'NV', 'nh': 'NH', 'nj': 'NJ', 'nm': 'NM', 'ny': 'NY',
    'nc': 'NC', 'nd': 'ND', 'oh': 'OH', 'ok': 'OK', 'or': 'OR', 'pa': 'PA', 'ri': 'RI', 'sc': 'SC',
    'sd': 'SD', 'tn': 'TN', 'tx': 'TX', 'ut': 'UT', 'vt': 'VT', 'va': 'VA', 'wa': 'WA', 'wv': 'WV',
    'wi': 'WI', 'wy': 'WY'
}

# Lista de métodos de pagamento controlados
PAYMENT_METHODS = [
    "Credit Card", "Debit Card", "Bank Transfer", "Wire Transfer", 
    "Financing", "Lease", "Cash", "ACH Payment", "Crypto Payment"
]

# Lista de status de entrega controlados
DELIVERY_STATUSES = [
    "Delivered", "Pending", "In Transit", "Cancelled", "Awaiting Delivery", 
    "Awaiting Pickup", "Pending Approval", "Pending Review", "Shipped", "Awaiting Review"
]

def sanitize_date(val):
    if pd.isna(val): return "INVALID"
    val_str = str(val).strip()
    
    # Remove sufixos ordinais comuns em inglês (st, nd, rd, th) de datas textuais
    val_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', val_str, flags=re.IGNORECASE)
    
    # Padrões de formatos aceitos para tentar conversão
    date_formats = [
        '%Y-%m-%d', '%Y/%m/%dd', '%Y.%m.%d', 
        '%m/%d/%Y', '%m/%d/%y', '%m-%d-%y',
        '%B %d, %Y', '%b %d %Y', '%B %d %Y'
    ]
    
    for fmt in date_formats:
        try:
            dt = datetime.strptime(val_str, fmt)
            # Regra implícita: testar se o ano faz sentido (ex: evitar 2027-06-40 que falha no parse)
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            continue
            
    return "INVALID"

def sanitize_model(val):
    if pd.isna(val): return "INVALID"
    # Apenas garante o Title Case conforme regra do schema
    return str(val).strip().title()

def sanitize_model_year(val):
    if pd.isna(val): return "INVALID"
    val_str = str(val).strip().lower()
    
    # Remove hífens ou espaços (ex: 20-24 -> 2024, 20 24 -> 2024)
    val_str = re.sub(r'[-\s]', '', val_str)
    
    # Tenta converter se for número por extenso
    try:
        # Substitui espaços temporariamente se vier separado por extenso
        text_val = str(val).strip().lower().replace('-', ' ')
        year = w2n.word_to_num(text_val)
    except ValueError:
        # Se falhar, tenta extrair dígitos limpos
        digits = re.sub(r'\D', '', val_str)
        if len(digits) == 4:
            year = int(digits)
        else:
            return "INVALID"
            
    if 1990 <= year <= 2035:
        return int(year)
    return "INVALID"

def text_to_numeric_clean(val_str):
    """Auxiliar para limpar strings de dinheiro e milhas misturadas com texto."""
    val_str = val_str.replace('$', '').replace(',', '').strip().lower()
    # Atalho para o multiplicador 'k'
    multiplier = 1
    if 'k' in val_str:
        multiplier = 1000
        val_str = val_str.replace('k', '')
    
    # Remove termos comuns de moeda/unidade
    val_str = val_str.replace('usd', '').replace('miles', '').replace('mi', '').strip()
    
    # Tenta conversão direta por extenso text_to_num
    try:
        return float(w2n.word_to_num(val_str)) * multiplier
    except ValueError:
        # Extrai apenas o número com ponto decimal se houver
        match = re.search(r'\d+\.?\d*', val_str)
        if match:
            return float(match.group()) * multiplier
    return None

def sanitize_sales_price(val):
    if pd.isna(val): return "INVALID"
    val_str = str(val).strip()
    
    num = text_to_numeric_clean(val_str)
    if num is not None:
        return f"{num:.2f}"
    return "INVALID"

def sanitize_vehicle_mileage(val):
    if pd.isna(val): return "INVALID"
    val_str = str(val).strip().lower()
    
    # Casos de carro novo / zero milhas
    if any(x in val_str for x in ['zero', 'new', 'novo']):
        return 0
        
    is_km = 'km' in val_str
    num = text_to_numeric_clean(val_str)
    
    if num is not None:
        if is_km:
            # 1 km = 0.621371 miles
            num = num * 0.621371
        return int(round(num))
        
    return "INVALID"

def sanitize_payment_method(val):
    if pd.isna(val): return "INVALID"
    val_str = str(val).strip().replace('-', ' ').replace('_', ' ')
    
    # Tenta bater case-insensitively com a lista controlada
    for method in PAYMENT_METHODS:
        if val_str.lower() == method.lower() or val_str.lower().replace(" ", "") == method.lower().replace(" ", ""):
            return method
            
    return val_str.title()  # Se desconhecido, apenas Title Case

def sanitize_city(val):
    if pd.isna(val): return "INVALID"
    # Normaliza preservando pontos (ex: St. Louis) utilizando .title()
    return str(val).strip().title()

def sanitize_state(val):
    if pd.isna(val): return "INVALID"
    val_str = str(val).strip().lower()
    
    if val_str in US_STATES:
        return US_STATES[val_str]
    return "INVALID"

def sanitize_delivery_status(val):
    if pd.isna(val): return "INVALID"
    # Remove pontuações extras (ex: Delivered!!!) e hífens
    val_str = re.sub(r'[!?.#-]', ' ', str(val)).strip().lower()
    # Corrige o typo específico mapeado no schema
    val_str = val_str.replace('deliverd', 'delivered')
    # Junta múltiplos espaços
    val_str = " ".join(val_str.split())
    
    for status in DELIVERY_STATUSES:
        if val_str == status.lower() or val_str.replace(" ", "") == status.lower().replace(" ", ""):
            return status
            
    return "INVALID"

def main():
    # 1. Carregar banco de dados original
    input_file = 'porsche_database.xlsx'
    output_file = 'porsche_database_sanitized.xlsx'
    
    try:
        df = pd.read_excel(input_file)
        print(f"Arquivo '{input_file}' carregado com sucesso!")
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return

    # 2. Processar e inserir as novas colunas imediatamente após suas originais
    # Mapeamento de (Coluna Origem : (Nome Nova Coluna, Função Higienizadora))
    mappings = {
        'sale_date': ('SaleDateSanitized', sanitize_date),
        'porsche_model': ('PorscheModelSanitized', sanitize_model),
        'model_year': ('ModelYearSanitized', sanitize_model_year),
        'sale_price': ('SalesPriceSanitized', sanitize_sales_price),
        'vehicle_mileage': ('VehicleMileageSanitized', sanitize_vehicle_mileage),
        'payment_method': ('PayMethodSanitized', sanitize_payment_method),
        'city': ('CitySanitized', sanitize_city),
        'state': ('StateSanitized', sanitize_state),
        'delivery_status': ('DeliveryStatusSanitized', sanitize_delivery_status)
    }
    
    for src_col, (new_col, func) in mappings.items():
        if src_col in df.columns:
            # Aplica a higienização na série
            sanitized_series = df[src_col].apply(func)
            # Encontra o index da coluna de origem para inserir logo após ela
            loc = df.columns.get_loc(src_col) + 1
            df.insert(loc, new_col, sanitized_series)
        else:
            print(f"Aviso: Coluna esperada '{src_col}' não foi encontrada no arquivo original.")

    # 3. Exportar banco tratado para um novo arquivo Excel
    df.to_excel(output_file, index=False)
    print(f"Higienização concluída com sucesso! Arquivo salvo como: '{output_file}'")

if __name__ == "__main__":
    main()