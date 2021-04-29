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
        return keanggotaan

    def ReadData(self, loc):
        self.df = pd.read_excel(loc)

    def Fuzzification(self, anggota, x):
        keAnggotaan = self.GenerateFuzzy()
        for i in keAnggotaan.keys():
            if i == anggota:
                for j, data in enumerate(keAnggotaan[i].keys()):
                    b, c = self.keanggotaan[i][j][data]
                    a, d = b - 1, c + 1
                    if b <= x <= c:
                        keAnggotaan[i][data] = 1
                    elif a <= x <= b:
                        keAnggotaan[i][data] = (x-a)/(b-a)
                    elif c <= x <= d:
                        keAnggotaan[i][data] = (d-x)/(d-c)
        return keAnggotaan[anggota]

    def FuzzyDataset(self):
        for i in range(len(self.df)):
            fuzzed = {}
            for j in self.keanggotaan:
                fuzzed[j] = self.Fuzzification(j, self.df[j][i])
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
                    if fuzzed[val][key[j]] < minVal:
                        minVal = fuzzed[val][key[j]]
                if minVal > result[output]:
                    result[output] = minVal
            self.inferenced.append(result)

    def Defuzzification(self):
        for i in self.inferenced:
            w, z = 0, 0
            for output in self.deffuzy.keys():
                w += i[output] * self.deffuzy[output]
                z += i[output]
            self.results.append(w/z)
        self.df['result'] = self.results

    def GetData(self):
        return self.df

    def SaveData(self, fileName):
        tmp = self.df.sort_values(by='result', ascending=False)[:10]
        tmp['id'].to_excel(fileName, engine='openpyxl')
