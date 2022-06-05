- Analyse multiple years worth of stack overflow user survey data
- Look at change in demographics of the years analysed
(data from stack over can be found here: https://insights.stackoverflow.com/survey

Code is executed using either:
1) ipython notebook
    StackOverflowAnalyse.ipynb
2) running
    run_analyse.py

Data loading:
1) From csv:
   \multipleYears\stack-overflow-developer-survey-2018\survey_results_public.csv
   \multipleYears\stack-overflow-developer-survey-2019\survey_results_public.csv
   \multipleYears\stack-overflow-developer-survey-2020\survey_results_public.csv
   \multipleYears\stack-overflow-developer-survey-2021\survey_results_public.csv

    The contents of the survey_results_public is downloaded from stack overflow
    and then copied into the apropriate folder structure
2) From pickle:
    If the pickle file is present in the root folder then the data in the pickle
     file will be used as data source.
