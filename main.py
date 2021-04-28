import pandas as pd

df = pd.read_excel("./restoran.xlsx")


def Fuzzy(anggota, x):
    keAnggotaan = {
        'pelayanan': {
            'sangat buruk': 0,
            'buruk': 0,
            'baik': 0,
            'sangat baik': 0
        },
        'makanan': {
            'tidak enak': 0,
            'cukup enak': 0,
            'enak': 0,
            'sangat enak': 0
        }
    }
    if anggota == "pelayanan":
        if x <= 20:
            keAnggotaan['pelayanan']['sangat buruk'] = 1
        elif 20 < x < 21:
            keAnggotaan['pelayanan']['sangat buruk'] = -(x-21) / (21-20)

        if 21 <= x <= 50:
            keAnggotaan['pelayanan']['buruk'] = 1
        elif 20 < x < 21:
            keAnggotaan['pelayanan']['buruk'] = (x-20)/(21-20)
        elif 50 < x < 51:
            keAnggotaan['pelayanan']['buruk'] = -(x-51)/(51-50)

        if 51 <= x <= 70:
            keAnggotaan['pelayanan']['baik'] = 1
        elif 50 < x < 51:
            keAnggotaan['pelayanan']['baik'] = (x-50)/(50-51)
        elif 70 < x < 71:
            keAnggotaan['pelayanan']['baik'] = -(x-71)/(71-50)

        if x >= 71:
            keAnggotaan['pelayanan']['sangat baik'] = 1
        elif 70 < x < 71:
            keAnggotaan['pelayanan']['sangat baik'] = -(x-70) / (71-70)
        return keAnggotaan['pelayanan']
    elif anggota == 'makanan':
        if x <= 2:
            keAnggotaan['makanan']['tidak enak'] = 1
        elif 2 < x < 3:
            keAnggotaan['makanan']['tidak enak'] = -(x-3) / (3-2)

        if 3 <= x <= 5:
            keAnggotaan['makanan']['cukup enak'] = 1
        elif 2 < x < 3:
            keAnggotaan['makanan']['cukup enak'] = (x-2)/(3-2)
        elif 5 < x < 6:
            keAnggotaan['makanan']['cukup enak'] = -(x-6)/(6-5)

        if 6 <= x <= 7:
            keAnggotaan['makanan']['enak'] = 1
        elif 5 < x < 6:
            keAnggotaan['makanan']['enak'] = (x-5)/(5-6)
        elif 7 < x < 8:
            keAnggotaan['makanan']['enak'] = -(x-8)/(8-5)

        if x >= 8:
            keAnggotaan['makanan']['sangat enak'] = 1
        elif 7 < x < 8:
            keAnggotaan['makanan']['sangat enak'] = -(x-7) / (8-7)
        return keAnggotaan['makanan']


fuzzied = []

for i in range(len(df)):
    fuzzed = {'pelayanan': 0, 'makanan': 0}

    fuzzed['pelayanan'] = Fuzzy('pelayanan', df['pelayanan'][i])
    fuzzed['makanan'] = Fuzzy('makanan', df['makanan'][i])

    fuzzied.append(fuzzed)

rules = {
    ('sangat buruk', 'tidak enak'): 'tidak rekomen',
    ('sangat buruk', 'cukup enak'): 'tidak rekomen',
    ('sangat buruk', 'enak'): 'tidak rekomen',
    ('sangat buruk', 'sangat enak'): 'tidak rekomen',
    ('buruk', 'tidak enak'): 'tidak rekomen',
    ('buruk', 'cukup enak'): 'tidak rekomen',
    ('buruk', 'enak'): 'tidak rekomen',
    ('buruk', 'sangat enak'): 'cukup rekomen',
    ('baik', 'tidak enak'): 'tidak rekomen',
    ('baik', 'cukup enak'): 'cukup rekomen',
    ('baik', 'enak'): 'rekomen',
    ('baik', 'sangat enak'): 'sangat rekomen',
    ('sangat baik', 'tidak enak'): 'tidak rekomen',
    ('sangat baik', 'cukup enak'): 'cukup rekomen',
    ('sangat baik', 'enak'): 'rekomen',
    ('sangat baik', 'sangat enak'): 'sangat rekomen',
}


def inference(fuzziedData):
    result = {'tidak rekomen': 0, "cukup rekomen": 0,
              "rekomen": 0, "sangat rekomen": 0}
    keys = [(pelayanan, makanan) for pelayanan in fuzziedData['pelayanan'].keys()
            for makanan in fuzziedData['makanan'].keys()]

    for key in keys:
        output = rules[key]
        minValue = min(
            fuzziedData['pelayanan'][key[0]], fuzziedData['makanan'][key[1]])
        if minValue > result[output]:
            result[output] = minValue
    return result


inferenced = [inference(fuzzed) for fuzzed in fuzzied]

deffuzy = {'tidak rekomen': 0, "cukup rekomen": 50,
           "rekomen": 75, "sangat rekomen": 100}


def defuzzification(inferences, deffuzy):
    w, z = 0, 0
    for output in deffuzy.keys():
        w += inferences[output] * deffuzy[output]
        z += inferences[output]
    return w/z


final = []
for i in inferenced:
    final.append(defuzzification(i, deffuzy))
df['result'] = final

dfFinal = df.sort_values(by='result', ascending=False)[:10]
print("RESULT")
print(dfFinal)
print("RESULT SAVE (peringkat.xls)")
dfFinal['id'].to_excel('peringkat.xls', engine='openpyxl')
