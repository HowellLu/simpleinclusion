# simplyincluded
An easy way to apply a simple inclusion criteria to a Pandas Dataframe to maximize an objective function.

This is a simple method that generates a ruleset that subsets a Pandas DataFrame with the express intent to maximize an objective value.

You can simply use it by: 

``` pip install simplyincluded  ```

and use it with 

``` from simplyincluded import generatesplit  ```

If we were to create a pandas dataframe like this called test: 

| var1 | var2 | var3 | Points |
|------|------|------|--------|
| 5    | 1    | 1    | 7      |
| 4    | 3    | 2    | -1     |
| 2    | 1    | 3    | -2     |
| 8    | 0    | 4    | -3     |
| 9    | 1    | 5    | 19     |
| 9    | 1    | 6    | -3     |
| 9    | 2    | 7    | 7      |

and we were to run the function generatesplit():

``` FirstOutput = generatesplit(test,400,10) ```

We would be able to output the selected, the remainder and the ruleset

``` FirstOutput.selected ```

| var1 | var2 | var3 |  Points |
|------|------|------|---------|
| 5    | 1    | 1    | 7       |
| 9    | 1    | 5    | 19      |
| 9    | 1    | 6    | -3      |
| 9    | 2    | 7    | 7       |

``` FirstOutput.remainder ```

| var1 | var2 | var3 | Points |
|------|------|------|---------|
| 4    | 3    | 2    | -1      |
| 2    | 1    | 3    | -2      |
| 8    | 0    | 4    | -3      |

``` FirstOutput.ruleset ```


| Variables | Directionality | Cutoffs    |
|-----------|-----------------|------------|
| var1      | >               | 4.688091   |
| var2      | >               | 0.165679   |
| var3      | >               | -2.806131  |


It’s a simple method called: generatesplit(PDDataframe, BatchSize, Epochs, ExponentalDecayFactor)

This generates a class which contains three properties:

.Selected (The Pandas Dataframe within the subset in the ruleset)

.Remainder (What was excluded from the Dataframe)

.Ruleset (The ruleset)

# Prerequisites

There are a few preconditions:

1.)	PDDataframe must be a pandas dataframe with all numeric values. (Can’t have anything missing)

2.)	The Last Column of PDDataframe should be the objective variable. 

3.)	The Objective Variable should be coded in a parsable manner (Positive numbers mean that the row should be kept, and negatives mean that it should not, with the size of the number meaning magnitude) 

#Methodology

Essentially, this algorithm works through a simple method; 

1.)	It throws randomly generated particles (Initially uniformly distributed) at the sample set. These points are going to have the same dimensionality as the # of predictor variables. Then the program splits the sample space into 2^(Amount of Predictor Variables). For example; if you had a square and had a random point in there there would be 4 splits ((Up, Left),(Up, Right),(Down, left), (Down, right)). This is **batch size** or the number of particles

2.)	It would then calculate the sum of the values for each split and store the highest one. This would then be done for all the particles. The highest one from this epoch will be remembered.

At the end of every epoch, there's an alternation between a large search function which essentially takes a bird’s eye view of the sample space, where the random particles are spread widely across the sample space, which prevents the function from being stuck at a local maxima. There’s also there's an exponentially decaying scope that will look at a smaller and smaller subsection, like gradient descent so that we would start taking incrementally smaller steps the longer that this function has been running. **(That’s the exponential decay function)**

3.)	Then, it would do these two past steps, a predetermined number of epochs. This is the **number of epochs** If a higher maximum value for a split is calculated in any epoch, then it will replace the previously highest point and the grid stored in memory. There are a couple more features baked in. After completing a preallotted number of epochs, we generate a split of the original dataset with the highest scoring point and the highest scoring set of partition directions, to get the portion that was accepted and the portion that was rejected.
This culminates in generating the optimal space alongside the ruleset that generated the space and the remainder space.

# Limitations

Some limitations should be noted, this works better with generally monotonic variables and it works better with homoscedastic functions. 


One problem that might occur with this formulation is the possibility that we run out of "good samples" in what remains in the sample space, as each remainder will have fewer and fewer "good samples" and therefore need to take in samples that are not so optimal just to hit our quota. The way that I coded to deal with this was to shift the distribution of the output variable by n standard deviations until we hit our quota. So you may need to consistently shift your objective variable if you need a larger or smaller sample/
 
I think  this question could be solved with some implementation with a genetic algorithm and some sort of particle swarm optimization, but I couldn’t find an easy plug-and-play library to use. Almost all of these libraries require a great deal of programming knowledge and are a bit too complicated for the layperson and didn't apply to this situation. So I decided to make my library.

# Version Control

Anyways, I’ve tested this from Python 3.6.1 to 3.12.2 and with Pandas 1.0.0 to 2.2.1. Enjoy!



