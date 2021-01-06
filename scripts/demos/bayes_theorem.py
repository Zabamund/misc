import sys

import numpy as np

def bayes_theorem(P_B_A, P_A, P_B_nA):
    """An implementation of Bayes theorem.
    Evaluate the probability of event $A$ given that $B$ is true.

    Parameters
    ----------
    P_B_A : array_like
        the likelihood of event $B$ occurring given that $A$ is true.
    P_A : array_like
        the likelihood of observing $A$.
    P_B_nA : array_like
        the likelihood of observing $B$ given $A$ is false.

    Returns
    -------
    P_A_B : float
        probability of event $A$ given that $B$ is true.
    
    Notes
    -----
    From wikipedia:
    [Bayes Theorem](https://en.wikipedia.org/wiki/Bayes%27_theorem)
    is described as in (1.):

    1. $$P(A|B) = \frac{P(B|A)P(A)}{P(B)} $$

    Where `A` and `B` are [events](https://en.wikipedia.org/wiki/Event_(probability_theory)) 
    and $P(B) \\neq 0$.

    - $P(A|B)$ is a [conditional probability](https://en.wikipedia.org/wiki/Conditional_probability):
      the likelihood of event $A$ occurring _given that_ $B$ is true.
    - $P(B|A)$ is also a conditional probability: the likelihood of event $B$ occurring
      given that $A$ is true.
    - $P(A)$ and $P(B)$ are the probabilities of observing $A$ and $B$ respectively;
      they are known as the [marginal probability](https://en.wikipedia.org/wiki/Marginal_distribution).
    - $A$ and $B$ must be different events.

    However it strikes me as obfuscating to only show the denominator as $P(B)$ as it must 
    be developed in order to actually evaluate this equation, as follows in (2.):

    2. $$ P(B) = P(B|A)P(A) + P(B|¬A)P(¬A) $$

    Where:
    - $P(B|¬A)$ is a conditional probability; 
        the likelihood of event $B$ occurring given that $A$ is false.
    - $P(¬A)$ is the probablity of not observing $A$.

    So we need a minimum of 3 numeric inputs to run this calculation:

    1. $P(B|A)$ the likelihood
    2. $P(A)$ the normalizing constant
    3. $P(B|¬A)$

    Example
    -------
    Retrieving a Special Publication of the GeolSoc (SPGS) from my bookshelf:
    Getting a SPGS book is the test (A);
    I have 11 SPGS books on my bookshelf and a total of 44 books on that shelf
    so:
    
    P(A) = 11 / 44 = 0.25
    P(B|A) = 1 - P(A) = 0.75
    P(B|¬A) = 1

    >>> python bayes_theorem.py 0.75 0.25 1
    P(A|B) = 0.200

    """
    P_B_A, P_A, P_B_nA = np.array(P_B_A), np.array(P_A), np.array(P_B_nA)
    return (P_B_A * P_A) / ((P_B_A * P_A) + P_B_nA * (1 - P_A))

if __name__ == "__main__":
    try:
        P_B_A_str, P_A_str, P_B_nA_str = sys.argv[1:]
        P_B_A, P_A, P_B_nA = float(P_B_A_str), float(P_A_str), float(P_B_nA_str)
        print(f'P(A|B) = {bayes_theorem(P_B_A, P_A, P_B_nA):.3f}')
    except ValueError:
        num_vals = int((len(sys.argv) - 1) / 3)
        vals = [float(val.strip('[],')) for val in sys.argv[1:]]
        P_B_A = vals[:num_vals]
        P_A = vals[num_vals:-num_vals]
        P_B_nA = vals[-num_vals:]
        print(f'P(A|B) = {bayes_theorem(P_B_A, P_A, P_B_nA)}')