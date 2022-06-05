import analyse
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.use('Qt5Agg')
# plt.ion()
analyse_so=analyse.Analysis()
analyse_so.find_multi_year_age_profile()
analyse_so.find_multi_year_education_profile()
analyse_so.regional_usage()
plt.show()