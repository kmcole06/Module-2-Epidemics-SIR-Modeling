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



#%% ===============================
# Estimate beta, sigma, gamma using grid search + Euler method
#=================================

# Initial population assumptions
N = 1000000

I0 = I[0]
E0 = I0
R0_init = 0
S0 = N - I0 - E0

# Euler SEIR model
def euler_SEIR(beta, sigma, gamma):

    S = np.zeros(len(t))
    E = np.zeros(len(t))
    I_model = np.zeros(len(t))
    R = np.zeros(len(t))

    S[0] = S0
    E[0] = E0
    I_model[0] = I0
    R[0] = R0_init

    dt = 1

    for i in range(len(t)-1):

        dS = -beta * S[i] * I_model[i] / N
        dE = beta * S[i] * I_model[i] / N - sigma * E[i]
        dI = sigma * E[i] - gamma * I_model[i]
        dR = gamma * I_model[i]

        S[i+1] = S[i] + dS * dt
        E[i+1] = E[i] + dE * dt
        I_model[i+1] = I_model[i] + dI * dt
        R[i+1] = R[i] + dR * dt

    return S, E, I_model, R


# Parameter ranges to test
beta_range = np.linspace(0.1,1.0,15)
sigma_range = np.linspace(0.1,1.0,15)
gamma_range = np.linspace(0.05,0.5,15)

best_SSE = np.inf
best_beta = None
best_sigma = None
best_gamma = None


# Grid search
for b in beta_range:
    for s in sigma_range:
        for g in gamma_range:

            S,E,I_model,R = euler_SEIR(b,s,g)

            SSE = np.sum((I_model - I)**2)

            if SSE < best_SSE:

                best_SSE = SSE
                best_beta = b
                best_sigma = s
                best_gamma = g


print("Best beta =", best_beta)
print("Best sigma =", best_sigma)
print("Best gamma =", best_gamma)
print("Lowest SSE =", best_SSE)


# Plot best SEIR fit
S,E,I_model,R = euler_SEIR(best_beta,best_sigma,best_gamma)

plt.figure()
plt.scatter(t, I, label="Observed Data")
plt.plot(t, I_model, label="Best SEIR Model")
plt.xlabel("Day")
plt.ylabel("Active Infections")
plt.legend()
plt.show()


# Compute R0 from SEIR parameters
R0_seir = best_beta / best_gamma
print("SEIR Estimated R0 =", R0_seir)
# Used ChatGPT 5.2 to help learn more about the line of best fit coding 
# OpenAI. (2026). ChatGPT (GPT-5.2 Thinking) [Large language model]. https://chat.openai.com