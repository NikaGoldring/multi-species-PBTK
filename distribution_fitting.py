import warnings
import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels as sm
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['figure.figsize'] = (8.0, 6.0)
matplotlib.style.use('ggplot')

# Create models from data
def best_fit_distribution(data, bins=200, ax=None):
    """Model data by finding best fit distribution to data"""
    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, density=True)    #y = frequency  ## density=True : If ``True``, the result is the value of the probability *density* function at the bin, normalized such that the *integral* over the range is 1. Note that the sum of the histogram values will not be equal to 1 unless bins of unity width are chosen; it is not a probability *mass* function.
    x = (x + np.roll(x, -1))[:-1] / 2.0                   #x = bin edges  ## cuts away 1st and last edge

    # Distributions to check
    DISTRIBUTIONS = [st.norm, st.gamma,  st.uniform] #

    # Best holders
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf

    # Estimate distribution parameters from data
    for distribution in DISTRIBUTIONS:

        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')

                # fit dist to data
                params = distribution.fit(data)

                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]

                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))

                # if axis pass in add to plot
                try:
                    if ax:
                        pd.Series(pdf, x).plot(ax=ax, label=distribution.name, legend=True)
                    end
                except Exception:
                    pass

                # identify if this distribution is better
                if best_sse > sse > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse

        except Exception:
            pass

    return (best_distribution.name, best_params, best_sse)

def make_pdf(dist, params, size=10000):
    """Generate distributions's Probability Distribution Function """

    # Separate parts of parameters
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]

    # Get sane start and end points of distribution
    start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
    end = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)

    # Build PDF and turn into pandas Series
    x = np.linspace(start, end, size)
    y = dist.pdf(x, loc=loc, scale=scale, *arg)
    #print (y)
    pdf = pd.Series(y, x)

    return pdf

def make_cdf(dist, params, size=10000):
    """Generate distributions's Cummulative Distribution Function """
    
    # Separate parts of parameters
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]

    # Get sane start and end points of distribution
    start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
    end = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)

    # Build CDF and turn into pandas Series
    x = np.linspace(start, end, size)
    y = dist.cdf(x, loc=loc, scale=scale, *arg)
    #print(y)
    cdf = pd.Series(y, x)
  
    
    return cdf



def distribution_plot(dataset, unit, data, bins):

    
    #bins = round(len(data)/10)
    bins = bins   

    # Plot for comparison
    plt.figure(figsize=(6,4))                        
    ax = data.plot(kind='hist', bins=bins, density=True, alpha=0.5, color=list(matplotlib.rcParams['axes.prop_cycle'])[1]['color'], label='Data', legend=True)
    # Save plot limits
    dataYLim = ax.get_ylim()
    

    # Find best fit distribution
    best_fit_name, best_fit_params, best_sse = best_fit_distribution(data, 200, ax) 
    best_dist = getattr(st, best_fit_name)
    

    # Update plots
    ax.set_ylim(dataYLim)
    ax.set_title(u''+dataset+'\n All fitted distributions')
    ax.set_xlabel(u''+unit)
    ax.set_ylabel('Frequency')
    ax.set_facecolor('white')
    ax.grid(False) #color='grey', linestyle='-', linewidth=0.25, alpha=0.5)

    # Make PDF with best params 
    pdf = make_pdf(best_dist, best_fit_params)
    cdf = make_cdf(best_dist, best_fit_params)

    # Display
    plt.figure(figsize=(6,4))
    ax0 = cdf.plot(lw=2, label='CDF', legend=True)
    ax = pdf.plot(lw=2, label='PDF', legend=True)
    ax.set_facecolor('white')
    ax.grid(False) #color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    data.plot(kind='hist', bins=bins, density=True, alpha=0.5, label='Data', legend=True, ax=ax)

    param_names = (best_dist.shapes + ', loc, scale').split(', ') if best_dist.shapes else ['loc', 'scale']
    param_str = ', '.join(['{}={:0.5f}'.format(k,v) for k,v in zip(param_names, best_fit_params)])   
    sse_str= 'SSE='+ str(round(best_sse, 2))                  ## SSE roundet to two digits
    dist_str = '{}({}, {})'.format(best_fit_name, param_str, sse_str)

    ax.set_title(u''+dataset+' with best fit distribution \n' + dist_str)
    ax.set_xlabel(u''+unit)
    ax.set_ylabel('Frequency')