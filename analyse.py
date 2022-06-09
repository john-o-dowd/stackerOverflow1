import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import helperFunctions

mpl.use('Qt5Agg')
plt.ion()

helper = helperFunctions.DataLoader('./multipleYears')
yearsToLoad = [2018, 2019, 2020, 2021]
columnsToLoad = ['EdLevel', 'Age', 'Gender', 'StackOverflowVisit', 'Country']
all_dfs = helper.loadyears(yearsToLoad, columnsToLoad)
# mpl.use('TkAgg')

dataProcess = helperFunctions.DataProcess(all_dfs, yearsToLoad, columnsToLoad)
ploty = helperFunctions.Dataplotter(yearsToLoad)

# Q1 change in age profile of first coding
dataProcess.age_profile_aliases()  # generate aliases for age profile
dfAgeProfile = dataProcess.find_multi_year_age_profile()
ploty.plot_age_profile(dfAgeProfile)

# Q2 change in education background using stackoverflow over the years
dataProcess.education_profile_aliases()
dfEduProfileMultiYear = dataProcess.find_multi_year_education_profile()
ploty.plot_education_profile(dfEduProfileMultiYear)

# Q3 change in regional usage
dfRegionStatsMultiYear = dataProcess.find_multi_year_region_profile()
ploty.plot_regional_spread_change(dfRegionStatsMultiYear)

print("hi")

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
