# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['calculadora_do_cidadao', 'calculadora_do_cidadao.adapters']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.22.0', 'typer>=0.0.8']

extras_require = \
{'docs': ['pip>=20.0.0',
          'readthedocs-sphinx-ext>=2.1.3',
          'sphinx>=3.4.3',
          'sphinx-rtd-theme>=0.5.1']}

setup_kwargs = {
    'name': 'calculadora-do-cidadao',
    'version': '0.5.1',
    'description': 'Tool for Brazilian Reais monetary adjustment/correction',
    'long_description': '# Calculadora do Cidadão\n\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/cuducos/calculadora-do-cidadao/Tests)](https://github.com/cuducos/calculadora-do-cidadao/actions)\n[![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability-percentage/cuducos/calculadora-do-cidadao)](https://codeclimate.com/github/cuducos/calculadora-do-cidadao/maintainability)\n[![Code Climate coverage](https://img.shields.io/codeclimate/coverage/cuducos/calculadora-do-cidadao)](https://codeclimate.com/github/cuducos/calculadora-do-cidadao/test_coverage)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/calculadora-do-cidadao)](https://pypi.org/project/calculadora-do-cidadao/)\n[![PyPI](https://img.shields.io/pypi/v/calculadora-do-cidadao)](https://pypi.org/project/calculadora-do-cidadao/)\n[![](https://img.shields.io/readthedocs/calculadora-do-cidadao)](https://calculadora-do-cidadao.readthedocs.io/)\n\nPacote em Python para correção de valores. Confira a [documentação](https://calculadora-do-cidadao.readthedocs.io/) para mais detalhes!\n\n## Exemplo de uso\n\n```python\nIn [1]: from datetime import date\n   ...: from decimal import Decimal\n   ...: from calculadora_do_cidadao import Ipca\n\nIn [2]: ipca = Ipca()\n\nIn [3]: ipca.adjust(date(2018, 7, 6))\nOut[3]: Decimal(\'1.051202206630561280035407253\')\n\nIn [4]: ipca.adjust("2014-07-08", 7)\nOut[4]: Decimal(\'9.407523138792336916983267321\')\n\nIn [5]: ipca.adjust("12/07/1998", 3, "01/07/2006")\nOut[5]: Decimal(\'5.279855889296777979447848574\')\n```\n\n[![asciicast](https://asciinema.org/a/295920.svg)](https://asciinema.org/a/295920)\n\n## Mini-guia de contribuição\n\nO pacote utiliza o padrão `pyproject.toml` e o [Poetry](https://python-poetry.org/). Para instalar as dependências:\n\n```console\n$ poetry install --extras "docs"\n```\n\n### Testes\n\nPara rodar os testes apenas com a versão atual do Python:\n\n```console\n$ poetry run pytest\n```\n\nPara rodar com todas as versões de Python:\n\n```console\n$ poetry run tox\n```\n\n#### Escrevendo testes de novos adaptadores\n\nQuando criar m novo adaptador, escreva ao menos três casos de teste para o método `adjust`:\n\n1. Utilizando apenas um argumento (data original)\n1. Utilizando dois argumentos (data original mais valor personalizado)\n1. Utilizando três argumentos (data original, valor personalizado e data final)\n\n### Documentação\n\nPara a documentação, é preciso utilizar o [Sphinx](https://www.sphinx-doc.org/en/):\n\n```console\n$ poetry run sphinx-build docs docs/_build\n```\n\nDepois, é só acessar `docs/_build/index.html`.\n\n### Limpeza de arquivos gerados automaticamente\n\nPara limpar os arquivos gerados automaticamente, existe o atalho `make clean`.\n',
    'author': 'Eduardo Cuducos',
    'author_email': 'cuducos@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://calculadora-do-cidadao.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
