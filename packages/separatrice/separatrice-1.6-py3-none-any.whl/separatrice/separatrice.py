import re
import pymorphy2
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

introductory_phrases = ['по-моему','например','в самом деле','само собой разумеется','по всей вероятности','так или иначе','что ещё лучше','как на беду','что ещё хуже','не дай бог','того и гляди','по правде сказать','надо правду сказать','если правду сказать','сказать по чести','между нами говоря','нечего зря говорить','в сущности говоря','с точки зрения','как говорили в','на мой взгляд','к тому же','в довершении всего','с одной стороны','с другой стороны','к слову сказать','как бы сказать','если можно так','по меньшей мере','по крайней мере','в той или','в значительной мере','как и всегда','как это бывает','как это случается','как это случается','можете себе представить','если хочешь знать','что ещё важнее','что ещё существенней','на момент данный','без сомнения','само собой','как кажется','как видно','может быть','должно быть','надо полагать','некоторым образом','в каком','то смысле','если хотите','к счастью','на счастье','к радости','на радость','к удовольствию','что хорошо','к несчастью','по несчастью','к сожалению','к стыду','к прискорбию','к досаде','на беду','как нарочно','грешным делом','что обидно','к удивлению','удивительное дело','к изумлению','странное дело','непонятное дело','неровен час','чего доброго','по совести','по справедливости','по сути','по существу','по душе','по правде','смешно сказать','кроме шуток','по сообщению','по мнению','по словам','по выражению','по слухам','по пословице','по преданию','как слышно','как думаю','как считаю','как помню','как говорят','как считают','как известно','как указывалось','как оказалось','таким образом','к примеру','в частности','кроме того','между прочим','в общем','сверх того','стало быть','кстати сказать','одним словом','другими словами','иначе говоря','прямо говоря','грубо говоря','собственно говоря','короче говоря','лучше сказать','прямо сказать','проще сказать','так сказать','что называется','иной степени','по обыкновению','по обычаю','как водится','видишь ли','знаешь ли','помнишь ли','понимаешь ли','веришь ли','представьте себе','поверишь ли','не поверишь','сделайте милость','что важно','что существенно']

class Separatrice:
  def __init__(self):
    self.alphabets= "([А-Яа-я])"
    self.acronyms = "([А-Яа-я][.][А-Яа-я][.](?:[А-Яа-я][.])?)"
    self.prefixes = "(Mr|Mrs|Ms|акад|чл.-кор|канд|доц|проф|ст|мл|ст. науч|мл. науч|рук|тыс|млрд|млн|кг|км|м|мин|сек|ч|мл|нед|мес|см|сут|проц)[.]"
    self.starters = "(Mr|Mrs|Ms|Dr)"
    self.websites = "[.](com|net|org|io|gov|ru|xyz|ру)"
    self.suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    self.conjs = '(чтобы|когда|несмотря на то что|вопреки|а также|либо|но|зато|а|тогда|а то|так что|чтоб|затем|дабы|коль скоро|если бы|если б|коль скоро|тогда как|как только|подобно тому как|будто бы)'
    self.morph = pymorphy2.MorphAnalyzer()
  
  def into_sents(self,text):
    flag = False
    if text[-1] != '.' and text[-1] != '!' and text[-1] != '?':
      text += '.'
      flag = True
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(' '+self.prefixes,"\\1<prd>",text)
    text = re.sub(self.websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + self.alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(self.acronyms+" "+self.starters,"\\1<stop> \\2",text)
    text = re.sub(self.alphabets + "[.]" + self.alphabets + "[.]" + self.alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(self.alphabets + "[.]" + self.alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+self.suffixes+"[.] "+self.starters," \\1<stop> \\2",text)
    text = re.sub(" "+self.suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + self.alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    if (flag == True):
      sentences[-1] = sentences[-1][:-1]
    sentences = [s.strip() for s in sentences if s not in ["!","?",'.']]
    return sentences
  
  def introductory_phrase(self, sent):
    result = []
    for phrase in introductory_phrases:
      if phrase in sent.lower():
        result.append(phrase)
        sent = re.sub('|, '+phrase+',|'+phrase+' |' + phrase+','+' |' + phrase, '', sent)
    tokens = word_tokenize(sent)
    comma = False
    i = 0
    tag = self.morph.parse(tokens[i])[0].tag
    while (('ADVB' in tag or 'CONJ' in tag or 'PRCL' in tag or 'COMP' in tag or 'NOUN' in tag or 'ADJS' in tag or 'ADJF' in tag or 'ADJS' in tag or 'NPRO' in tag) or tokens[i] == ','):
        if (tokens[i] == ','):
          comma = True
          break
        i += 1
        if i == len(tokens):
          break
        tag = self.morph.parse(tokens[i])[0].tag

    if comma:    
      result.append(' '.join(tokens[:i]))
    return result
  
  # check whether or not text contains predicate
  def _pred_in(self,text,subj_required=False):
    '''
    params
    ---
    text : str
    return
    ---
    bool
    '''
    tokenized = text.strip(' ').split(' ')
    noun = False
    pron = False
    adj = False
    prt = False
    verb = False
    for word in tokenized:
      word = word.strip('.')
      word = word.strip('!')
      word = word.strip('?')
      word = word.strip(',')
      if ('VERB' in self.morph.parse(word)[0].tag or 'INFN' in self.morph.parse(word)[0].tag or 'PRED' in self.morph.parse(word)[0].tag
            or 'нет' == word or 'здесь' == word or 'тут' == word):
          return True
      if ('это' == word):
        pron = True
      elif ('ADJF' in self.morph.parse(word)[0].tag or 'ADJS' in self.morph.parse(word)[0].tag):
        adj = True
      elif (len(self.morph.parse(word)) > 1):
        if ('ADJF' in self.morph.parse(word)[1].tag or 'ADJS' in self.morph.parse(word)[1].tag):
          adj = True
        elif 'NOUN' in self.morph.parse(word)[0].tag:
          noun = True
      elif 'NOUN' in self.morph.parse(word)[0].tag and 'nomn' in self.morph.parse(word)[0].tag:
        noun = True
      elif 'NPRO' in self.morph.parse(word)[0].tag:
        pron = True
      elif 'PRTF' in self.morph.parse(word)[0].tag or 'PRTS' in self.morph.parse(word)[0].tag:
        prt = True
      if len(self.morph.parse(word)) > 1:
        if ('VERB' in self.morph.parse(word)[1].tag):
          return True

    if ((noun == True or pron == True) and (adj == True or prt == True or verb == True)):
      return True
    if (noun == True and pron == True):
      return True

    return False
  
  # split by delim and check which pieces are true clauses 
  def separate_by(self,delim,text,subj_required=False):
    '''
    params
    ---
    text : str
    return
    ---
    result : list of str
    '''
    result = []
    cands = [cand for cand in re.split(delim,text) if cand != ' ']
    appended = [False]*len(cands)
    if (len(cands) > 1):
      for i in range(1,len(cands)):
        if self._pred_in(cands[i]) == False:
          if cands[i-1] in result:
            result.remove(cands[i-1])
          result.append(cands[i-1] + delim + cands[i])
          cands[i] = cands[i-1] + delim + cands[i]
          appended[i] = True
          appended[i-1] = True
        else:
          result.append(cands[i])
          appended[i] = True
      if (appended[0] == False):
        if self._pred_in(cands[0]) ==True:
          result.insert(0,cands[0])
        else:
          result[0] = cands[0] + delim + result[0]
      return result
    result = cands
    return result

  def into_clauses(self,text):
    '''
    params
    ---
    text : str
    
    return
    ---
    clauses : list of str 
    '''
    result = []

    for phrase in introductory_phrases:
        if phrase in text:
          text = re.sub(', '+phrase+',', '', text)
          result.append(phrase)
    text = ' ' + text + ' '
    text = re.sub(', ' + self.conjs + ' | ' + self.conjs + ' ', '<stop>',text)
    clauses = text.split('<stop>')
    
    temp = []
    if ';' in text:
      temp = []
      for clause in clauses:
        for x in self.separate_by(';',clause):
          temp.append(x.strip(' '))
      clauses = [x for x in temp if x != '']
    if ' - ' in text:
      temp = []
      for clause in clauses:
        for x in self.separate_by('-',clause):
          temp.append(x.strip(' '))
      clauses = [x for x in temp if x != '']
    if ',' in text:
      for clause in clauses:
        for x in self.separate_by(',',clause):
          temp.append(x.strip(' '))
      clauses = [x  for x in temp if x != '']
    
    temp = []
    for clause in clauses:
      phrases = self.introductory_phrase(clause)
      for phrase in phrases:
        clause = re.sub(phrase+' |' + phrase+','+' |' + phrase + '|, '+phrase+',|', '', clause)
        temp.append(phrase)
      temp.append(clause)

    for clause in temp:
      if clause.strip() != '':
        result.append(clause.strip())

    return result

