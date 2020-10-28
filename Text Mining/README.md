# Text Processing



# Training and Creating the LDA Model


Now that data is all in a standard form, we can start to train our model. First, an LDA (Latent Dirchlet Association) model is a generative statistical model 
that allows sets of observations to be explained by unobserved groups and in this way it can explained why some of the observations are similar between themselves. 
In our particular case, the model will group the news articles according to their words. This groups is what we call topics, and each topic has a word distribution
relative to the frequency that each word appears in each topic. The result also depends on two parameters: $\beta$ and $\alpha$.  
With these and knowing which the words inside every article we can also obtain the probability that an article belongs to a certain topic. 
This is called the document-topic distribution and is a dimensional reduction of this distribution that we observed in plots available to you at this url: [https://topic-model-app.herokuapp.com/]. 
