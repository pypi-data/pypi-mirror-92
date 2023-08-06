# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ridgeplot']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.5,<2.0.0', 'plotly>=4.14.3,<5.0.0', 'statsmodels>=0.12.1,<0.13.0']

setup_kwargs = {
    'name': 'ridgeplot',
    'version': '0.1.6',
    'description': '',
    'long_description': '![ridgeplot - beautiful ridgeline plots in Python](assets/hero.png)\n\n---\n\n# ridgeplot: beautiful ridgeline plots in Python\n\n\nThe `ridgeplot` python library aims at providing a simple API for plotting beautiful\n[ridgeline plots](https://www.data-to-viz.com/graph/ridgeline.html) within the\nextensive [Plotly](https://plotly.com/python/) interactive graphing environment.\n\nBumper stickers:\n- Do one thing, and do it well!\n- Use sensible defaults, but allow for extensive configuration!\n\n\n## How to get it?\nThe source code is currently hosted on GitHub at: https://github.com/tpvasconcelos/ridgeplot\n\nInstall and update using [pip](https://pip.pypa.io/en/stable/quickstart/):\n```shell\npip install -U ridgeplot\n```\n\n### Dependencies\n- [plotly](https://plotly.com/) - the interactive graphing backend that powers `ridgeplot`\n- [statsmodels](https://www.statsmodels.org/) - Used for Kernel Density Estimation (KDE)\n- [numpy](https://numpy.org/) - Supporting library for multi-dimensional array manipulations\n\n\n## How to use it?\n\n### Sensible defaults\n```python\nfrom numpy.random import normal\nfrom ridgeplot import ridgeplot\n\nsynthetic_samples = [normal(n / 1.2, size=600) for n in reversed(range(9))]\nfig = ridgeplot(samples=synthetic_samples)\nfig.show()\n```\n![ridgeline plot example using the ridgeplot Python library](assets/example_simple.png)\n\n\n### Fully configurable\nIn this example, we will be replicating the first ridgeline plot example in\n[this _from Data to Viz_ post](https://www.data-to-viz.com/graph/ridgeline.html),\nwhich uses the _probly_ dataset. You can find the _plobly_ dataset on multiple sources like in the\n[bokeh](https://raw.githubusercontent.com/bokeh/bokeh/main/bokeh/sampledata/_data/probly.csv)\npython interactive visualization library. I\'ll be using the\n[same source](https://raw.githubusercontent.com/zonination/perceptions/master/probly.csv)\nused in the original post.\n```python\nimport numpy as np\nimport pandas as pd\nfrom ridgeplot import ridgeplot\n\n\n# Get the raw data\ndf = pd.read_csv("https://raw.githubusercontent.com/bokeh/bokeh/main/bokeh/sampledata/_data/probly.csv")\n\n\n# Let\'s grab only the subset of columns displayed in the example\ncolumn_names = [\n    "Almost Certainly", "Very Good Chance", "We Believe", "Likely",\n    "About Even", "Little Chance", "Chances Are Slight", "Almost No Chance",\n]\ndf = df[column_names]\n\n\n# Not only does \'ridgeplot(...)\' come configured with sensible defaults\n# but is also fully configurable to your own style and preference!\nfig = ridgeplot(\n    samples=df.values.T,\n    bandwidth=4,\n    kde_points=np.linspace(-12.5, 112.5, 400),\n    colorscale="viridis",\n    colormode="index",\n    coloralpha=0.6,\n    labels=column_names,\n    spacing=5 / 9,\n)\n\n# Again, update the figure layout to your liking here\nfig.update_layout(\n    title="What probability would you assign to the phrase <i>“Highly likely”</i>?",\n    height=650,\n    width=800,\n    plot_bgcolor="rgba(255, 255, 255, 0.0)",\n    xaxis_gridcolor="rgba(0, 0, 0, 0.1)",\n    yaxis_gridcolor="rgba(0, 0, 0, 0.1)",\n    yaxis_title="Assigned Probability (%)",\n)\nfig.show()\n```\n![ridgeline plot of the probly dataset using the ridgeplot Python library](assets/example_probly.png)\n\n\n## Alternatives\n\n- [`plotly` - from examples/galery](https://plotly.com/python/violin/#ridgeline-plot)\n- [`seaborn` - from examples/galery](https://seaborn.pydata.org/examples/kde_ridgeplot)\n- [`bokeh` - from examples/galery](https://docs.bokeh.org/en/latest/docs/gallery/ridgeplot.html)\n- [`matplotlib` - from blogpost](https://matplotlib.org/matplotblog/posts/create-ridgeplots-in-matplotlib/)\n- [`joypy` - Ridgeplot library using a `matplotlib` backend](https://github.com/sbebo/joypy)\n\n',
    'author': 'Tomas Pereira de Vasconcelos',
    'author_email': 'tomasvasconcelos1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tpvasconcelos/ridgeplot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
