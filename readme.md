# Motivation:
- Analyse multiple years worth of stack overflow user survey data
- Look at change in demographics of the years analysed
(data from stack over can be found here: https://insights.stackoverflow.com/survey


# Installation and Data loading:
1) From csv:
   download data from stackoverflow and save the survey_results_public.csv for each year as follows
   - \multipleYears\stack-overflow-developer-survey-2018\survey_results_public.csv
   - \multipleYears\stack-overflow-developer-survey-2019\survey_results_public.csv
   - \multipleYears\stack-overflow-developer-survey-2020\survey_results_public.csv
   - \multipleYears\stack-overflow-developer-survey-2021\survey_results_public.csv

    The contents of the survey_results_public is downloaded from stack overflow
    and then copied into the apropriate folder structure
2) From pickle:
    If the pickle file is present in the root folder then the data in the pickle
     file will be used as data source.


# Code is executed using either:
1) ipython notebook
    StackOverflowAnalyse.ipynb
2) running
    analyse.py
<img src="https://miro.medium.com/max/1209/1*KGixCUcZ-L15Q0Bwd1XiJA.png" width="800px" height="auto">

# Results:
Overall there has been large changes in the type of user that frequent stack overflow. The trend is away from the traditional groups that use stackover flow (middle aged, well education Western Europeans / Asians and North Americans) to users from other parts of the world. With many of these users being younger and have as yet not completed third level education.

Medium post discussing trends observed in data:
https://medium.com/@jodowd_87110/trends-in-stack-overflow-user-base-from-2018-to-2021-7d08a8f17315

# Acknowledgement:
The data analysed was sourced from stackoverflow. 

Respondents were recruited primarily through channels owned by Stack Overflow. The top 5 sources of respondents were onsite messaging, blog posts, email lists, Meta posts, banner ads, and social media posts. Since respondents were recruited in this way, highly engaged users on Stack Overflow were more likely to notice the links for the survey and click to begin it.

As an incentive, respondents who finished the survey could opt into a "Census" badge if they completed the survey.

You can find the official published results here:

https://insights.stackoverflow.com/survey/

Find previous survey results here:

https://insights.stackoverflow.com/survey

Legal:

This database - The Public 2021 Stack Overflow Developer Survey Results - is made available under the Open Database License (ODbL): http://opendatacommons.org/licenses/odbl/1.0/. Any rights in individual contents of the database are licensed under the Database Contents License: http://opendatacommons.org/licenses/dbcl/1.0/

TLDR: You are free to share, adapt, and create derivative works from The Public 2021 Stack Overflow Developer Survey Results as long as you attribute Stack Overflow, keep the database open (if you redistribute it), and continue to share-alike any adapted database under the ODbl.

Massive, heartfelt thanks to all Stack Overflow contributors and lurking developers of the world who took part in the survey this year. We value your generous participation more than you know. <3
