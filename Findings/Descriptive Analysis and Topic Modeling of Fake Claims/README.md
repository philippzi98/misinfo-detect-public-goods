# Descriptive Analysis and Topic Modeling of Fake Claims

## Some Facts on our Claims Data
In this section, we offer a quantitative glimpse into our expansive dataset of fact-checked claims. 
By harnessing the rich data from various fact-checking organizations, we establish a foundational understanding of the landscape of misinformation and its trajectories over time. 
As illustrated below, the dataset of fact-checked claims is skewed towards false claims (59,712), followed by misleading (16,891) and true claims (6,826). 
This distribution is not surprising given that we expect fact-checking organizations whose data we are utilizing to be focused on identifying and highlighting false information. 
Oftentimes, they approach their work with the aim of debunking misleading or false claims rather than “confirming” true claims that seem unlikely to be true. 
For our later purposes of identifying fake claims amongst social media posts, this imbalance is not problematic since we compute the semantic similarity and mention of fake-claim-prone domains rather than prompting a trained model to identify if a claim is true or false (like past work by DeVerna et al., 2023).
We also observe an increase in the number of recorded claim-verdict pairs over time in recent years. 
Our dataset peaks with 3,571 ground-truth false claims recorded alone in Q3 of 2023. 
While we observe an overall increase for all types of claims (that is, true, false, and misleading), the effect is particularly pertinent to observed false claims. 
Another key dimension of our fake claims dataset and thus the main basis of our future studies, are the sources of the fact checks. 
As discussed above, we ensure the credibility of our data by checking the certification of fact-checking organizations with the International Fact-Checking Network. 
Thereby, we seek to reduce potential biases and increase the reliability of our dataset. 
The importance of this validation step became particularly apparent to us through the incident of a Mexican fact-checking organization which emerged on the fact-checking landscape a few years ago and was accused of being biased in its assessments partly due to its ownership by no other than the Mexican president López Obrador (Poynter, 2019). 

&nbsp;

<p align="center">
<img src="https://drive.google.com/uc?export=view&id=1vEgYWywR69m3ZBiWiZ1FaVAHiitNygxg" alt="Distribution of Verdict Labels (over Time)" title="Distribution of Verdict Labels (over Time)"/>
<p/>

&nbsp;

<p align="center">
<img src="https://drive.google.com/uc?export=view&id=1VX4n2t3efNtytQmIj5cgWp9mx3etbUBR" alt="Distribution of Verdict Labels across Fact-Checking Organizations (over Time)" title="Distribution of Verdict Labels across Fact-Checking Organizations (over Time)"/>
<p/>

&nbsp;

In the visual above, we zero in on a select group of fact-checking agencies with significant presence in West Africa, particularly Nigeria. 
These include prominent organizations such as factcheck.afp.com, africacheck.org, dubawa.org, thecable.ng, and cddfactcheck.org. 
These entities not only provide fact-checks but also contribute to the growing awareness of misinformation in the region. 
Similar to the entire dataset with international scope, the Nigerian fact-checking agencies likewise focus on false and misleading claims. 
Furthermore, we can observe that more agencies have become active over the years, indicating the increasing importance of fact-checking.
Next, as a stepping stone to our topic modeling work, we took a first glance at the frequency of word tokens in our claims dataset. 
To draw a comparison between the overarching dataset on fact-checks and a geographically more narrow perspective on Nigeria, we map the word clouds of all claims and only those by the Nigerian agencies whose fact-checking repositories we scraped. 
We observe the US-centric focus of the international dataset through tokens like Donald Trump and Joe Biden. 
As for the Nigerian perspective, social media appears to be a relevant theme along with specific platforms such as WhatsApp and Twitter. 
From our observations working with the data, we attribute this to many claims emerging or being propagated on different social media platforms through which they become apparent to the fact-checkers and thus fact-checked.

&nbsp;

<p align="center">
<img src="https://drive.google.com/uc?export=view&id=1QPFufcmK9SHN3iC-sUK44l9ioKiDDpob" alt="Word Clouds of (1) All Claims and (2) Claims by Scraped Nigerian Fact-Checkers" title="Word Clouds of (1) All Claims and (2) Claims by Scraped Nigerian Fact-Checkers"/>
<p/>

&nbsp;

## How to Identify Themes Amongst Fake Claims
In our exploration of the claims dataset, we move beyond the preliminary insights provided by word clouds to adopt a more systematic and rigorous approach to uncovering thematic structures within the data. 
The word clouds offer an initial visualization of the frequency of terms across all claims and those specific to Nigerian fact-checkers. 
To delve deeper, we implement a process that can be described as a semi-supervised approach to topic modeling. 

Our data consists of textual claims lacking "ground-truth" topic labels that would allow for straightforward categorization. 
This necessitates an approach that can infer structure in an unsupervised manner but also incorporates human judgment in the final designation of topics. 
To this end, we employ Latent Dirichlet Allocation (LDA), a widely-used topic modeling technique that identifies themes from a collection of texts by grouping together words that frequently co-occur.

LDA differs from other NLP methods like BERT in several key aspects:
- Probabilistic Model: Unlike BERT, which generates dense vector representations, LDA is a generative probabilistic model that assumes each document is a mixture of a small number of topics and that each word's creation is attributable to one of the document's topics.
- Interpretability: LDA focuses on maximizing the co-occurrence of words within topics, which often results in more interpretable clusters of words, forming the basis for topic identification.
- Scalability and Simplicity: LDA is generally more straightforward to implement and interpret compared to deep learning approaches, making it suitable for datasets where deep contextual embeddings might not be essential - as is the case in our task.

After preprocessing our text data with the common steps of lemmatization, lowercasing, removing stopwords, and removing special characters, we convert the text into a matrix of token counts with the help of a CountVectorizer since LDA, being a probabilistic graphical model, requires numerical input. 
LDA models require the choice of the number of clusters as an input, wherefore we experiment with varying model settings (from 5 to 12 topic clusters). 
We identified 10 topic clusters to be a good balance with fewer topics missing the nuance of significant, yet specialized topics (Indian Politics and US Politics), while more topics resulted in a fragmented topic space. 
The model outputs a set of topics, each represented as a collection of words, which we then interpret to understand the predominant themes in the claims. 
In the step of inferring the topic labels, the supervised aspect of our methodology comes into play. 
We pay particular attention to exclude words like geographic locations and personal names that, while potentially frequent in the corpus, do not contribute to the thematic significance of topics. 
This step ensures that our topics reflect the substantive content of the claims, rather than being skewed by frequently occurring but thematically irrelevant terms. 
Our team investigates the most relevant words of each cluster - that is, the words statistically determined to be most informative or expressive of the specific topic. 
Based on these terms, we manually assign representative labels to the clusters. 
Therefore, the identified topics are a direct outcome of our claims data rather than a representative “ground-truth” topic landscape online. 
For instance, we observe specialized clusters that represent Indian Politics (key terms include Modi and BJP) and US Politics (key terms include Trump, Biden, and Obama). 
The set of identified topics aligns with our observations that the Google API - our main data source - contains many fact checks on Indian and US politics. 
Aside from these two topics, our model’s clusters cover a comprehensive topic space, wherefore we believe the below-illustrated findings are insightful in understanding the misinformation landscape.

&nbsp;

## Findings from our Topic Modeling
With the topics delineated and labeled, we embark on a dual-pronged analysis: a global examination of all claims, alongside a more localized investigation focusing on claims checked by Nigerian fact-checkers. 
This allows us to understand both the overarching themes at play in our broader dataset and the specific narratives that emerge within the subset of Nigerian fact-checker data. 

&nbsp;

<p align="center">
<img src="https://drive.google.com/uc?export=view&id=1YyD7DuuzhRRLr6lRu0nbrhLrkzybABg3" alt="Topic Distribution across All Claims" title="Topic Distribution across All Claims"/>
<p/>

&nbsp;

One immediate observation for the “global” view on the claims topics is that we have a relatively even distribution of fake claims across topics, which might be partly a result of topic models seeking to form cohesive, similarly sized clusters. 
However, introducing the temporal disaggregation, we can make some interesting observations. 
As such, arguably in the lead-up to the last US presidential elections, the number of related fact-checks more than doubled. 
Likewise, we can clearly identify the occurrence of the COVID-19 Pandemic and related fact-checks, as well as an increase in Global Politics and Conflicts in 2022. 
The latter can be traced back to Russia’s war on Ukraine with many claims in this cluster referring to claims on military movements, battles, and other countries’ actions or statements related to the conflict.
Zooming in on the fact-checks by Nigerian fact-checking organizations, we can observe a national perspective on claims that differs in its thematic distribution from the international picture. 
Particularly, Social Media related claims (such as fake claims with their origins on platforms like YouTube and Facebook) are very prevalent and increasing in number. 
Likewise, Health and Education is a very prominent theme, which we would partly attribute to the many statements of politicians on the state of the country, which we found in our dataset. 
Ultimately, we can thereby also identify how the public dialogue changes and how countries’ “development markers” move to the center of attention in times of elections, when politicians seek to position themselves - for instance, in relation to the current government’s “performance.”

&nbsp;

<p align="center">
<img src="https://drive.google.com/uc?export=view&id=1nYdVLFeY2oi6tkdZ6U5OjyQ0v8IpmziD" alt="Topic Distribution across Nigerian Claims" title="Topic Distribution across Nigerian Claims"/>
<p/>

&nbsp;
  
An overarching observation we can make is on the relative prevalence of false, misleading and true claims that are investigated by the fact-checking organizations. 
While the deviances across topics are minor, it is interesting that we can observe relatively more true (and also misleading) claims on the “broader” Health and Education topic cluster, while the specific COVID-19 cluster exhibits similar patterns as the other claim clusters. 
We hypothesize that this is potentially due to many investigated claims being statements on statistics by politicians and thought leaders rather than extremely dubious claims. 
Generally speaking, while our results intuitively make sense, we will continue evaluating our approach iteratively and also observe changes over time with ever more claims data becoming available to us in the next stage of the project. 
The current labeled data set of claims as well as a file with aggregate statistics is available here.

&nbsp;

<p align="center">
<img src="https://drive.google.com/uc?export=view&id=1l-wKgRRFIEcT53e4pLDnHVLCw_NKUi-O" alt="Verdict distribution across Topics" title="Verdict distribution across Topics"/>
<p/>

&nbsp;

