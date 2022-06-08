import os
import pandas as pd
import matplotlib.pyplot as plt
import pycountry_convert as pc
import difflib
import pycountry
import pygal
from pygal.style import Style
import pickle
from os.path import exists


class DataLoader:

    def __init__(self, folder):
        # check what data is available (in csv format)
        # folders=os.listdir(folder)
        self.folder = folder


        self.pickleLocation = "loaded_data.p"
        self.picklePresent = exists("loaded_data.p")

    def loadyears(self, years, columns):

        if self.picklePresent:
            with open(self.pickleLocation, 'rb') as handle:
                all_dfs = pickle.load(handle)
        else:

            ################################
            # Load the requested data for multiple years
            ################################
            # years=years to load
            folders = os.listdir(self.folder)
            self.yearFolders = [s for s in folders if "zip" not in s]
            self.yearsAvailable = [(int(s[-4:])) for s in folders if "zip" not in s]
            if all(elem in self.yearsAvailable for elem in years):  # check the years are available to load
                print("all years are available")
                locs = []  # file indices to load
                for year in years:
                    locs.append([i for i, s in enumerate(self.yearFolders) if str(year) in s])
            else:
                locs = []
                exit('999:some of the requested years are not available')

            # define column aliases as the names of columns changed a bit over the years in the source data
            col_aliases = {'EdLevel': ['EdLevel', 'FormalEducation'],
                           'Age': ['Age'],
                           'Gender': ['Gender'],
                           'StackOverflowVisit': ['StackOverflowVisit', 'SOVisitFreq'],
                           'Professional': ['Professional'],
                           # 'Age1stCode': ['Age1stCode'],#not present in 2019 so dont use
                           'Country': ['Country']}
            all_dfs = []
            for loc in locs:  # files to load (each file is a different year)
                print(self.yearFolders[loc[0]])
                df = pd.read_csv(f'./multipleYears/{self.yearFolders[loc[0]]}/survey_results_public.csv', nrows=10)
                colsPresent = (set(df.columns))
                cols2Load = []
                for column in columns:
                    cols2Load.append(set.intersection(set(col_aliases[column]), set(colsPresent)).pop())
                newDF = \
                    pd.read_csv(f'./multipleYears/{self.yearFolders[loc[0]]}/survey_results_public.csv', usecols=cols2Load,
                                low_memory=False)[cols2Load]
                newDF.columns = columns  # make the column labesl consistent (use common column alias)
                all_dfs.append(newDF)

                with open(self.pickleLocation, 'wb') as handle:
                    pickle.dump(all_dfs, handle)


        return all_dfs



class DataProcess:
    def __init__(self, all_dfs, years, columns_loaded):
        self.years = years
        self.allDfs = all_dfs
        self.columnsLoaded = columns_loaded

    def age_profile_aliases(self):
        # the age groupings are a bit too granular so further group them
        self.yearAliases = {'Under 18 years old': ['Under 18 years old'],
                       '18 - 24 years old': ['18 - 24 years old', '18-24 years old'],
                       '25 - 34 years old': ['25 - 34 years old', '25-34 years old'],
                       '35 - 44 years old': ['35 - 44 years old', '35-44 years old'],
                       '45 - 54 years old': ['45 - 54 years old', '45-54 years old'],
                       '55 - 64 years old': ['55 - 64 years old', '55-64 years old'],
                       '65 years or older': ['65 years or older']
                       }
        self.yearsToGroup = {'under24': ['Under 18 years old', '18 - 24 years old'],
                        '24-55': ['25 - 34 years old', '35 - 44 years old', '45 - 54 years old'],
                        'over55': ['55 - 64 years old', '65 years or older']}
        self.yearsToGroupNumeric = {'under24': [6, 24],
                               '24-55': [25, 54],
                               'over55': [55, 90]}

    def find_multi_year_age_profile(self):

        # dfSingleYearDF[(dfSingleYearDF['Age'] < 16) & (dfSingleYearDF['Age'] > 10)][0].sum()

        dfAgeProfile = pd.DataFrame()
        dfAgeProfile['ageRange'] = self.yearsToGroup.keys()
        for itt, year in enumerate(self.years):
            dfSingleYear = self.allDfs[itt].value_counts(subset=['Age'], dropna=True)
            # temp['25 - 34 years old']

            keys = list(yearsToGroup.keys())  # year groupings (i.e. under 24)
            subgroupCounters = []
            if len(dfSingleYear.keys()) > 20:  # some years dont have groupings in the source data
                for key in self.yearsToGroupNumeric.keys():
                    start = self.yearsToGroupNumeric[key][0]
                    end = self.yearsToGroupNumeric[key][1]
                    dfSingleYearDF = pd.DataFrame(dfSingleYear)
                    dfSingleYearDF = dfSingleYearDF.reset_index()
                    subgroupCounters.append(
                        dfSingleYearDF[(dfSingleYearDF['Age'] > start) & (dfSingleYearDF['Age'] < end)][0].sum())
            else:  # if the years are grouped then the datatype for age is a string
                for key in keys:  # iterate over each age group
                    groups2Load = yearsToGroup[key]
                    subgroupCounter = 0
                    for group in groups2Load:  # iterate over the age subgroups that are to be aggregated
                        # check aliases of group to see which one is in use
                        subGroupAliases = yearAliases[group]
                        ageGroupsInCurYear = list(pd.DataFrame(dfSingleYear).reset_index()['Age'])
                        subgroupCounter = subgroupCounter + dfSingleYear[
                            set.intersection(set(subGroupAliases), set(ageGroupsInCurYear)).pop()]
                    subgroupCounters.append(subgroupCounter)
            dfAgeProfile[year] = subgroupCounters
        return dfAgeProfile

    def find_multi_year_education_profile(self):
        # check the number of professionals in the US

        educationAliases = {'Some college/university study without earning a degree': [
            'Some college/university study without earning a degree'],
            'Professional degree (JD, MD, etc.)': ['Professional degree (JD, MD, etc.)'],
            'Bachelor’s degree (BA, BS, B.Eng., etc.)': ['Bachelor’s degree (BA, BS, B.Eng., etc.)',
                                                         'Bachelor’s degree (B.A., B.S., B.Eng., etc.)'],
            'Associate degree': ['Associate degree', 'Associate degree (A.A., A.S., etc.)'],
            'Master’s degree (MA, MS, M.Eng., MBA, etc.)': [
                'Master’s degree (MA, MS, M.Eng., MBA, etc.)',
                'Master’s degree (M.A., M.S., M.Eng., MBA, etc.)'],
            'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)': [
                'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)'],
            'Primary/elementary school': ['Primary/elementary school'],
            'Other doctoral degree (Ph.D, Ed.D., etc.)': ['Other doctoral degree (Ph.D, Ed.D., etc.)',
                                                          'Other doctoral degree (Ph.D., Ed.D., etc.)']}
        educationPlotAliases = {'Some college/university study without earning a degree': 'College without degree',
                                'Professional degree (JD, MD, etc.)': 'Professional degree',
                                'Bachelor’s degree (BA, BS, B.Eng., etc.)': 'Bachelor’s degree',
                                # 'I never completed any formal education':'Something Else',
                                'Associate degree': 'Associate degree',
                                'Master’s degree (MA, MS, M.Eng., MBA, etc.)': 'Master’s degree',
                                'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)':
                                    'Secondary school',
                                'Primary/elementary school': 'Primary school',
                                'Other doctoral degree (Ph.D, Ed.D., etc.)': 'Other Doctoral degree'
                                }

        years = self.years

        dfEduProfileMultiYear = pd.DataFrame()
        dfEduProfileMultiYear['EdLevel'] = list(educationPlotAliases.values())

        for itt, year in enumerate(years):
            dfEduSingleYear = self.allDfs[itt]
            singleYearCounters = []
            for group in educationAliases.keys():  # itterate through each group of eductation type
                curEduAlias = set.intersection(set(educationAliases[group]), set(dfEduSingleYear.EdLevel.unique()))
                singleYearCounters.append(dfEduSingleYear.EdLevel.value_counts()[list(curEduAlias)].values[0])
            dfEduProfileMultiYear[year] = singleYearCounters

        return dfEduProfileMultiYear

    def find_multi_year_region_profile(self):
        dfRegionStatsMultiYear = []
        for yearItt, year in enumerate(self.years):
            dfRegionsSingleYear = self.allDfs[yearItt]

            def countries_available():
                allCountries_avail = []
                for country_avail in list(pycountry.countries):
                    allCountries_avail.append(country_avail.name)
                return allCountries_avail

            def country_to_continent(country_name):
                country_alpha2 = pc.country_name_to_country_alpha2(country_name)
                country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
                country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
                return country_continent_name

            allCountries = countries_available()
            foundCountries = []
            foundContinents = []
            nValuesPerCountry = []
            countriesValueCounts = dfRegionsSingleYear.Country.value_counts().sort_values()
            for country, value in countriesValueCounts.items():
                # noinspection PyBroadException
                try:
                    if country_to_continent(country):
                        foundCountries.append(country)
                        foundContinents.append(country_to_continent(country))
                        nValuesPerCountry.append(value)
                except:  # country not matched so look for a country with a similar name
                    closestMatch = difflib.get_close_matches(country, allCountries)
                    if len(closestMatch) > 0:
                        foundCountries.append(closestMatch[0])
                        foundContinents.append(country_to_continent(closestMatch[0]))
                        nValuesPerCountry.append(value)
            dfRegionStats = pd.DataFrame()
            dfRegionStats['Countries'] = foundCountries
            dfRegionStats['Continents'] = foundContinents
            dfRegionStats['No. People'] = nValuesPerCountry
            dfRegionStatsMultiYear.append(dfRegionStats)
        return dfRegionStatsMultiYear


class Dataplotter:
    def __init__(self, years_to_load):
        self.yearsToLoad = years_to_load

    def plot_age_profile(self, df_age_profile):
        # the age groupings are a bit too granular so further group them
        plt.figure(f'Age profile for last {len(self.yearsToLoad)}-years')
        plt.title(f'Age profile for last {len(self.yearsToLoad)}-years')
        for year in self.yearsToLoad:
            plt.plot(df_age_profile.ageRange, 100*(df_age_profile[year] / df_age_profile[year].sum()))
        plt.legend(self.yearsToLoad)
        plt.xlabel('Age bands')
        plt.ylabel('Percent (%)')

        plt.figure('Change in age distribution vs. time')
        for ageGroup in df_age_profile['ageRange']:
            ageGroupVsYears = df_age_profile[df_age_profile['ageRange'] == ageGroup].iloc[0].values[1:]
            ageGroupRatios = ageGroupVsYears / df_age_profile.sum()[1:]
            ageGroupNormPercChng = (100 * ageGroupRatios / ageGroupRatios.values[0]) - 100
            plt.plot(list(map(str, self.yearsToLoad)), ageGroupNormPercChng)
        plt.legend(df_age_profile['ageRange'])
        plt.xlabel("Years")
        plt.ylabel('Percent (%)')

    def plot_education_profile(self, df_edu_profile_multi_year):

        plt.figure(f'Education profile for last {len(self.yearsToLoad)}-years')
        plt.title(f'Education profile for last {len(self.yearsToLoad)}-years')
        plt.xticks(rotation=90)
        for year in self.yearsToLoad:
            plt.plot(df_edu_profile_multi_year['EdLevel'], 100*(df_edu_profile_multi_year[year] /
                     df_edu_profile_multi_year[year].sum()))
        plt.legend(self.yearsToLoad)
        plt.xlabel('Education bands')
        plt.ylabel('Percent (%)')
        plt.tight_layout()

        plt.figure('Change in Education distribution vs. time')
        for eduGroup in df_edu_profile_multi_year['EdLevel']:
            eduGroupVsYears = df_edu_profile_multi_year[df_edu_profile_multi_year['EdLevel'] ==
                                                        eduGroup].iloc[0].values[1:]
            eduGroupRatios = eduGroupVsYears / df_edu_profile_multi_year.sum()[1:]
            eduGroupNormPercChng = (100 * eduGroupRatios / eduGroupRatios.values[0]) - 100
            plt.plot(list(map(str, self.yearsToLoad)), eduGroupNormPercChng)
        plt.legend(df_edu_profile_multi_year['EdLevel'])
        plt.xlabel("Years")
        plt.ylabel("Percent (%)")

    @staticmethod
    def plot_regional_spread_change(df_region_stats_multi_year):

        continentStats_beginYear = df_region_stats_multi_year[0].groupby(["Continents"]).sum()
        continentStats_beginYear = continentStats_beginYear.reset_index()
        continentStats_endYear = df_region_stats_multi_year[-1].groupby(["Continents"]).sum()
        continentStats_endYear = continentStats_endYear.reset_index()
        # continentStats=dfRegionStatsMultiYear.groupby(["Continents"]).sum()

        continentAliases = {'Africa': 'africa',
                            'Asia': 'asia',
                            'Europe': 'europe',
                            'North America': 'north_america',
                            'Oceania': 'oceania',
                            'South America': 'south_america'}

        ##########################################################
        # Where do the users principally live
        ##########################################################

        # generate colours for the ranges of continent size
        ranges_df = pd.DataFrame(columns=['label', 'lowThreshold', 'highThreshold', 'colour'])
        ranges_df = pd.concat([ranges_df, pd.DataFrame.from_records([{'label': 'reallySmall', 'lowThreshold': 0,
                                                                      'highThreshold': 10, 'colour': '#98FB98'}])])
        ranges_df = pd.concat([ranges_df, pd.DataFrame.from_records([{'label': 'Small', 'lowThreshold': 10,
                                                                      'highThreshold': 20, 'colour': '#7CFC00'}])])
        ranges_df = pd.concat([ranges_df, pd.DataFrame.from_records([{'label': 'Big', 'lowThreshold': 20,
                                                                      'highThreshold': 30, 'colour': '#3CB371'}])])
        ranges_df = pd.concat([ranges_df, pd.DataFrame.from_records([{'label': 'VeryBig', 'lowThreshold': 30,
                                                                      'highThreshold': 100, 'colour': '#006400'}])])

        # colours and legend text
        colours = []
        proportions = {}
        for continent in continentStats_beginYear.Continents.values:
            endPeopleTotal = continentStats_endYear["No. People"].sum()
            endPeopleCurcon = continentStats_endYear[continentStats_endYear["Continents"]
                                                     == continent]['No. People'].iloc[0]
            proportion = (endPeopleCurcon / endPeopleTotal) * 100
            colours.append(ranges_df.loc[(ranges_df['lowThreshold'] <= proportion) &
                                         (ranges_df['highThreshold'] > proportion)]['colour'][0])
            proportions[continent] = proportion
        custom_style = Style(colors=colours)

        # adding the continents
        worldmap1 = pygal.maps.world.SupranationalWorld(style=custom_style, truncate_legend=22)
        for continent in continentStats_beginYear.Continents.values:
            worldmap1.add(f"{continent} ({proportions[continent]:.1f}%)", [(continentAliases[continent])])
        # save into the file
        worldmap1.render_to_file('WhereUsersLive.svg')

        ##########################################################
        # proportional change for each continent
        ##########################################################
        proportialChangeForEachContinent = {}  # look at how much a continent has changed relative to itselt
        for continent in continentStats_beginYear.Continents.values:
            startPeopleTotal = continentStats_beginYear["No. People"].sum()
            endPeopleTotal = continentStats_endYear["No. People"].sum()
            startPeopleCurcon = \
                continentStats_beginYear[continentStats_beginYear["Continents"] == continent]['No. People'].iloc[0]
            endPeopleCurcon = \
                continentStats_endYear[continentStats_endYear["Continents"] == continent]['No. People'].iloc[0]
            # adding the continents
            propChange = (100 * (endPeopleCurcon / endPeopleTotal) / (startPeopleCurcon / startPeopleTotal)) - 100
            proportialChangeForEachContinent[continent] = propChange

        # create a world map for proportional change of each continent

        ranges_df = pd.DataFrame(columns=['label', 'lowThreshold', 'highThreshold', 'colour'])
        ranges_df = pd.concat([ranges_df, pd.DataFrame.from_records([{'label': 'decreasingFast', 'lowThreshold': -100,
                                                                      'highThreshold': -5, 'colour': '#FF0000'}])])
        ranges_df = pd.concat([ranges_df, pd.DataFrame.from_records([{'label': 'decreasingSlow', 'lowThreshold': -5,
                                                                      'highThreshold': -1, 'colour': '#F08080'}])])
        ranges_df = pd.concat([ranges_df, pd.DataFrame.from_records([{'label': 'limitedChange', 'lowThreshold': -1,
                                                                      'highThreshold': 1, 'colour': '#F5F5DC'}])])
        ranges_df = pd.concat([ranges_df, pd.DataFrame.from_records([{'label': 'increasingSlow', 'lowThreshold': 1,
                                                                      'highThreshold': 5, 'colour': '#00FF00'}])])
        ranges_df = pd.concat([ranges_df, pd.DataFrame.from_records([{'label': 'increasingFast', 'lowThreshold': 5,
                                                                      'highThreshold': 100, 'colour': '#008000'}])])

        # asign colour and legend text
        colours = []
        for continent in continentStats_beginYear.Continents.values:
            change = proportialChangeForEachContinent[continent]
            colours.append(
                ranges_df.loc[(ranges_df['lowThreshold'] <= change) & (ranges_df['highThreshold'] > change)]['colour'][
                    0])
        custom_style = Style(colors=colours)
        worldmap = pygal.maps.world.SupranationalWorld(style=custom_style, truncate_legend=22)
        # worldmap.title = 'Continents'

        # adding the continents
        for continent in continentStats_beginYear.Continents.values:
            worldmap.add(f"{continent} ({proportialChangeForEachContinent[continent]:.1f}%)",
                         [(continentAliases[continent])])
        # save into the file
        worldmap.render_to_file('proportionalChangeInLocation.svg')
        #worldmap.render_to_png('./proportionalChangeInLocation.png')

        #re render svg as png as it is easier to load into jupyter notebook (currently not working due to svg3rlg bug)
        # -*- coding: utf-8 -*-
        # drawing = svg2rlg('proportionalChangeInLocation.svg')
        # renderPM.drawToFile(drawing, 'proportionalChangeInLocation.png', fmt='PNG')