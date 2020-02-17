library(tm)
library(ggplot2)
#q1#
path = "./Dataset/"
dir = DirSource(paste(path,sep=""), encoding = "UTF-8")
corpus = Corpus(dir)
length(corpus)
#corpus[[1]]$content
#strwrap(corpus)
myStopwords = c(stopwords(),"crime","crimes","security","securities")
tdm = TermDocumentMatrix(corpus,
                         control = list(weighting = weightTfIdf,
                                        stopwords = myStopwords, 
                                        removePunctuation = T,
                                        removeNumbers = T,
                                        stemming = T))



#q3
( tf <- as.matrix(tdm) ) #frequency of each term in entire corpus
idf <- tf
idf[idf>0]<-1
idf <- log10(ncol(tf)/rowSums(idf))
idf

library(SnowballC)
#inspect(tdm[2005:2015,100:103])
freq=rowSums(as.matrix(tf))
View(freq)
head(freq,10)
tail(freq,10)
barplot(sort(freq, decreasing = T),col="blue",main="Word TF-IDF frequencies", xlab="TF-IDF-based rank", ylab = "TF-IDF")
tail(sort(freq),n=10)

high.freq=tail(sort(freq),n=10)
hfp.df=as.data.frame(sort(high.freq))
hfp.df$names <- rownames(hfp.df) 

ggplot(hfp.df, aes(reorder(names,high.freq), high.freq)) +
  geom_bar(stat="identity") + coord_flip() + 
  xlab("Terms") + ylab("Frequency") +
  ggtitle("Term frequencies")

# q2
tdm <- TermDocumentMatrix(corpus,list(dictionary=c("kill","miss","kidnap","crime","shoot","death", "victim","police","murder", "suspect","blood")))
#( tf <- as.matrix(tdm) )


#q4
tdm <- TermDocumentMatrix(corpus,list(dictionary=c("kill","miss","kidnap","crime","shoot","death", "victim","police","murder", "suspect","blood")))
( tf <- as.matrix(tdm) )
tfLog  <- ifelse(tf>0,1+log10(tf),0)
tfLog

idf <- tf
idf[idf>0]<-1
idf <- log10(ncol(tf)/rowSums(idf))
idf

tf.idf <- tfLog*idf
tf.idf

#q5

freq=rowSums(as.matrix(tf.idf))
View(freq)
head(freq,11)
tail(freq,11)
barplot(sort(decreasing = T, freq),col="blue",main="Word TF-IDF frequencies", xlab="TF-IDF-based rank", ylab = "TF-IDF")
tail(sort(freq),n=11)
plot(sort(decreasing = T, freq),col="blue",main="Word TF-IDF frequencies", xlab="TF-IDF-based rank", ylab = "TF-IDF")
tail(sort(freq),n=11)

freq=rowSums(as.matrix(idf))
high.freq=tail(sort(freq),n=11)
hfp.df=as.data.frame(sort(high.freq))
hfp.df$names <- rownames(hfp.df) 

ggplot(hfp.df, aes(reorder(names,high.freq), high.freq)) +
  geom_bar(stat="identity") + coord_flip() + 
  xlab("Query Terms") + ylab("IDF") +
  ggtitle("IDF Bar Chart")

# Simple Pie Chart
x=freq
pie(x, labels = names(x), edges = 200, radius = 0.8,
    )

#q7
library(proxy)
cosd<- function(x, y) {
 similarity <- sum(x * y) / ( sqrt( sum(y ^ 2) ) * sqrt( sum(x ^ 2) ) )
  
  # given the cosine value, use acos to convert back to degrees
  # acos returns the radian, multiply it by 180 and divide by pi to obtain degrees
  return( acos(similarity) * 180 / pi )
}


#pr_DB$set_entry(FUN = cosde, names = c("cosde"))
#d1 <- dist(tf.idf, method = "cosde")
#d1
#summary(pr_DB)
#View(d1)

#cosd <- function(x,y) {
 # z <- rbind(x,y)
  #z <- as.matrix(z[,colSums(is.na(z)) == 0])
  #x <- z[1,]
  #y <- z[2,]
  #x %*% y / (sqrt(x%*%x) * sqrt(y%*%y))
#}
query <- idf
query[] <- 0
query["kill"] <- idf["kill"]
query["miss"] <- idf["miss"]
query["kidnap"] <- idf["kidnap"]
query["crime"] <- idf["crime"]
query["shoot"] <- idf["shoot"]
query["death"] <- idf["death"]
query["victim"] <- idf["victim"]
query["police"] <- idf["police"]
query["murder"] <- idf["murder"]
query["suspect"] <- idf["suspect"]
query["blood"] <- idf["blood"]
query

qtf.idf <- cbind(tdm,query)
qtf.idf

pr_DB$set_entry(FUN = cosd, names = c("cosd"))
d1 <- dist(qtf.idf, method = "cosd", upper=TRUE)
View(d1)


#heat Map
data <- as.matrix(tf.idf)
library(RColorBrewer)
my_group <- as.numeric(as.factor(substr(rownames(data), 1 , 1)))
colSide <- brewer.pal(9, "Set1")[my_group]
colMain <- colorRampPalette(brewer.pal(8, "Blues"))(25)
heatmap(data, Colv = NA, Rowv = NA, scale="column" , RowSideColors=colSide, col=colMain )

#wordcloud
library(wordcloud)
inspect(corpus)
toSpace <- content_transformer(function (x , pattern ) gsub(pattern, " ", x))
corpus <- tm_map(corpus, toSpace, "/")
corpus <- tm_map(corpus, toSpace, "@")
corpus <- tm_map(corpus, toSpace, "\\|")
# Convert the text to lower case
corpus <- tm_map(corpus, content_transformer(tolower))
# Remove numbers
corpus <- tm_map(corpus, removeNumbers)
# Remove english common stopwords
corpus <- tm_map(corpus, removeWords, stopwords("english"))
# Remove your own stop word
# specify your stopwords as a character vector
corpus <- tm_map(corpus, removeWords, c("blabla1", "blabla2"))
# Remove punctuations
corpus <- tm_map(corpus, removePunctuation)
# Eliminate extra white spaces
corpus <- tm_map(corpus, stripWhitespace)
# Text stemming
# corpus <- tm_map(corpus, stemDocument)

dtm <- TermDocumentMatrix(corpus)
m <- as.matrix(dtm)
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)
head(d, 10)
set.seed(1234)
wordcloud(words = d$word, freq = d$freq, min.freq = 1,
          max.words=1000, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))


