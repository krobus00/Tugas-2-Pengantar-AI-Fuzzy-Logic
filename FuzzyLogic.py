import pandas as pd


class FuzzyLogic():
    def __init__(self, config):
        self.df = []
        self.keanggotaan = config['keanggotaan']
        self.fuzzied = []
        self.rules = {}
        self.inferenced = []
        self.results = []
        self.rules = config['rules']
        self.deffuzy = config['deffuzy']

    def GenerateFuzzy(self):
        data = self.keanggotaan
        keanggotaan = {}
        for i in data:
            keanggotaan[i] = {}
            for j in data[i]:
                k = list(j.keys())[0]
                keanggotaan[i][k] = 0
        # {
        # 'pelayanan': {'sangat buruk': 0, 'buruk': 0, 'baik': 0, 'sangat baik': 0},
        # 'makanan': {'tidak enak': 0, 'cukup enak': 0, 'enak': 0, 'sangat enak': 0}
        # }
        return keanggotaan

    def ReadData(self, loc):
        self.df = pd.read_excel(loc)

    def Fuzzification(self, anggota, x):
        keAnggotaan = self.GenerateFuzzy()
        for j, data in enumerate(keAnggotaan[anggota].keys()):
            b, c = self.keanggotaan[anggota][j][data]
            a, d = b - 1, c + 1
            if b <= x <= c:
                keAnggotaan[anggota][data] = 1
            elif a < x < b:
                keAnggotaan[anggota][data] = (x-a)/(b-a)
            elif c < x <= d:
                keAnggotaan[anggota][data] = (d-x)/(d-c)
        # {'sangat buruk': 1, 'buruk': 0, 'baik': 0, 'sangat baik': 0}
        # {'tidak enak': 0, 'cukup enak': 0, 'enak': 1, 'sangat enak': 0.0}
        return keAnggotaan[anggota]

    def FuzzyDataset(self):
        for i in range(len(self.df)):
            fuzzed = {}
            for j in self.keanggotaan:
                fuzzed[j] = self.Fuzzification(j, self.df[j][i])
            # {'pelayanan': {'sangat buruk': 0, 'buruk': 0, 'baik': 1, 'sangat baik': 0},
            # 'makanan': {'tidak enak': 0, 'cukup enak': 0, 'enak': 1, 'sangat enak': 0.0}}
            self.fuzzied.append(fuzzed)

    def Inference(self):
        for fuzzed in self.fuzzied:
            result = {}
            keys = []
            for i in self.rules:
                keys.append(i)
                result[self.rules[i]] = 0
            for key in keys:
                output = self.rules[key]
                minVal = fuzzed[list(fuzzed.keys())[0]][key[0]]
                for j, val in enumerate(fuzzed):
                    minVal = min(minVal, fuzzed[val][key[j]])
                result[output] = max(minVal, result[output])
            # {'tidak rekomen': 0, 'cukup rekomen': 0, 'rekomen': 1, 'sangat rekomen': 0}
            self.inferenced.append(result)

    def Defuzzification(self):
        for i in self.inferenced:
            atas, bawah = 0, 0
            for output in self.deffuzy.keys():
                atas += i[output] * self.deffuzy[output]
                bawah += i[output]
            self.results.append(atas/bawah)
        self.df['result'] = self.results

    def GetData(self):
        return self.df

    def SaveData(self, fileName):
        tmp = self.df.sort_values(by='result', ascending=False)[:10]
        tmp['id'].to_excel(fileName, engine='openpyxl', index=False)
