# Created on: 20230321
# Description: This program copies a csv file and replaces key fields.
# First Step: https://www.microsoft.com/en-us/download/details.aspx?id=53339  x64
# Second Step: Use cmd as admin to install cd C:\Python36\Scripts> pip install pyodbc
# C:\Users\ekyi\PycharmProjects
# ---------------------------------------------------------------------------
# This is created by Eint on Python 3.11

#import necessary packages
import pandas as pd
import numpy as np
import plotly.express as px
import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as tls


data = pd.read_csv('data.csv', encoding = 'unicode_escape') #read CSV file
data = data.drop(data.columns[[2, 12,13,14,15]], axis =1) #drop uncessary columns
print(data.dtypes) #look at data type
data = data.set_axis(['Year', 'Population', 'Under 15K', '15K to 25K', '25K to 35K','35K to 50K','50K to 75K','75K to 100K','100K to 150K','150K to 200K','Over 200K'], axis=1) #rename columns
data = data.dropna() #drop rows with NAs
data = data.reset_index(drop = True) #reset index


Year = data['Year'] #extract Year to add to dataset after

data['Population'] = data['Population'].replace({',':''}, regex = True) #remove ',' from Population data
data['Population'] = data['Population'].astype(int) #convert Population from string to int
Population = data['Population'] #extract Population to add to dataset after

Race = ['White', 'Black','Asian','Native American','Hispanic'] #create df for race
Race = pd.DataFrame(Race)

#calculate the percent of population where data was collected
data1 = data[['Under 15K', '15K to 25K', '25K to 35K','35K to 50K','50K to 75K','75K to 100K','100K to 150K','150K to 200K','Over 200K']].mul(data['Population'], axis = 0)
data1 = data1[['Under 15K', '15K to 25K', '25K to 35K','35K to 50K','50K to 75K','75K to 100K','100K to 150K','150K to 200K','Over 200K']].div(100)

#add Year, Population, Race to Data1
data1['Population'] = Population
data1['Year'] = Year
data1['Race'] = np.repeat(Race, 20)


data1 = data1.sort_values('Year', ascending=True) #sort Data1 by Year ascending


note = 'United States Census Bureau: https://data.census.gov/' #source footnote to add to plots


data1_melt = pd.melt(data1, id_vars= ['Year','Race','Population'], value_vars = (['Under 15K', '15K to 25K', '25K to 35K',
                                                                                  '35K to 50K','50K to 75K','75K to 100K',
                                                                                  '100K to 150K','150K to 200K','Over 200K'])) #melt the dataframe for easy plotting

#Plotly Figure 1
fig1 = px.bar(data1_melt, x ='variable', y = 'value', animation_frame='Year',color = 'Race',
                    animation_group='variable', hover_name = 'Race', range_y = [0, 25000])

fig1.update_layout(title = dict(text = 'Median Income Across Race by Population Size From 2002 - 2021', font = dict(size = 30), automargin = True, yref = 'paper'), plot_bgcolor = 'rgb(250, 250, 250)',
                   showlegend = True, xaxis_title = dict(text = 'Income Brackets (in $)', font = dict(size = 15)),  yaxis_title = dict(text = 'Population (in thousands)', font = dict(size = 15)),
                    legend_title = dict(text = 'Race', font = dict(size = 18))) #change/edit plot aesthetics


#add annotation for data source
fig1.add_annotation(
    showarrow=False,
    text= note,
    yref = 'paper',
    xref ='paper',
    x = 1,
    y = -0.05,
    font = dict(size =10))


fig1.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000 #slow down frame transition
fig1.update_traces(opacity = 0.7) #Decrease opacity for aesthetics
fig1.show()


##Data2 for percent of Income##
data2 = data


data2['Race'] = np.repeat(Race, 20) #repeat Race df 20 times to match data2


data2 = data2.sort_values('Year', ascending=True) #sort Year by ascending


data2_melt = pd.melt(data2, id_vars= ['Year','Race','Population'], value_vars = (['Under 15K', '15K to 25K', '25K to 35K',
                                                                                  '35K to 50K','50K to 75K','75K to 100K',
                                                                                  '100K to 150K','150K to 200K','Over 200K'])) #melt the dataframe for easy plotting

#Plotly Figure 2
fig2 = px.scatter(data2_melt, x ='variable', y = 'value', animation_frame='Year', size= 'Population', color = 'Race', size_max= 60,
                    animation_group='variable', hover_name = 'Race', range_y=[0,25])

fig2.update_layout(title = dict(text = 'Percent of Median Income Across Race From 2002 - 2021', font = dict(size = 30), automargin = True, yref = 'paper'), plot_bgcolor = 'rgb(250, 250, 250)',
                   showlegend = True, xaxis_title = dict(text = 'Income Brackets (in $)', font = dict(size = 15)),  yaxis_title = dict(text = 'Percent of Population (%)', font = dict(size = 15)),
                    legend_title = dict(text = 'Race', font = dict(size = 18))) #change/edit plot aesthetics

#add annotation for data source
fig2.add_annotation(
    showarrow=False,
    text= note,
    yref = 'paper',
    xref ='paper',
    x = 1,
    y = -0.05,
    font = dict(size =10))


fig2.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000 #slow down frame transition
fig2.update_traces(opacity = 0.7) #decrease opacity for aesthetics
fig2.show()

chart_studio.tools.set_credentials_file(username = 'ekyi', api_key = 'eDKF3ElHcVIMDKAnKe3s') #API key generated from Plotly profile
py.plot(fig1, filename = 'Median_Income', auto_open = True)
py.plot(fig2, filename = 'Percent_Median', auto_open = True)
