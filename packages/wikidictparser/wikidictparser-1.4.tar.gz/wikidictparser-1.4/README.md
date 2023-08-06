# Wiktionary Parser Package

![Python package](https://github.com/ls2716/wikidictparser_package/workflows/Python%20package/badge.svg?branch=master)


Python package to scrape Polish Wikitionary to parse meaning of every word and its declination/conjugation where appriopriate.

The package uses bs4, requests and pandas.

### To install - requires pip

```
pip install wikidictparser
```

### Example usage:

```python
# Import wikitionary.
import wikidictparser as wdp

# Create polish parser object.
parser = wdp.get_parser('pl')

# Fetch a word.
result = parser.fetch('onomatopeja')

# Print the result.
print('Result:\n', result)
```

The parser.fetch() function will return a dictionary with two keys: 'znaczenia' (meanings) and 'odmiana' (declination).
Each of them will contain smaller dictionary with Wiktionary styled division i.e.

```python
{
    "znaczenia": {
        1: {
            1: {
                "part_of_speach": ...,
                "meaning" ...
            }
            2: {
                ...
            }
            ...
        }
        2: {
            ...
        }
        ...
    }
    "odmiana": {
        1: {
            1: {
                pandas.DataFrame # or nieodm (nondeclinable)
            }
            2: {
                ...
            }
            ...
        }
        2: {
            ...
        }
        ...
    }
}
```