import pandas as pd
import chardet
from settings import PATH_TO_DATA_SCORE


with open(PATH_TO_DATA_SCORE, 'rb') as f:
    result = chardet.detect(f.read())
data_score = pd.read_csv(PATH_TO_DATA_SCORE, encoding=result['encoding'])

# Отображаем каждый результат из CSV
for date, score in data_score.sort_values(ascending=False, by= "score").itertuples(index = False):
    score_text = f"{date} - Score: {score}"
    print(score_text)

    # self.scores.sort_values(ascending=False, by= Score)[:7].