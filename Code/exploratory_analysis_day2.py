#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
#%%
# Load the data
data = pd.read_csv('/Users/vkb5cq/Desktop/Spring 2026/BME 2315/Module-2-Epidemics-SIR-Modeling/Data/mystery_virus_daily_active_counts_RELEASE#1.csv', parse_dates=['date'], header=0, index_col=None)
#%%
# We have day number, date, and active cases. We can use the day number and active cases to fit an exponential growth curve to estimate R0.
# Let's define the exponential growth function
def exponential_growth(t, r):
    return I0 * np.exp(r * t)

# Fit the exponential growth model to the data. 
# We'll use a handy function from scipy called CURVE_FIT that allows us to fit any given function to our data. 
# We will fit the exponential growth function to the active cases data. HINT: Look up the documentation for curve_fit to see how to use it.

# Approximate R0 using this fit

# Add the fit as a line on top of your scatterplot.

data['day'] = (data['date'] - data['date'].min()).dt.days

t = data['day'].to_numpy()
I = data['active reported daily cases'].to_numpy()


# Defines exponential model

def exponential_model(t, I0, r):
    return I0 * np.exp(r * t)


# Performs curve fit
params, covariance = curve_fit(exponential_model, t, I, p0=[I[0], 0.2])

I0_fit, r_fit = params

print("Fitted I0 =", I0_fit)
print("Fitted growth rate r =", r_fit)


# Create smooth curve for plotting

t_smooth = np.linspace(min(t), max(t), 300)
I_fit = exponential_model(t_smooth, I0_fit, r_fit)


# Plot data + best-fit curve
plt.figure()
plt.scatter(t, I, label='Observed Data')
plt.plot(t_smooth, I_fit, linewidth=2, label='Best-Fit Exponential Curve')
plt.xlabel('Day')
plt.ylabel('Active Infections')
plt.title('Exponential Curve Fit to Infection Data')
plt.legend()
plt.show()


# Compute R0
# Infectious period D = 2 days
# R0 = 1 + rD

D = 2
R0 = 1 + r_fit * D

print("Estimated R0 =", R0)

# Used ChatGPT 5.2 to help learn more about the line of best fit coding 
# OpenAI. (2026). ChatGPT (GPT-5.2 Thinking) [Large language model]. https://chat.openai.com

