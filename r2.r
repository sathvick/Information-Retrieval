library(plyr)
library(dplyr)
library(tm)
library(stringr)
library(tidytext)
library(ggplot2)

# load the input data, add a "category" column and bind them all into one
path = "./Dataset/"
dir = DirSource(paste(path,sep=""), encoding = "UTF-8")
corpus = Corpus(dir)
length(corpus)

#corpus <- tolower(corpus)
View(corpus)

myStopwords = c(stopwords(),"crime","crimes","security","securities","i.e.", "would", "get", "like", "using", "know", "question", "use", 
                "get", "possible" , "aah",
                "much", "find", "anyone",'able', 'according', 'accordingly', 'across',
                'actually', 'afterwards', "ain't", 'allow', 'allows', 'almost',
                "tell", "know", "another", "various", "also", "etc", "around", "vs",
                "used", "could", "without", "way", "new",
                'alone', 'along', 'already', 'although', 'always', 'among', 
                'amongst', 'anybody', 'anyhow', 'anything', 
                'anyway', 'anyways', 'anywhere', 'apart', 'appear', 'appreciate',
                'appropriate', 'aside', 'ask', 'asking', 
                'associated', 'available', 'away', 'awfully', 
                'b', 'be', 'became', 'become', 'becomes',
                'becoming', 'been', 'before', 'beforehand', 'behind', 'being',
                'believe', 'below', 'beside', 'besides', 'best', 'better',
                'between', 'beyond', 'both', 'brief', 'but', 'by', 'c', "c'mon",
                "c's", 'came', 'can', "can't", 'cannot', 'cant', 'cause',
                'causes', 'certain', 'certainly', 'changes', 'clearly', 'co',
                'com', 'come', 'comes', 'concerning', 'consequently', 'consider',
                'considering', 'contain', 'containing', 'contains',
                'corresponding', 'could', "couldn't", 'course', 'currently', 'd',
                'definitely', 'described', 'despite', 'did', "didn't", 'didnt',
                'different', 'do', 'does', "doesn't", 'doesnt','doing', "don't",
                'dont', 'done',
                'down', 'downwards', 'during', 'e', 'each', 'edu', 'eg', 'eight',
                'either', 'else', 'elsewhere', 'enough', 'entirely', 'especially',
                'et', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone',
                'everything', 'everywhere', 'ex', 'exactly', 'example', 'except',
                'f', 'far', 'few', 'fifth', 'first', 'five', 'followed',
                'following', 'follows', 'for', 'former', 'formerly', 'forth',
                'four', 'from', 'further', 'furthermore', 'g', 'get', 'gets',
                'getting', 'given', 'gives', 'go', 'goes', 'going', 'gone', 'got',
                'gotten', 'greetings', 'h', 'had', "hadn't",'hadnt', 'happens', 'hardly',
                'has', "hasn't", 'hasnt','have', "haven't",'havent', 'having',
                'he', "he's",'hes', 'hello', 'help', 'hence', 'her', 'here', 
                "here's",'heres', 'hereafter',
                'hereby', 'herein', 'hereupon', 'hers', 'herself', 'hi', 'him',
                'himself', 'his', 'hither', 'hopefully', 'how', 'howbeit',
                'however', 'i', "i'd", 'id','ill',"i'll", "i'm", 'im', "i've", 
                'ive','isnt', "isn't", 'ie', 'if',
                'ignored', 'immediate', 'in', 'inasmuch', 'inc', 'indeed',
                'indicate', 'indicated', 'indicates', 'inner', 'insofar',
                'instead', 'into', 'inward', 'is', "isn't",'isnt', 'it', "it'd",
                'itd','itll', "it'll",
                "it's", 'its', 'itself', 'j', 'just', 'k', 'keep', 'keeps',
                'kept', 'know', 'knows', 'known', 'l', 'last', 'lately', 'later',
                'latter', 'latterly', 'least', 'less', 'lest', 'let', "let's",
                'like', 'liked', 'likely', 'little', 'look', 'looking', 'looks',
                'ltd', 'm', 'mainly', 'many', 'may', 'maybe', 'me', 'mean',
                'meanwhile', 'merely', 'might', 'more', 'moreover', 'most',
                'mostly', 'much', 'must', 'my', 'myself', 'n', 'name', 'namely',
                'nd', 'near', 'nearly', 'necessary', 'need', 'needs', 'neither',
                'never', 'nevertheless', 'new', 'next', 'nine', 'no', 'nobody',
                'non', 'none', 'noone', 'nor', 'normally', 'not', 'nothing',
                'novel', 'now', 'nowhere', 'o', 'obviously', 'of', 'off', 'often',
                'oh', 'ok', 'okay', 'old', 'on', 'once', 'one', 'ones', 'only',
                'onto', 'or', 'other', 'others', 'otherwise', 'ought', 'our',
                'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'own',
                'p', 'particular', 'particularly', 'per', 'perhaps', 'placed',
                'please', 'plus', 'possible', 'presumably', 'probably', 'put',
                'provides', 'q', 'que', 'quite', 'qv', 'r', 'rather', 'rd', 're',
                'really', 'reasonably', 'regarding', 'regardless', 'regards',
                'relatively', 'respectively', 'right', 's', 'said', 'same', 'saw',
                'say', 'saying', 'says', 'second', 'secondly', 'see', 'seeing',
                'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves',
                'sensible', 'sent', 'serious', 'seriously', 'seven', 'several',
                'shall', 'she', 'should', "shouldn't", 'since', 'six', 'so',
                'some', 'somebody', 'somehow', 'someone', 'something', 'sometime',
                'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry',
                'specified', 'specify', 'specifying', 'still', 'sub', 'such',
                'sup', 'sure', 't', "t's", 'take', 'taken', 'tell', 'tends', 'th',
                'than', 'thank', 'thanks', 'thanx', 'that', "that's", 'thats',
                'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence',
                'there', "there's", 'theres', 'thereafter', 'thereby', 'therefore',
                'therein', 'theres', 'thereupon', 'these', 'they', "they'd", 'theyd', 
                'theyll', 'theyre',
                "they'll", "they're", "they've", 'think', 'third', 'this', 'theyve',
                'thorough', 'thoroughly', 'those', 'though', 'three', 'through',
                'throughout', 'thru', 'thus', 'to', 'together', 'too', 'took',
                'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying',
                'twice', 'two', 'u', 'un', 'under', 'unfortunately', 'unless',
                'unlikely', 'until', 'unto', 'up', 'upon', 'us', 'use', 'used',
                'useful', 'uses', 'using', 'usually', 'uucp', 'v', 'value',
                'various', 'very', 'via', 'viz', 'vs', 'w', 'want', 'wants',
                'was', "wasn't", 'wasnt', 'way', 'we', "we'd", "we'll", "we're", "we've",
                'wed', 'well', 'were', 'weve', 'werent', 'whats', 'wheres', 
                'whos','wont','wouldnt',
                'welcome', 'well', 'went', 'were', "weren't", 'what', "what's",
                'whatever', 'when', 'whence', 'whenever', 'where', "where's",
                'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon',
                'wherever', 'whether', 'which', 'while', 'whither', 'who',
                "who's", 'whoever', 'whole', 'whom', 'whose', 'why', 'will',
                'willing', 'wish', 'with', 'within', 'without', "won't", 'wonder',
                'would', 'would', "wouldn't", 'x', 'y', 'yes', 'yet', 'you',
                'youd', 'youll', 'youre', 'youve', 
                "you'd", "you'll", "you're", "you've", 'your', 'yours',
                'yourself', 'yourselves', 'z', 'zero')

tdm = TermDocumentMatrix(corpus,control = list(removePunctuation = T,
                                        removeNumbers = T,
                                        stemming = T))

#q3
( tf <- as.matrix(tdm) ) #frequency of each term in entire corpus
idf <- tf
idf[idf>0]<-1
idf <- log10(ncol(tf)/rowSums(idf))
idf
------------------
library(lapply)
filenames <- list.files(pattern="*.txt")
text.tagged <- lapply(filenames, function(x) treetag(x, treetagger="manual", lang="en",
                                                     TT.options=list(path=filepath, preset="en")))

text.tagged[1]


