# Text Processing

Once the data is all store in a structured and organized way. we can loop over each json file to open and process the text. In this step by processing I actually mean the following:

- putting all words in lower case
- Removing the accents and punctuation signs since we use a bag of words method. 
- Removing the excess of blank spaces
- Create a common reference for Covid19, since it was and still is a big topic during this period of time.
- Lemmatize the words: Lematizing a word is a linguistic process in which we replace each word with its lemma. By lemma I refer to the standarized form in which that particular word is commonly known. I was able to achieve this by using the Stanford NLP module in python. 


If you are interested in checking out the code for this part of the project, look in the 



# Training and Creating the LDA Model




Now that data is all in a standard form, we can start to train our model. First, an LDA (Latent Dirchlet Association) model is a generative statistical model 
that allows sets of observations to be explained by unobserved groups and in this way it can explained why some of the observations are similar between themselves. 
In our particular case, the model will group the news articles according to their words. This groups is what we call topics, and each topic has a word distribution
relative to the frequency that each word appears in each topic. The result also depends on two parameters: $\beta$ and $\alpha$. Now that we know which the words are inside every article we can also obtain the probability that an article belongs to a certain topic. This is called the document-topic distribution and is a dimensional reduction of this distribution that we observed in plots available to you at this url: [topic Modelling dash app](https://topic-model-app.herokuapp.com/). 


If you are interested in checking out the code for this part of the project, look in the 
