#%%
import pandas as pd
import matplotlib.pyplot as plt

#%%
# Load the data
data = pd.read_csv('/Users\yqr8pz\Documents\BME 2315\Module-2-Epidemics-SIR-Modeling\Data\mystery_virus_daily_active_counts_RELEASE#1.csv', parse_dates=['date'], header=0, index_col=None)

#%%
# Make a plot of the active cases over time

# Create a day number column (days since first date)
data['day'] = (data['date'] - data['date'].min()).dt.days

# Plot
plt.figure()
plt.plot(data['day'], data['active reported daily cases'])
plt.xlabel('Day')
plt.ylabel('Active Infections')
plt.title('Active Infections vs Day (Data Release #1)')
plt.show()
# %%



# Lecture Questions Post Day 1
#What do you notice about the initial infections?
 # Infections are low in the biggining but rapidly accelerating over the course of time.
#How could we measure how quickly its spreading?
 # We can measure this by studying growth rate, doubling time, and repreduction number. 
#What information about the virus would be helpful in determining the shape of the outbreak curve?
 #How the virus is transmitted (airborne, etc.), incubation period, infectious period, behavioral factors 