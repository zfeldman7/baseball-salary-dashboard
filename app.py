#!/usr/bin/env python
# coding: utf-8

# # Visualizing Baseball Salaries
# 
# This is a small notebook that does a simple visualization of Major League Baseball players' salary trends, using a dataset we've seen in previous weeks of this course.
# 
# ## Load the dataset
# 
# First, we load the dataset we're familiar with, and remember what it contains.
import streamlit as st
import pandas as pd
df = pd.read_csv( 'baseball-salaries-simplified.csv' )
df.head()

st.title('Major League Baseball Salaries')
# ## Filter the dataset
# 
# Just as an example, we'll focus our attention on third basemen in the years from 2000 to 2010, inclusive.
year_range = st.sidebar.slider('Years to include:', 1988, 2016, (2000, 2011), 1)
year_start = year_range[0]
year_end = year_range[1]
# year_start = st.sidebar.slider('Choose the starting year', 1988, 2020, 2000, 1)
# year_end = st.sidebar.slider('Choose the ending year', 1988, 2020, 2011, 1)
position_list = ['3B', '2B', '1B', 'OF', 'P', 'DH', 'C', 'SS', 'CF', 'RF', 'LF', 'RP', 'SP']
def get_position_name(position_key):
	positions = {
		'3B': 'Third Base',
		'2B': 'Second Base',
		'1B': 'First Base',
		'OF': 'Outfield',
		'P': 'Pitcher',
		'DH': 'Designated Hitter',
		'C': 'Catcher',
		'SS': 'Short Stop',
		'CF': 'Center Field',
		'RF': 'Right Field',
		'LF': 'Left Field',
		'RP': 'Relief Pitcher',
		'SP': 'Starting Pitcher'
	}
	return positions[position_key]

position = st.sidebar.selectbox('Choose the position you would like to graph', position_list, format_func=get_position_name, index=0)


year_range = (df.year >= year_start) & (df.year <= year_end )
focus_pos = df.pos == position
focus = df[year_range & focus_pos]
focus.head()


# ## Create a table of percentiles
# 
# I'm interested in seeing trends in the entire dataset.  There are so many data points that if we plotted them all, the graph would be quite busy.  So I'll plot the various percentiles of the data over time instead.  To do so, we must first compute what those percentiles are.

# Which years do we care about?
years = range( year_start, year_end + 1)

# We'll store the results in a new DataFrame.
df_pcts = pd.DataFrame( { "year" : years } )

# How to compute a percentile in a given year:
def percentile_in_year ( year, percent ):
    return focus[focus.year == year].salary.quantile( percent/100 )

# Fill the DataFrame using that function.
for percent in range( 0, 110, 10 ):
    df_pcts[percent] = [ percentile_in_year( year, percent ) for year in years ]

# Make years the index.
df_pcts.index = df_pcts.year
del df_pcts['year']

# Change units to millions of dollars.
df_pcts /= 1000000


# ## Plot the data
# 
# Now we can view the trends in the salary distribution over time.

import matplotlib.pyplot as plt
df_pcts.plot( legend='upper left' )
plt.gcf().set_size_inches(8,10)
plt.title( f'Salaries for {get_position_name(position)} ({len(focus)} players)', fontsize=20 )
plt.xticks( df_pcts.index, rotation=90 )
plt.ylabel( 'Salary percentiles in $1M', fontsize=14 )
plt.xlabel( None )

#st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot(plt.gcf()) # edited for streamlit


st.header(f'''
Highest salaries for {get_position_name(position)}, {year_start}-{year_end}
''')
# See result.

st.dataframe( focus.nlargest( 10, 'salary' ).reset_index( drop=True ) )


# ## Investigate Extreme Values
# 
# Makes you wonder who created the spikes on the graph...Let's find out.

focus.nlargest( 10, 'salary' ).reset_index( drop=True )

