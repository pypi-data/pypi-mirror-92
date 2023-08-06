def get_symbol(date, month):
    if (month == 12 and date >= 22) or (month == 1 and date <= 19):
        return ["Capricorn", "Ground", "Secluded, shy, faithful, conscientious, ambitious, loyal"]
    elif (month == 1 and date >= 20) or (month == 2 and date <= 18):
        return ["Aquarius", "Water", "Peace lover, clear-sighted, intuitive, loyal, inventive, revolutionary"]
    elif (month == 2 and date >= 19) or (month == 3 and date <= 20):
        return ["The Pisces", "Water", "Empathy, humane, careless, kind, secretive, easygoing, inspiring"]
    elif (month == 3 and date >= 21) or (month == 4 and date <= 19):
        return ["Aries", "Fire", "Warm, enthusiastic, social, emotional, stressed, impulse driven, aggressive"]
    elif(month == 4 and date >= 20) or (month == 5 and date <= 20):
        return ["Taurus", "Ground", "Stubborn, protective, loyal, patient, persistent, stable, practical, realistic"]
    elif (month == 5 and date >= 21) or (month == 6 and date <= 21):
        return ["The Twins", "Air", "Quick, communicative, superficial, curious, independent, brave, impulsive, stressed"]
    elif (month == 6 and date >= 22) or (month == 7 and date <= 22):
        return ["Crab", "Water", "The parent, the protector, the custodian, the faithful, the loyal & sympathetic"]
    elif (month == 7 and date >= 23) or (month == 8 and date <= 22):
        return ["Lion", "Sun", "Magnificent, loving, strong-willed, jealous, leader, faithful, conscientious"]
    elif (month == 8 and date >= 23) or (month == 9 and date <= 22):
        return ["Virgo", "Ground", "Shy, self-aware, analytical, productive, critical, changeable"]
    elif (month == 9 and date >= 23) or (month == 10 and date <= 22):
        return ["Wave", "Air", "Love, charm, indecision, seduction, diplomacy, social skills"]
    elif (month == 10 and date >= 23) or (month == 11 and date <= 21):
        return ["Scorpio", "Water", "Intense, jealous, passionate, quiet, intense, loyal, brave, strong"]
    else:
        return ["Error", "Details: Date and Month must be numerical values. Date and Month must be real dates and months."]


def output_enter():
    print("Choose month. Must be a numerical value.")

    print("1. January")

    print("2. February")

    print("3. March")

    print("4. April")

    print("5. May")

    print("6. June")

    print("7. July")

    print("8. August")

    print("9. September")

    print("10. October")

    print("11. November")

    print("12. December")

    month = int(input('Month: '))

    print("Choose date. Must be a numerical value.")

    date = int(input('Date: '))

    symbol = get_symbol(date, month)

    if symbol[0] != "Error":
        print(f"Symbol: {symbol[0]}")
        print(f"Element: {symbol[1]}")
        print(f"Characteristics: {symbol[2]}")
    else:
        print(symbol)
