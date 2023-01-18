import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import PIL

df_word = pd.read_csv("../Data/avatar_okt.csv")
df_word = df_word[['word', 'count']]

df_word = df_word.groupby('word', as_index=False) \
    .agg(n=("word", "count")) \
    .sort_values("n", ascending=False)

top20 = df_word.head(20)
print(top20)

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
# sns.barplot(data=top20,x='n',y='word')
# plt.show()

font = '../Data/DoHyeon-Regular.ttf'
dic_word = df_word.set_index('word').to_dict()['n']

icon = PIL.Image.open('../Data/avatar.png')

img = PIL.Image.new('RGB', icon.size, (255, 255, 255))
img.paste(icon, icon)
img = np.array(img)

wc = WordCloud(random_state=1234,
               font_path=font,
               width=400,
               height=400,
               background_color='white',
               mask=img,
               colormap='inferno')

img_wordcloud = wc.generate_from_frequencies(dic_word)

plt.figure(figsize=(10, 10))
plt.axis('off')
plt.imshow(img_wordcloud)
plt.show()