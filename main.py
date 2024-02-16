from quickstart import retriveSheet
from flask import Flask, render_template

app = Flask(__name__)

sheet = retriveSheet()

p = {
    "nov": {"Jason Ji": 0, "Ryan Ji": 0, "Jenny Pan": 0, "Alex Zeng": 0 , "Henry Zhang": 0},
    "beg": {"Jasper Deng": 0, "Jacob Dong": 0, "Eric Huang": 0, "Marcus Huang": 0, "Dash Jin": 0, "Ariel Li": 0, "Christina Yan": 0, "Sabrina Yan": 0, "Jiasen Yao": 0, "Jonathan Ye": 0, "Daniela Yu": 0, "Danny Yu": 0, "Analise Zeng": 0 , "Emily Zeng": 0, "Chenran Zhao": 0, "William Zhou": 0},
    "int": {"Ziyi Dai": 0, "Oscar Feng": 0, "Max Jia": 0, "Eric Luo": 0, "Samuel Wu": 0, "Ben Ye": 0, "Aiden Yu": 0, "Harris Yu": 0, "Colin Zhou": 0, "William Pan": 0},
}

def get_values(range):
    result = (
        sheet.values()
        .get(spreadsheetId="1wFp77E5wPOhHN2ttAH2gT8qbycE9iFg_vIYkRT_apLA", range=range)
        .execute()
    )['values']
    return result

def round_pairings(category, round):
    match category:
        case "nov":
            match round:
                case 1:
                    pairings = get_values("A3:B5")
                case 2:
                    pairings = get_values("E3:F5")
                case 3:
                    pairings = get_values("I3:J5")
                case 4:
                    pairings = get_values("M3:N5")
                case 5:
                    pairings = get_values("Q3:R5")
        case "beg":
            match round:
                case 1:
                    pairings = get_values("A10:B17")
                case 2:
                    pairings = get_values("E10:F17")
                case 3:
                    pairings = get_values("I10:J17")
                case 4:
                    pairings = get_values("M10:N17")
                case 5:
                    pairings = get_values("Q10:R17")
        case "int":
            match round:
                case 1:
                    pairings = get_values("A22:B26")
                case 2:
                    pairings = get_values("E22:F26")
                case 3:
                    pairings = get_values("I22:J26")
                case 4:
                    pairings = get_values("M22:N26")
                case 5:
                    pairings = get_values("Q22:R26")
    return pairings

def setScores():
    temp = {
        "nov": {"Jason Ji": 0, "Ryan Ji": 0, "Jenny Pan": 0, "Alex Zeng": 0 , "Henry Zhang": 0},
        "beg": {"Jasper Deng": 0, "Jacob Dong": 0, "Eric Huang": 0, "Marcus Huang": 0, "Dash Jin": 0, "Ariel Li": 0, "Christina Yan": 0, "Sabrina Yan": 0, "Jiasen Yao": 0, "Jonathan Ye": 0, "Daniela Yu": 0, "Danny Yu": 0, "Analise Zeng": 0 , "Emily Zeng": 0, "Chenran Zhao": 0, "William Zhou": 0},
        "int": {"Ziyi Dai": 0, "Oscar Feng": 0, "Max Jia": 0, "Eric Luo": 0, "Samuel Wu": 0, "Ben Ye": 0, "Aiden Yu": 0, "Harris Yu": 0, "Colin Zhou": 0, "William Pan": 0},
    }
    for i, l in enumerate(["C", "G", "K", "O", "S"]):
        #nov scores
        results = get_values(f"{l}3:{l}5")
        nov_pairings = round_pairings('nov', i+1)
        for j, r in enumerate(results):
            if r != ["P"]:
                w = float(r[0].split('-')[0])
                b = float(r[0].split('-')[1])
                if nov_pairings[j][0] != "BYE":
                    temp['nov'][nov_pairings[j][0]] += w
                if nov_pairings[j][1] != "BYE":
                    temp['nov'][nov_pairings[j][1]] += b
        #beg scores
        results = get_values(f"{l}10:{l}17")
        try:
            beg_pairings = round_pairings('beg', i+1)
            for j, r in enumerate(results):
                if r != ["P"]:
                    w = float(r[0].split('-')[0])
                    b = float(r[0].split('-')[1])
                    if beg_pairings[j][0] != "BYE":
                        temp['beg'][beg_pairings[j][0]] += w
                    if beg_pairings[j][1] != "BYE":
                        temp['beg'][beg_pairings[j][1]] += b
        except:
            pass
        #int scores
        results = get_values(f"{l}22:{l}26")
        try:
            int_pairings = round_pairings('int', i+1)
            for j, r in enumerate(results):
                if r != ["P"]:
                    w = float(r[0].split('-')[0])
                    b = float(r[0].split('-')[1])
                    if int_pairings[j][0] != "BYE":
                        temp['int'][int_pairings[j][0]] += w
                    if int_pairings[j][1] != "BYE":
                        temp['int'][int_pairings[j][1]] += b
        except:
            pass
    for c in temp:
        for i in temp[c]:
            p[c][i] = temp[c][i]
            

def rankings(category):
    return {k: v for k, v in sorted(p[category].items(), key=lambda item: item[1])[::-1]}

@app.route('/')
def index():
    nr = int(get_values("U2")[0][0])
    br = int(get_values("U3")[0][0])
    ir = int(get_values("U4")[0][0])
    nov_pairings = round_pairings('nov', nr)
    beg_pairings = round_pairings('beg', br)
    int_pairings = round_pairings('int', ir)
    return render_template('index.html', nov_pairings=nov_pairings, beg_pairings=beg_pairings, int_pairings=int_pairings, nr=nr, br=br, ir=ir)

@app.route('/standings')
def standings():
    setScores()
    nov_rankings = rankings("nov")
    beg_rankings = rankings("beg")
    int_rankings = rankings("int")
    return render_template('standings.html', nov_rankings=nov_rankings, beg_rankings=beg_rankings, int_rankings=int_rankings)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)