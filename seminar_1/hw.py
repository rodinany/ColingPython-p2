from multiprocessing import Process, Pool
import os
import pandas as pd
from razdel import tokenize
from pymorphy2 import MorphAnalyzer

# В данном задании необходимо будет реализовать параллельную обработку и сохранение текстов в вашу файловую систему.

# Подготовка:
# Загрузите корпус ria.csv с помощью команды: wget https://github.com/ods-ai-ml4sg/proj_news_viz/releases/download/data/ria.csv.gz
# Разахривируйте корпус (или считывайте сразу с декомпрессором в pandas)
# Установите библиотеки pandas, pymorphy2 и razdel

# Логика программы: функция main() -- точка входа данного скрипта.
# В ней вы считываете корпус в виде csv таблицы,выделяете темы и стартуете процессы.
# Нас интересуют только новости из следующих категорий:'В мире', 'Происшествия', 'Общество', 'Экономика', 'РИА Наука', 'Политика', 'Россия', 'Безопасность'
# После выделения тем необходимо заранее создать 8 директорий (по одной на тему), в которые вы будете складывать соответствующие новости.
# За это будет отвечать функция make_dirs,которая с помощью библиотеки os проверяет наличие переданных в нее директорий, и, если их нет, создаёт их.
# Затем создаётся pool процессов, который применяет функцию process к каждой строчке датасета (в map() можно передать, например, df.iterrows() для этого).
# Функция process(row) вызывает функцию preprocess(), а затем сохраняет полученный результат с помощью функции save().
# Функция preprocess() токенизирует текст с помощью razdel.tokenize(), лемматизирует только строки, проходящие проверку str.isalpha() и конкатенирует через пробел.
# Конечный вид output должен выглядеть как-то так:
# |- Безопасность
#   |- 1543457829.txt
#   |- 1547480072.txt
#   |- .
#   |- .
# |- В мире
#   |- 1543....txt
#   |- 1543....txt
#   |- .
#   |- .
# Имя файлов берём из url

m = MorphAnalyzer()


def make_dirs(names):
    try:
        os.mkdir('C:/Users/rodin/PycharmProjects/ColingPython-p2/seminar_1/news'+f'/{names}')
    except:
        print('already existing directory')


def preprocess(text):
    tokens = list(tokenize(text))
    tokens_list = [_.text for _ in tokens]
    lemma_list = []
    for i in tokens_list:
        if i.isalpha():
            p = m.parse(i)[0]
            p = p.normal_form
            lemma_list.append(p)
    lem_text = ' '.join(lemma_list)
    return lem_text


def save(text, topic, url):
    with open(os.path.abspath(os.getcwd())+r'\news'+rf'\{topic}'+rf'\{url}'+'.txt',
              "w", encoding='utf-8') as news:
        news.write(text)


def process(row):
    text = row[1]['text']
    save(preprocess(text), row[1]['topics'], row[1]['url'].split('/')[-1].split('.')[0])


def main():
    df = pd.read_csv('ria.csv', encoding='utf-8')
    topics = ['В мире', 'Происшествия', 'Общество', 'Экономика', 'РИА Наука', 'Политика', 'Россия', 'Безопасность']
    rslt_df = df.loc[df['topics'].isin(topics)]
    try:
        os.mkdir('C:/Users/rodin/PycharmProjects/ColingPython-p2/seminar_1/news')
    except:
        print('already existing directory')
    for i in topics:
        make_dirs(i)
    with Pool(4) as pool:
        pool.map(process, rslt_df.iterrows())
    for i in topics:
        print(i)
        for j in os.listdir(os.getcwd()+r'\news'+rf'\{i}'):
            print(f'\t{j}')


if __name__ == '__main__':
    main()
