import matplotlib.pyplot as plt

def estimate_parameters(t, S, I, R, D, alpha, beta, gamma, mu, N):
    if t == 0:
        return beta[0], gamma[0], alpha[0], mu[0]
    if t >= len(I) or t >= len(S) or t >= len(R) or t >= len(D):
        return beta[-1], gamma[-1], alpha[-1], mu[-1] 
    beta_new = (I[t] - I[t-1] + mu[-1] * I[t-1] + gamma[-1] * I[t-1]) * N / (S[t-1] * I[t-1]) if S[t-1]*I[t-1] > 0 else beta[-1] 
    gamma_new = R[t] / I[t-1] if I[t-1] > 0 else gamma[-1]
    alpha_new = S[t] / R[t-1] if R[t-1] > 0 else alpha[-1]
    mu_new = D[t] / I[t-1] if I[t-1] > 0 else mu[-1]
    return beta_new, gamma_new, alpha_new, mu_new


def update_SIR_model(S, I, R, D, alpha, beta, gamma, mu, N):
    S_new = S[-1] + (alpha*R[-1] - beta*S[-1]*I[-1]/N)
    I_new = I[-1] + (beta*S[-1] * I[-1]/N - mu*I[-1] - gamma*I[-1])
    R_new = R[-1] + (gamma*I[-1] - alpha*R[-1])
    D_new = D[-1] + (mu*I[-1])
    return S_new, I_new, R_new, D_new


def plot_SIR(updated_df, R0, days):
    plt.figure(figsize=(10,6))
    plt.plot(updated_df['Day'], updated_df['Susceptible'], label='Susceptible', color= 'blue')
    plt.plot(updated_df['Day'], updated_df['Infected'], label='Infected', color='red')
    plt.plot(updated_df['Day'], updated_df['Recovered'], label='Recovered', color='green')
    plt.plot(updated_df['Day'], updated_df['Died'], label='Died', color='black')
    plt.xlabel("Days")
    plt.ylabel("Population")
    plt.title("SIR Model")
    plt.legend()
    plt.show() 
    
    #plot of R0
    plt.figure(figsize=(10, 6))
    plt.plot(updated_df['Day'][1:], R0[:days-1], label='R0 (Basic Reproduction Number)', color='purple')
    plt.xlabel("Days")
    plt.ylabel("R0 Value")
    plt.title("Basic Reproduction Number Over Time")
    plt.legend()
    plt.show()



