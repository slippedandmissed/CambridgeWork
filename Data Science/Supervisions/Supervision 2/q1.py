import numpy as np

def sigma(x):
    mu_mle = np.mean(mu)
    sigma_mle = np.sqrt(mu_mle * mu_mle - np.mean(x*x)) * 0.5
    return sigma_mle


def parametric_sample(x):
    n = x.size[0]
    mu_mle = np.mean(mu)
    sigma_mle = sigma(x)
    new_x = np.random.normal(mu_mle, sigma_mle, size=(n, 100000))
    new_sigma = sigma(new_x)
    plt.hist(new_sigma) # Mark off confidence interval from this histogram
