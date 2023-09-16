#import libaraies
import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

#URL to be Scaped
url = 'https://www.basketball-reference.com/leagues/NBA_2023_totals.html'

#check response
response= requests.get(url)
print(response)

#check content
html = response.content
soup = BeautifulSoup(html,'html.parser')
print(soup.head.text)

response = requests.get(url)

#collect data in table format to DF
dfs= pd.read_html(response.text)
df=dfs[0]
print(df.head())

#Check df.head()
df.head()
#Check df.tail()
df.tail()

#Saving the raw data as csv using utf-8 as the player names contain speical characters
df.to_csv('2022_23_NBA_Stats_Raw.csv', encoding = 'utf-8' )

#Drop all rows contining RK in Column Rk as it is the title headings
df = df[df['Rk'] != 'Rk']
#Drop column Rk as unneeded.
df.drop(columns = 'Rk', inplace = True)

#Creating a save point for the cleaned data.
#Reopen the csv as now that the we have dropped the title rows containing 'Rk' the remaining data should be recongnized as numbers
df.to_csv('2022_23_NBA_Stats_Cleaned.csv', encoding = 'utf-8', index = False )
nba_df = pd.read_csv('2022_23_NBA_Stats_Cleaned.csv')

#Creating per game calulations and new columns
nba_df['PPG'] = nba_df['PTS']/nba_df['G']
nba_df['RPG'] = nba_df['TRB']/nba_df['G']
nba_df['APG'] = nba_df['AST']/nba_df['G']
nba_df['SPG'] = nba_df['STL']/nba_df['G']
nba_df['BPG'] = nba_df['BLK']/nba_df['G']
nba_df.head()
#Creating another save point
nba_df.to_csv('2022_23_NBA_Stats_PerGame.csv', encoding = 'utf-8', index = False )

#Work off the latest iteration of saved data
nba_df = pd.read_csv('2022_23_NBA_Stats_PerGame.csv')

#Calulating league means.  for FT$, FG% and 3P%, we will calculate the mean less the 0 values.
ftp_mean = nba_df[nba_df['FT%']!= 0]['FT%'].mean()
fgp_mean = nba_df[nba_df['FG%'] !=0 ]['FG%'].mean()
tpp_mean = nba_df[nba_df['3P%']!= 0]['3P%'].mean()
ppg_mean = nba_df['PPG'].mean()
rpg_mean = nba_df['RPG'].mean()
apg_mean = nba_df['APG'].mean()
spg_mean = nba_df['SPG'].mean()
bpg_mean = nba_df['BPG'].mean()

print('ftp_mean:', ftp_mean)
print('fgp_mean:', fgp_mean)
print('tpp_mean:', tpp_mean)
print('ppg_mean:', ppg_mean)
print('rpg_mean:', rpg_mean)
print('apg_mean:', apg_mean)
print('spg_mean:', spg_mean)
print('bpg_mean:', bpg_mean)

#Create leauge_means_df

league_mean_df = pd.DataFrame({
    'FT%': [ftp_mean],
    'FG%': [fgp_mean],
    '3P%': [tpp_mean],
    'PPG': [ppg_mean],
    'RPG': [rpg_mean],
    'APG': [apg_mean],
    'SPG': [spg_mean],
    'BPG': [bpg_mean]
})
#Finding MVP values. MVP = Joel Embiid

mvp_ftp = nba_df.loc[nba_df['Player'] == 'Joel Embiid', 'FT%'].values[0]
mvp_fgp = nba_df.loc[nba_df['Player'] == 'Joel Embiid', 'FG%'].values[0]
mvp_tpp = nba_df.loc[nba_df['Player'] == 'Joel Embiid', '3P%'].values[0]
mvp_ppg = nba_df.loc[nba_df['Player'] == 'Joel Embiid', 'PPG'].values[0]
mvp_rpg = nba_df.loc[nba_df['Player'] == 'Joel Embiid','RPG'].values[0]
mvp_apg = nba_df.loc[nba_df['Player'] == 'Joel Embiid', 'APG'].values[0]
mvp_spg = nba_df.loc[nba_df['Player'] == 'Joel Embiid', 'SPG'].values[0]
mvp_bpg = nba_df.loc[nba_df['Player'] == 'Joel Embiid', 'BPG'].values[0]

print('mvp_ftp:', mvp_ftp)
print('mvp_fgp:', mvp_fgp)
print('mvp_tpp:', mvp_tpp)
print('mvp_ppg:', mvp_ppg)
print('mvp_rpg:', mvp_rpg)
print('mvp_apg:', mvp_apg)
print('mvp_spg:', mvp_spg)
print('mvp_bpg:', mvp_bpg)

#Creating a DF for MVP stats

mvp_df = pd.DataFrame({
    'FT%': [mvp_ftp],
    'FG%': [mvp_fgp],
    '3P%': [mvp_tpp],
    'PPG': [mvp_ppg],
    'RPG': [mvp_rpg],
    'APG': [mvp_apg],
    'SPG': [mvp_spg],
    'BPG': [mvp_bpg]
})

#Plotting the data using matplotlib
#Get the column names
column_names = league_mean_df.columns

#Get the data values from the DataFrames
league_mean = league_mean_df.values.squeeze()
mvp = mvp_df.values.squeeze()

#Set the figure size
plt.figure(figsize=(10, 6))

#Set the bar width
bar_width = 0.35

#Set the x coordinates for the bars
index = range(len(column_names))

#Create the bar plot for league mean
plt.bar(index, league_mean, bar_width, label='League Average')

#Create the bar plot for Joel Embiid
plt.bar([i + bar_width for i in index], mvp, bar_width, label='MVP - Joel Embiid')

#Set the x-axis tick labels
plt.xticks([i + bar_width/2 for i in index], column_names)

#Add labels and title
plt.xlabel('Categories')
plt.ylabel('Values')
plt.title('Comparison of League Average vs MVP')

#Add legend
plt.legend()

plt.savefig('League Average vs MVP.png')
plt.show()