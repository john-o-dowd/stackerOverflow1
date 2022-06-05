import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import helperFunctions


class Analysis:
    def __init__(self):
        # mpl.use('Qt5Agg')
        # plt.ion()

        self.helper = helperFunctions.DataLoader('./multipleYears')
        yearsToLoad = [2018, 2019, 2020, 2021]
        columnsToLoad = ['EdLevel', 'Age', 'Gender', 'StackOverflowVisit', 'Country']
        self.all_dfs = self.helper.loadyears(yearsToLoad, columnsToLoad)
        # mpl.use('TkAgg')

        self.dataProcess = helperFunctions.DataProcess(self.all_dfs, yearsToLoad, columnsToLoad)
        self.ploty = helperFunctions.Dataplotter(yearsToLoad)

    def find_multi_year_age_profile(self):
        # Q1 change in age profile of first coding
        dfAgeProfile = self.dataProcess.find_multi_year_age_profile()
        self.ploty.plot_age_profile(dfAgeProfile)

    def find_multi_year_education_profile(self):
        # Q2 change in education background using stackoverflow over the years
        dfEduProfileMultiYear = self.dataProcess.find_multi_year_education_profile()
        self.ploty.plot_education_profile(dfEduProfileMultiYear)

    def regional_usage(self):
        # Q3 change in regional usage
        dfRegionStatsMultiYear = self.dataProcess.find_multi_year_region_profile()
        self.ploty.plot_regional_spread_change(dfRegionStatsMultiYear)

    # # load dates from csv
    # df = pd.read_csv('./singleYear/survey_results_public.csv')
    # print(df.groupby('Professional'))
    # # df categorical & quantitative
    # dfCategorical = df[df.select_dtypes(exclude=['float64']).columns]
    # dfQuantitative = df[df.select_dtypes(include=['float64']).columns]
    # # print(dfCategorical.dtypes)
    #
    # # look at the statistics for our continuous data
    # df.describe()  # gives min maxs and no. of missing values
    # df.hist()  # subplot histograms of all the continuous data
    #
    # # plt.figure()
    # # sns.heatmap(df.corr(),annot=True,fmt='.2f')
    # # plt.tight_layout()
    # # country grouping
    # respondantsCounty = df.groupby('Country').size().sort_values(ascending=False)
    # respondantsCountyProfession = df.groupby(['Country', 'Professional']).size().sort_values(ascending=False)
    # respondantsCountyProfession = respondantsCountyProfession.reset_index()
