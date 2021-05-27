import os
import pandas as pd
import re
import matplotlib.pyplot as plt 
from datetime import date

# Read in all of the site data and create a dictionary of dataframes
# Run and the command line using python readandplot.py

def plotsitedata():
    codedir = os.getcwd() # set current working (where this code is) as a variable
    datadir = os.path.join(codedir, 'sitedata') # nested

    datafiles = ['data_site1-2.xlsx','data_site3-4.xlsx'] # list of excel datasheets to read in  
    site_dfs = {} # empty dictionary to input site data into 

    for f in datafiles:
        fpath = os.path.join(datadir,f)
        df = pd.read_excel(fpath,sheet_name='Sheet1')

        # use re module to extract site number from the file name (str)
        pattern = '([0-9])'
        sitenums = re.findall(pattern, f)

        # extract data from specifc site
        for s in sitenums:
            sitename = 'site%s' % s 
            df_s = df[df.location == sitename] # extract data with location = sitename
            df_name = 'df%s' % s # create a name for the new dataframe 
            site_dfs[df_name] = df_s

    # Extract some of the data from site 2
    df2 = site_dfs['df2']

    # get the format of the data
    type(df2['Date'].iloc[0])

    # get dates in the datetime.date (seems to be a better format for plotting than time stamps)
    d = df2['Date'].apply(lambda x: date(x.year, x.month, x.day)) # creates a df of datetime.date (could add this back onto the original array)
    d = d.values # extract values to an array

    # get temp, ec, ph data
    temp = df2['Temp C'].values
    ec = df2['EC (mS/cm)'].values
    ph = df2['pH'].values    

    # Plot the data
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize = (12,8))

    ax1b = ax1.twinx() # for plotting on secondary y axis
    ax1.plot(d, temp, c='blue', marker='x', lw=2, ls='-')
    ax1b.plot(d, ec, c='orange', marker='x', lw=2, ls='-')
    ax2.plot(d, ec, c='brown', marker='x', lw=2, ls='-')

    ax1.tick_params(labelbottom=False) # turn off x tick labels on ax1
    ax2.tick_params(axis='x', labelrotation=70, labelsize = 14)

    # set axes titles
    fs = 20
    ax1.set_ylabel('Temp (C', fontsize=fs)
    ax1b.set_ylabel('EC (mS/cm)', fontsize=fs)
    ax2.set_ylabel('pH', fontsize=fs)

    # Save the plot

    # if there is no file dir 'figures' then create open
    figdir = os.path.join(codedir, 'figures')

    if os.path.isdir(figdir) == False:  
        os.makedirs(figdir)

    pltname = 'site2timeseries.png' # format inferred from extension 
    fname = os.path.join(figdir,pltname)
    fig.savefig(fname)

    return('Created figure: %s' % fname)

if __name__ == "__main__":
    plotsitedata()

