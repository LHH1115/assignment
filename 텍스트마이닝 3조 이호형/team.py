import pandas as pd
import konlpy
import requests as req
import re

# url = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code=74977&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=3'
text = ''
for i in range(70):
    text += req.get(
        f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code=74977&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={i}').text

# print(text)
comment = re.findall(
    r'<span id="_filtered_ment_.+?">\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(.+?)\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t</span>',
    text, re.DOTALL)
# <span id="_filtered_ment_.+?">.+?(.+?).+?</span>
# print(comment)

# print(len(comment))

def listToString(str_list):
    result = ""
    for s in str_list:
        result += s + " "
    return result.strip()

comment = listToString(comment)

# comment = re.sub('[^가-힣a-zA-Z]', ' ', comment)
comment = re.sub('[^가-힣]', ' ', comment)
# print(comment)

# 불용어 처리
stop_words = ["한번", "영화", "보고", "미가", "역시", "상미", "그냥", "동안", "하나", "정도", "아바타"]
for word in stop_words:
    comment = re.sub(word, ' ', comment)

# 동의어 처리
old_word = ['진짜', '정말', '제임스', '카메룬']
new_word = ['최고', '최고', '카메론', '카메론']

for i in range(len(old_word)):
    comment = re.sub(old_word[i], new_word[i], comment)

# kkma = konlpy.tag.Kkma()
# comment_kkma = kkma.nouns(comment)
# print(comment_kkma)

# print('-'*50)

okt = konlpy.tag.Okt()
comment_okt = okt.nouns(comment)
# print(comment_okt)

# print('-'*50)

# komo = konlpy.tag.Komoran()
# comment_komo = komo.nouns(comment)
# print(comment_komo)

df_word = pd.DataFrame({'word': comment_okt})
df_word['count'] = df_word['word'].str.len()
df_word = df_word[df_word['count'] >= 2]

df_word.to_csv("../Data/avatar_okt.csv", mode='w', header=True)
print("저장 완료.")
