# emotext

emotext is a python library to analize sentiment it can be negative (0), positive (4) or neutral (2).

### Installation

```bash
pip3 install emotext
```
### Instructions for use

```python
from emotext import SentimentProbability

prob = SentimentProbability()
prob.fit("positive_words.txt", "negative_words.txt", "stop_words.txt")

pred = prob.predict("hari ini sangat indah sekali")
print(pred)

# outout
# 4 or positive
```
| name | description |
| ---- | ----------- |
| positive_words.txt | put all the positive words on this file it can be in any language. in this documentation i use indonesian language,so the positive words like example : optimis, kuat, menyenangkan and etc |
| negative_words.txt | all the negative words, example : mengganggu, menindas, kejam and etc |
| stop_words.txt | all the stop words, example : yang, di, dan itu, etc |

###### *note
all of those file wrote in indonesian language, it possible to change with any language. just put all of the word into .txt file and make sure 1 line for 1 word, look at example below :

```python
# do
optimis
kuat
menyenangkan

# don't
optimis kuat menyenangkan
```

If you are indonesian i have created all of those file just look at folder **data**

### warning
You don't have to worry about noise on your text like

- omoji : 🥸 😘 🤬
- punctuation : #?!^&*%@, etc

all of that will be removed automatically and if you grab the data from **twitter** it automatically remove username and hastag
