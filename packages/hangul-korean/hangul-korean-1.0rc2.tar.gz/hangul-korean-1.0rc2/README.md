# Package **hangul-korean**
Hangul is the alphabet for the Korean language. **hangul-korean** is a package
which currently contains a module for segmenting words in written Korean texts.

# Segmentation of Korean Words 한국어 낱말 분절
Written Korean texts do employ white space characters. However, more often than not,
Korean words occur in a text concatenated immediately to adjacent words without
an intervening space character. This low degree of separation of words from
each other in writing is due somewhat to an abundance of what linguists call "endoclitics" 
in the language.

As the language has been subjected to principled and rigorous study for a few
decades, the issue of which strings of sounds, or letters, are words and which are
not, has been settled among a small group of selected linguists. This kind of
advancement has not been propagated to the general public yet, and nlp
engineers working on Korean cannot but make do with whatever inconsistent
grammars they happen to have access to. Thus, a major source of difficulty in
developing competent Korean text processors has been, and still is, the notion of a word
as the smallest syntactic unit.

# The **WordSegmenter** class
The module **tokenizer** in this package defines the class **WordSegmenter**.
It has, among other things, the following methods:
* __init__(modelFile, word2idxFile)
* infile(fileName)
* outfile(fileName)
* inputAsString(aStr)
* doSegment()
* segmentedOutput()

After creating a WordSegmenter object, say wseg, give it a file or a string and then
issue wseg.doSegment(). The word-segmented text will be in a file (if specified
with outfile()) or in an instance variable accessible via segmentedOutput().

# Typical use

```python
from hangul.tokenizer import WordSegmenter

wsg = WordSegmenter()
aPassage = "어휴쟤가 왜저래? 정말우스워죽겠네"  # 문자열을 함수 inputAsString의
wsg.inputAsString (aPassage)                    # 매개변인으로 주거나
# inFile = "tobesegmented"        # 파일 안에 담긴 글을 낱말분절할 때에는 
# wsg.infile(inFile)              # 그 파일 이름을 함수 infile에 넘긴다.
# wsg.outfile("output.txt")
wsg.doSegment() 
# infile()이 사용되면 낱말 분절 된 글이 적힌 파일이 생겨 난다.
# 이 파일은 함수 outfile()로 지정될 수 있고 디폴트 값은 "segmented_yyddd_hhmm.txt"이다.
# with open("segmented_yyddd_hhmm.txt", "r") as f:
#   lines = f.readlines()
# for aLine in lines:
#   print(aLine)
# inputAsString()이 사용된 경우에는
print(wsg.segmentedOutput)
```

# Forms of a verb are not analyzed into morphs
The lexical category verb is inflected in hundreds (or thousands) of ways in
the language and it is the only category that inflects. We do not analyze
a form of a verb into its morphs. Such an analysis is best reserved for
a separate component of inflectional morphology and is certainly required in
order to do syntactic analyses of various kinds.

# Slim size of the model
The model this package uses is of a very compact size: it is merely ten
megabytes long.

# Forthcoming in the package
The next version of this package might well contain a POS tagger. A higher
F-measure of the word segmentation system (which currently is 0.970
while that of the open access model is somewhat lower) is something we would 
like to see as well.

# Status of papers that describe this package
A draft is to be submitted to a journal, which describes the way the model for
this package is obtained.
