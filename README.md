# Generate network data for the purpose of experimenting
Sometimes you need to have a bunch of connection information to experiment with, but it just isn't there.
This tiny project aims to do exactly that.

# Running the tool
For now the tool only supports the ```plain``` mode of which you can see an example in the 'Example output' section of this readme.

## Plain mode
You can determine if it should generate only connections within the VLAN, between VLANs or all of them:

```python generator_cli.py --mode inner plain```


# Example output
The following is example output

## plain mode
```
{'srchost': '219.64.120.76', 'dsthost': '68.206.89.177', 'srcport': 64878, 'dstport': 3389}
{'srchost': '219.64.120.13', 'dsthost': '68.206.89.162', 'srcport': 63219, 'dstport': 3389}
{'srchost': '92.9.15.58', 'dsthost': '118.220.234.59', 'srcport': 49842, 'dstport': 3389}
{'srchost': '92.9.15.62', 'dsthost': '118.220.234.216', 'srcport': 57969, 'dstport': 445}
{'srchost': '92.9.15.13', 'dsthost': '118.220.234.130', 'srcport': 51065, 'dstport': 3389}
{'srchost': '92.9.15.83', 'dsthost': '118.220.234.131', 'srcport': 55201, 'dstport': 445}
{'srchost': '92.9.15.107', 'dsthost': '118.220.234.217', 'srcport': 60131, 'dstport': 445}
{'srchost': '92.9.15.246', 'dsthost': '118.220.234.36', 'srcport': 57648, 'dstport': 3389}
{'srchost': '92.9.15.67', 'dsthost': '118.220.234.24', 'srcport': 64662, 'dstport': 445}
```
# Convert to yED image
The output from this tool can be used as input for other tools. The following one liner will generate a CSV format that you can then import to Excel and then import into yED

```python generator_cli.py plain | jq -r '[.srchost,.dsthost,.dstport] | join(",")' > geninput.csv```

# PyTest
You can run the tests like this:

```python -m pytest tests/```

# MyPy
You check type annotations & hints with:

```mypy generator_cli.py lib_networkdatagenerator/```