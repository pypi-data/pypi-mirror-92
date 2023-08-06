# aelbatal_distributions

aelbatal_distributions is a Python library built by Adham El-Batal in 2021 as an entry to the Udacity Machine Learning Engineer course.
This library allows for calculcations and plots, based on Gaussian and binomial distribution. The library allows you to calculcate
the means and standard deviations of a given distribution, and plot histograms of the distribution.

## installation

To install, please use pip.

```
pip install aelbatal_distributions
```

## usage

Instantiate Python in command line, and create a distribution with the correct parameters.
```
>>> import aelbatal_distributions
>>> from aelbatal_distributions import Gaussian, Binomial
>>> gaussian1 = Gaussian(mu = 2.0, sigma = 0.5)
>>> print(gaussian1.mean)
2.0
>>> binomial1 = Binomial(prob = 0.2, size = 100)
>>> binomial1.plot_bar()
```

## contributing

Please do not contribute to this document. It is a class assignment and is intended only for that purpose.