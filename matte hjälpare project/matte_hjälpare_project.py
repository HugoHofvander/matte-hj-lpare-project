import math
import requests

def convert_sek(sek, target_currency):
    url = "https://api.frankfurter.dev/v2/rates?base=SEK"
    target_currency = target_currency.upper()
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        rate = None
        if isinstance(data, dict):
            rates = data.get("rates")
            if isinstance(rates, dict):
                rate = rates.get(target_currency)
            elif isinstance(rates, list):
                rate = next((item.get("rate") for item in rates if item.get("quote") == target_currency), None)
        elif isinstance(data, list):
            rate = next((item.get("rate") for item in data if item.get("quote") == target_currency), None)

        if rate is None:
            print(f"Valuta '{target_currency}' hittades inte i API-svaret.")
            return None, None

        return sek * float(rate), float(rate)

    except requests.RequestException as e:
        print("Nätverksfel:", e)
        return None, None
    except (ValueError, TypeError) as e:
        print("Fel vid tolkning av API-svaret:", e)
        return None, None


def parse_eur_rate_from_json(json_data):
    if isinstance(json_data, dict) and "rates" in json_data:
        return json_data["rates"].get("EUR")
    if isinstance(json_data, list):
        return next((item.get("rate") for item in json_data if item.get("quote") == "EUR"), None)
    return None


print("====================================")
print("VÄLKOMMEN TILL MATTE 1C-HJÄLPAREN!")
print("====================================\n")

aktiv = True

while aktiv:
    print("\n--- HUVUDMENY ---")
    print("1. Procentuell förändring & förändringsfaktor")
    print("2. Ränte beräkning")   
    print("3. Räta linjens ekvation (k-värde)")
    print("4. Pythagoras sats")
    print("5. Potensberäkning (Ränte-på-ränta / Tillväxt)")
    print("6. Sannolikhet (Oberoende händelser i flera steg)")
    print("7. Valutaväxling (SEK till EUR)")
    print("8. Avbetalning & Jämförelsepris")
    print("9. Avsluta programmet")
    
    val = input("\nVälj ett alternativ: ")
    
    if val == "1":
        print("\n--- PROCENT & FÖRÄNDRINGSFAKTOR ---")
        gammalt = float(input("Skriv in det ursprungliga värdet: "))
        nytt = float(input("Skriv in det nya värdet: "))
        ff = nytt / gammalt
        procent = (ff - 1) * 100
        print(f"\nResultat:\nFörändringsfaktor: {ff:.2f}")
        if procent > 0:
            print(f"Det är en ökning med {procent:.1f}%")
        elif procent < 0:
            print(f"Det är en minskning med {abs(procent):.1f}%")
        else:
            print("Ingen förändring har skett (0%).")
            
    elif val == "2":
        print("\n--- RÄNTEBERÄKNING ---")
        print("Vilken typ av ränta är det?")
        print("1. Årsränta (%)")
        print("2. Månadsränta (%)")

        r_val = input("Välj (1-2): ")

        lan = float(input("Lånebelopp (kr): "))
        ranta_procent = float(input("Räntesats (%): "))
        tid_manader = int(input("Lånets löptid (antal månader): "))
        upplagningsavgift = float(input("Upplägningsavgift (kr, 0 om ingen): "))
        aviseringsavgift = float(input("Aviseringsavgift (kr, 0 om ingen): "))
        if r_val == "1":
            manadsranta_procent = ranta_procent / 12
        elif r_val == "2":
            manadsranta_procent = ranta_procent
        else:
            print("Ogiltigt val, sätter standard till årsränta.")
        manadsranta_procent = ranta_procent / 12

        manadsranta_kr = lan * (manadsranta_procent) / 100
        total_ranta = manadsranta_kr * tid_manader
        totala_avgifter = upplagningsavgift + (aviseringsavgift * tid_manader)
        total_extra_kostnad = total_ranta + totala_avgifter

        print("\n--- RESULTAT ---")
        print(f"Räntekostnad per månad : {manadsranta_kr:.2f} kr")
        print(f"Total räntekostnad under {tid_manader} månader: {total_ranta:.2f} kr")
        print(f"Total avigfter: {totala_avgifter:.2f} kr")
        print(f"Total extra kostnad utöver lånet: {total_extra_kostnad:.2f} kr")

    elif val == "3":
        print("\n--- RÄTA LINJENS EKVATION ---")
        x1 = float(input("x1: "))
        y1 = float(input("y1: "))
        x2 = float(input("x2: "))
        y2 = float(input("y2: "))
        if (x2 - x1) == 0:
            print("\nFel: Division med noll (lodrät linje).")
        else:
            k = (y2 - y1) / (x2 - x1)
            print(f"\nResultat:\nLinjens k-värde (lutning) är: {k:.2f}")
            
    elif val == "4":
        print("\n--- PYTHAGORAS SATS ---")
        print("Vad vill du räkna ut?\n1. Hypotenusan (långa sidan)\n2. En katet (korta sidan)")
        p_val = input("Välj (1-2): ")
        if p_val == "1":
            a = float(input("Längd på katet a: "))
            b = float(input("Längd på katet b: "))
            c = math.sqrt(a**2 + b**2)
            print(f"\nHypotenusans längd är: {c:.2f}")
        elif p_val == "2":
            c = float(input("Längd på hypotenusan c: "))
            a = float(input("Längd på kända kateten a: "))
            if c <= a:
                print("\nFel: Hypotenusan måste vara längre än kateten.")
            else:
                b = math.sqrt(c**2 - a**2)
                print(f"\nDen andra katetens längd är: {b:.2f}")

    elif val == "5":
        print("\n--- POTENSBERÄKNING (Tillväxt) ---")
        start = float(input("Startvärde (t.ex. pengar på banken): "))
        procent_forandring = float(input("Årlig procentuell förändring (t.ex. 4 eller -2): "))
        ar = int(input("Antal år: "))
        ff = 1 + (procent_forandring / 100)
        slutvarde = start * (ff ** ar)
        print(f"\nResultat efter {ar} år: {slutvarde:.3f}")

    elif val == "6":
        print("\n--- SANNOLIKHET (Flera steg) ---")
        p = float(input("Sannolikhet för händelsen i ett steg (i decimalform, t.ex. 0.5): "))
        steg = int(input("Antal upprepningar/steg (t.ex. kasta slant 3 gånger): "))
        if 0 <= p <= 1:
            total_p = p ** steg
            print(f"\nSannolikheten att det händer {steg} gånger i rad är: {total_p*100:.2f}% ({total_p:.4f})")
        else:
            print("\nFel: Sannolikhet måste vara mellan 0 och 1.")
            
    elif val == "7":
        print("\n--- VALUTAVÄXLING (SEK till EUR) ---")
        kronor = float(input("Hur många SEK vill du växla?: "))
        
        valuta_val = input("Vilken valuta vill du växla till? (EUR, USD, DKK, GBP etc): ").upper()

        resultat, kurs = convert_sek(kronor, valuta_val)

        if resultat is not None:
            print(f"{kronor} SEK motsvarar {resultat:.2f} {valuta_val} (Kurs: 1 SEK = {kurs:.4f} {valuta_val})")


            
    elif val == "8":
        print("\n--- AVBETALNINGSKÖP ---")  
        kontant = float(input("Kontantpris (kr): "))
        manadskostnad = float(input("Månadsbelopp (kr/mån): "))
        manader = int(input("Antal månader: "))
        aviseringsavgift = float(input("Aviseringsavgift per månad (kr): "))
        upplagning = float(input("Uppläggningsavgift (kr): "))

        total_avbetalning = (manadskostnad + aviseringsavgift) * manader + upplagning
        skillnad = total_avbetalning - kontant

        print(f"\nResultat:")
        print(f"Total kostnad vid avbetalning: {total_avbetalning:.2f} kr")
        print(f"Mellanskillnad (extra kostnad): {skillnad:.2f} kr")

    elif val == "9":
        print("\nTack för den här gången! Lycka till med Matte 1c!")
        aktiv = False
    else:
        print("\nOgiltigt val, försök igen.")

