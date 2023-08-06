# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['random_names', 'random_names.etl', 'random_names.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'random-names',
    'version': '0.1.0',
    'description': 'Convert int to random name, like tree_dance and convert it back to same int.',
    'long_description': '# random_names\nConvert int to random name, like tree_dance and convert it back to same int.\n\nLike [git-name](https://pypi.org/project/git-name/) which converts hashes to memorable names and back.\n\nAlso like the [Mnemonic Major System](https://en.wikipedia.org/wiki/Mnemonic_major_system) which converts\nstrings of numbers it phrases to aid in memorization, implemented here [mnemonic-major-encoder](https://pypi.org/project/mnemonic-major-encoder/)\nIn action here: https://major-system.info/en/\n\nUsage\n-----\n```\nfrom random_names.make_names import number_to_name,number_from_name\n\n# TODO: needs a user specified separator\nname = number_to_name(100,"prefix","q")\nprint(name) # prefix_q_activated\n\nnumber = number_from_name(name)\nassert number==100\n```\n\n# Why\nLets say that your users need to type in a long number, 48342342. It would be easier to\ntype in tree_dance. But your app still needs that number, so you need to convert it\nback. This is similar to [docker container names](https://github.com/moby/moby/blob/master/pkg/namesgenerator/names-generator.go), except reversable.\n\n# How\nI map 10,000 words to 4 digits, twice. That yields two words\ncovering 100,000,000 numbers.\n\nIf you use a short word list, you can\'t generate enough names.\n\nIf you use any dictionary, you get a lot of funny, obscene or offensive names. So\nI ran the world list through cuss word detection & removed most of the worst.\n\nDocs\n----\n- [To do](TODO.md)\n\n\nRelated Pypi Packages\n--\nCrypocurrency related\n- [mnemonic](https://pypi.org/project/mnemonic/) Words to cryptocurrency "wallet"\n\nMneumonic Major System\n- [major_system](https://pypi.org/project/major_system/)\n- [mnemonic-major-encoder](https://pypi.org/project/mnemonic-major-encoder/)\n\nConverting arabic numbers, e.g. 22, to spoken equivalent, e.g. twenty-two and back.\n- [inflect](https://pypi.org/project/inflect/) Converts, 22 to twenty-two\n- [words2num](https://pypi.org/project/words2num/) Converts twenty-two to 22.\n- [num2words](https://pypi.org/project/num2words/) Converts 22 to twenty-two\n- [text2num](https://pypi.org/project/text2num/) Converts twenty-two to 22. Multilingual\n- [num2rus](https://pypi.org/project/num2rus/) Converts 22 to Russian currency\n- [num2fawords](https://pypi.org/project/num2fawords/) Convert number to Persian\n- [zahlwort2num](https://pypi.org/project/zahlwort2num/) Convert german to 22.\n\nConverting numbers to a shorter string, like [Ascii85](https://en.wikipedia.org/wiki/Ascii85)\n- [num-shorty](https://pypi.org/project/num-shorty/)\n- [ascii85](https://github.com/euske/pdfminer/blob/master/pdfminer/ascii85.py)\n\nRandom names, just random names. No way to convert to a number\n- [pypi search](https://pypi.org/search/?q=random+name) To many to list, mostly just a function or two.\n',
    'author': 'Matthew Martin',
    'author_email': 'matthewdeanmartin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/matthewdeanmartin/random_names',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
