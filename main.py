from FuzzyLogic import FuzzyLogic

config = {
    'keanggotaan': {
        'pelayanan': [{'sangat buruk': [1, 20]}, {'buruk': [21, 50]}, {'baik': [51, 70]}, {'sangat baik': [71, 100]}],
        'makanan': [{'tidak enak': [1, 2]}, {'cukup enak': [3, 5]}, {'enak': [6, 7]}, {'sangat enak': [8, 10]}]
    },
    'rules': {
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
    },
    'deffuzy': {'tidak rekomen': 0, "cukup rekomen": 50,
                "rekomen": 75, "sangat rekomen": 100}
}
fl = FuzzyLogic(config)
fl.ReadData('./restoran.xlsx')
fl.FuzzyDataset()
fl.Inference()
fl.Defuzzification()
print((fl.GetData().sort_values(by='result', ascending=False)[:10]))
fl.SaveData('peringkat.xls')
