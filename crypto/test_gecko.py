import requests
from datetime import datetime
import pytz

def get_crypto_to_nok_price(crypto_symbol: str, date: str) -> float:
    """
    Henter historisk kurs for en kryptovaluta i NOK på en gitt dato.

    Args:
        crypto_symbol (str): Symbol for kryptovaluta (f.eks. 'btc' for Bitcoin).
        date (str): Dato i formatet 'YYYY-MM-DD'.

    Returns:
        float: Kursen i NOK på den spesifiserte datoen.
    """
    base_url = "https://api.coingecko.com/api/v3/coins"
    
    # Konverter dato til UNIX-timestamp
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    timestamp = int(date_obj.replace(tzinfo=pytz.UTC).timestamp())
    
    # Bygg URL for API-forespørsel
    url = f"{base_url}/{crypto_symbol}/history"
    params = {
        "date": date_obj.strftime("%d-%m-%Y"),
        "localization": "false",
    }
    
    # Gjør forespørselen
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise ValueError(f"Feil ved henting av data: {response.status_code} - {response.json()}")
    
    data = response.json()
    try:
        nok_price = data["market_data"]["current_price"]["nok"]
        return nok_price
    except KeyError:
        raise ValueError(f"Ingen prisdata funnet for {crypto_symbol} på {date}.")

crypto = "bitcoin"  # Eller "ethereum", "ripple", osv.
dato = "2024-07-01"

try:
    pris = get_crypto_to_nok_price(crypto, dato)
    print(f"Kursen for {crypto} i NOK på {dato} var {pris:.2f} NOK.")
except ValueError as e:
    print(f"Feil: {e}")
