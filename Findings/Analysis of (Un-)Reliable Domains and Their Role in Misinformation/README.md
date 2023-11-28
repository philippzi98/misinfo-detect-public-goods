# Analysis of (Un-)Reliable Domains and Their Role in Misinformation

## The Prevalence of News Domains amongst Tweets
Our approach involves examining the prevalence of news domains classified as non-credible within the links shared by Nigerian Twitter users. 
Our analysis is grounded in a dataset of 11,000 news domains, each assigned a quality rating on a scale from 0 to 1, as per Lin et al. ([2023](https://academic.oup.com/pnasnexus/article/2/9/pgad286/7258994?login=true)). 
These ratings serve as a proxy for the credibility of the content, with lower scores indicating a higher likelihood of misinformation. 
We have discovered that a subset of 9.1K out of these 11K domains appears in our Twitter dataset, a figure which, while representing a mere 0.1% of all domains shared, accounts for a significant 10% of all links shared – totaling approximately 219 million links. 
Closer scrutiny reveals that approximately 2,000 of these domains have ratings below 0.4, which we categorize as predominantly disseminating misinformation. 
These suspect domains contribute to 1.6% of all links shared, equating to 34 million links – a non-trivial volume that carries the potential for substantial impact on public discourse.
The preliminary sweep of flagged domains from the Nigerian fact-checking organization CDD underscores the challenge in establishing the precision of these ratings. 
Approximately 10 domains identified by the CDD have been flagged for further analysis, but without a refined sense of their accuracy in signaling misinformation. 
By integrating these quality ratings with the extensive number of links in our dataset, we have begun to map the contours of misinformation spread through news domains on Nigerian Twitter. 
This analysis provides a critical foundation for developing automated tools that can detect and flag potential sources of misinformation. 

&nbsp;

## The Spread of Fake News Links
In the complex web of social media, misinformation can be propagated in numerous ways. 
On Twitter, this often occurs through tweets containing either direct false claims or links to external sources with misleading content. 
Our investigation focused on 26 domains infamous for their dissemination of fake news (as identified through the earlier outlined approach). 
Tracing back to these sources, we uncovered that 13,000 Twitter users had shared links from these dubious websites. 
This substantial figure points to the widespread reach of misinformation. 
Beyond identifying these users, our analysis delved deeper into the followership network of these 13,000 individuals. 
By examining who they follow and their interconnectedness, we sought to unravel the social dynamics underpinning this web of misinformation.

&nbsp;

<p align="center">
<img src="https://drive.google.com/uc?export=view&id=1MnSAyLqh3CCo5zOJURca9MUjmPiqELN9" alt="(1) Fake News and (2) Reliable Websites" title="(1) Fake News and (2) Reliable Websites"/>
<p/>

&nbsp;

## Unraveling Homophily in Misinformation Networks
Central to our analysis was the concept of homophily, the natural human tendency to connect with others who share similar traits or beliefs. 
To quantify this phenomenon within our context, we calculated a revealing ratio: the proportion of friends sharing fake news among users who posted such content compared to the overall Twitter population. 

Our findings were quite revealing:
- Among users who disseminated fake news, 6.6% of their friends also engaged in similar activities.
- For the average Twitter user, this statistic stood at just 2.3%.
  
This stark disparity illustrates a significant pattern: users involved in spreading fake news were nearly three times more likely to have connections with others who also shared such content. 
This pattern paints a vivid picture of misinformation echo chambers, where false narratives find fertile ground to grow and proliferate.

&nbsp;

## Assessing the Scale of Fake News Consumption
Broadening our scope, we aimed to understand the scale of fake news consumption relative to overall news engagement. 
After mapping the Nigerian news domain, we differentiated between approximately 260 credible news sources and the 26 identified fake news sites. 
Our methodology involved analyzing the retweet patterns of all Twitter users in our dataset, focusing on links to reliable and fake news domains. 

Our analysis brought to light the following:
- Retweets linking to reliable news sources amounted to a total of 19,114,203.
- Contrastingly, retweets of fake news content reached 351,255.

This data indicates that fake news constituted about 1.8% of the total news consumption among Twitter users in Nigeria. 
While this percentage might appear modest at first glance, it signifies a substantial volume of misinformation permeating the user base. 
This aspect of our findings highlights fake news's subtle yet significant impact on shaping public narratives and influencing discourse.
