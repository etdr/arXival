
# title

Slides for this post are available HERE


## Intro

The [arXiv](https://arxiv.org/) is a preprint repository for over 1.6 million papers from across physics, mathematics, computer science, and a few other subjects.
Over 10,000 papers a month these days are uploaded and free to download in PDF form and, usually, the source (La)TeX files as well.

For this project, the fourth for Metis and The One About NLP, I chose to work with papers from 2019. Like, all of them. I could have written a script to download them all directly from arxiv.org, but they ask that if you really need to bulk-download part of the arXiv you use the S3 requester-pays bucket, which I did. For reference, one year of PDFs ran me about $20, which I consider an OK price to pay.

It would be even more of a deal if I could gain knowledge by actually reading the papers, but that's almost all beyond my abilities as a human, unfortunately. That being said, I chose to work with this repository-cum-dataset because I find these topics fascinating, even if I wasn't actually working with them. I was able to work near them, which gave me a sense of, I don't know, working with something meaningful. Anyway.










## Data acquisition 

After downloading the PDFs, I converted them into text using the pdftotext utility from the Poppler set of PDF command-line tools. Originally I kept the version of this output obtained by feeding the "-layout" option to pdftotext, which "preserves the layout" as best it can, but in effect all this does is insert whitespace that I would later have to take out, so I eventually dropped this form of the text.

On the majority of the PDFs, the arXiv ID and date are printed along the the left side of the first page, and pdftotext does include this in the output, although not in a consistent place. I wrote a few functions to extract these data, and, along with the text, stored it all as documents in MongoDB, with a collection for each month. However, not all of the documents had this information (my hypothesis is that these are the ones where the authors uploaded their PDFs directly instead of uploading the source, but I'm not sure), and in any case, only the *first* topic was printed in the document, when in actuality the topics function as tags, meaning a paper can have more than one.

So, I wrote a script to fetch XML metadata from the arXiv's OAI interface and extract the dates and topic lists I needed. I was operating under what I thought was a four-requests-per-second limit that they ask you observe, but then after I ran the script for awhile (two at a time, actually) I reread that for that service they ask you to limit to one request every three seconds, which, if anyone relevant is reading this, I apologize for not adhering to these guidelines exactly...

*Anyway*, I ended up with a lot of text. At some point I started working on a VM on Google Cloud Platform, which meant I had to learn how to use Debian for the first time, which mostly meant all the apt-get commands. I'm used to systemd and most other Linux stuff from Arch already, so it wasn't that hard. I used a GCP bucket to transfer the exported MongoDB database to the cloud VM, and restoring it was simple enough. 




## Preprocessing

The main problem with my pdftotext approach isn't really pdfttext's fault, it's that I asked it to deal with complex typeset mathematics and give me pure text. I don't know if I could have done better.

I ended up with documents filled with Latin letters, math symbols, Greek letters, parens and brackets sometimes with spaces between them and their enclosures and sometimes without, general spacing inconsistencies, and probably other issues I'm not aware of. Now, one approach to this is keeping everything, which I kind of considered, since I was and still am under the impression that the math and symbols contain information useful for text analysis of a paper, and I wasn't sure what to discard. But this keeps in a *lot* of noise, plus the sheer number of combinations of random variables, digits, and symbols makes it untenable if you're tokenizing and encoding *everything*.

Another approach is to find a list of English words and filter on that. I did get a list of words (this one)

and although it wasn't specifically tuned to math and physics, it was pretty expansive ("cuboctahedron" was on there, for instance). 





I ended up with a function that took in the word in question, the document, and other parameters, and spat out True (keep the word) or False (drop it). (fastText below has a similar customizable "trim" function parameter but it isn't given the document, although it is given the number of times the word appears in the whole corpus as an input, which is nice.) The criteria I used were:
* 

If I come back to this project, I will work on a v2 filtering function, or even more general functions for preprocessing.











## Exploration 1: Topic Modeling with LDA

[Latent Dirichlet allocation](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation)
is a tool that is used for topic modeling, among other things.
Of all the things I've learned at Metis, this might be the one that I consider the most magicky,
in that I can't believe it works but it really does. You ask for a certain number of topics---I chose 12---and it comes back with the words that define those topics.

The reason that I can't believe it works is essentially that it goes through your documents, in my case academic papers, and, well, I honestly don't understand the math, and that's why it bothers me.



Here are my interpretations of the twelve topics identified by LDA:

1. vague physics
2. dynamical systems, orbits, stability, phase spacey stuff
3. almost entirely digit bigrams 😢
4. “proof of”, “there exists”, “for every”, “follows from”, “implies that”
5. vague physics, polluted with reference abbreviations and such
6. high-energy physics
7. like 4, but more physicsy maybe
8. data science and machine learning
9. mashup of conferences and deep learning
10. astrophysics, but very polluted
11. journal references and other jargon
12. computer science, but very polluted



Some of these I'm proud of, for instance topic 4, the mathy proof category. Almost all the bigrams in the top ten or twenty or hundred even were right on this topic. Others, like twelve, seemed somewhat CSy but were filled with many other bigrams that weren't really on a particular topic, which might be just the process and might be that I didn't do enough or the right kind of preprocessing, and I'm aware of that. Topic three, which was just numbers, shows this to be the case pretty strongly.








## Exploration 2: Word Embeddings with fastText


[fastText](https://fasttext.cc/) comes from Facebook and is a library for learning text representation via word embeddings. You can download pre-trained word vectors on their website or train your own using your own corpus. While it doesn't use a GPU, the CPU implementation is multicore and pretty fast, I was able to do 20 passes over the 75k documents overnight (the GPU was simultaneously being used by Exploration 3, see below).

You can download the official version of fastText on their site, or, as I did, use the version implemented in [gensim](https://radimrehurek.com/gensim/), a popular Python package that serves as one person's collected implementations of lots of algorithms. It also implements word2vec (though not GPU-accelerated) and the LDA from the previous Exploration.











## Exploration 3: Word Embeddings with word2vec

Now, here's where things go off the rails a bit.

Basically, I "implemented" word2vec in TensorFlow using only what little I know about the algorithm and not actually reading either of the original papers.

I created an encoding using the tokenizer built into keras.


Keras has an *Embedding* layer, which will take in a sequence of numbers and at those locations in the input it'll put a 1. Not explaining this well. Hm. It basically saves you the trouble of converting a bag of words encoded 1, 2, ..., howevermany into a one-hot vector with the words in the bag 1. So, for me, I just wanted to predict a target word using a single word near it in the text, so my input_length was 1, even though it works for a sequence.

The Embedding layer actually goes from the input to the 240-neuron hidden layer, so the weight matrix that I'm interested in, the actual embeddings, is 100000x240. Then you have to add a Flatten layer so keras doesn't complain about shape (my depiction of how Embedding works in the last paragraph wasn't exactly correct, I remember now), and then a Dense layer taking the 240 neurons back out to 100,000 with softmax as the activation function. All that's left is to train it.

For that, I wrote a function to randomly select a document, then randomly select a word in that document and call that the target word. I then selected one word within two of the input word before or after, and called that the input. So that's what I trained the model on. I used stochastic gradient descent as an optimizer and categorical crossentropy as the loss function, because, like I said, I didn't read the papers so I don't know better.


