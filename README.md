# LazyIter
Implementation of the ICML paper "LazyIter: A Fast Algorithm for Counting Markov Equivalent DAGs and Designing Experiments". You can find the paper [here](https://proceedings.mlr.press/v119/ahmaditeshnizi20a.html) and the PyPi package [here](https://pypi.org/project/LazyIter-teshnizi/#history).

## Installation

1. **using PyPi**

  LazyIter could be simply installed using pip:
  ```bash
  pip install LazyIter-teshnizi
  ```

2. **using the codes directly**
  
  You can also copy files inside **LazyIter** folder to your project's folder and import the functions into your code. 


## Usage

<p align="center">
  <a><img width="30%" src="https://github.com/teshnizi/LazyIter/raw/master/example_graph.png" title="Example" alt="Example Graph"></a>
</p>


  - **LazyCount**
  
  Import **lazy_count** function from **LazyIter.count** and pass it the adjacency set of the corresponding MEC to get the MEC size:
  
  ```python
  from LazyIter.count import lazy_count
  
  neighbors = {
        0: {1, 3, 6},
        1: {0, 3},
        2: {4, 5},
        3: {0, 1, 5, 6},
        4: {2, 5, 6},
        5: {2, 3, 4, 6},
        6: {0, 3, 4, 5}
        }


  print(lazy_count(neighbors))
  ```
  output:
  ```python
  22
  ```
  - **Passive Learning**
  
  You can find the number of directed edges in the worst case for a given set of experiment targets using **pl_score** function. To find the best target, you could simply iterate over all valid target sets (based on the experiment budget) and choose the one with maximum score.
  
  ```python
  from LazyIter.learn import pl_score
  
  neighbors = {
        0: {1, 3, 6},
        1: {0, 3},
        2: {4, 5},
        3: {0, 1, 5, 6},
        4: {2, 5, 6},
        5: {2, 3, 4, 6},
        6: {0, 3, 4, 5}
        }
  
  print(pl_score(neighbors, {0, 4}))
  ```
  output:
  ```python
  8
  ```
  Explanation: If you intervene on nodes 0 and 4 simultaneously in different trials, you will discover direction of at least 8 edges.
  
  - **Active Learning**
  Active learning is a sub-problem of the Passive learning case where the target set contains only 1 node. Therefore, You can use **pl_score** for this purpose too.


## Contribution
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Future work maybe focused at adding support for other objective functions.


## License
[MIT](https://choosealicense.com/licenses/mit/)
