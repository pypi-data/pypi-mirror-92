# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dapodik_webservice',
 'dapodik_webservice.console',
 'dapodik_webservice.models',
 'dapodik_webservice.models.ptk',
 'dapodik_webservice.models.rombongan_belajar',
 'dapodik_webservice.template']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0', 'requests>=2.25.1,<3.0.0']

extras_require = \
{'excel': ['openpyxl>=3.0.5,<4.0.0', 'click>=7.1.2,<8.0.0']}

entry_points = \
{'console_scripts': ['dapodik = dapodik_webservice.__main__:main']}

setup_kwargs = {
    'name': 'dapodik-webservice',
    'version': '3.1.0',
    'description': 'SDK Python Web Service aplikasi Dapodik',
    'long_description': '# dapodik-webservice\n\n[![PyPi Package Version](https://img.shields.io/pypi/v/dapodik-webservice)](https://pypi.org/project/dapodik-webservice/)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/dapodik-webservice)](https://pypi.org/project/dapodik-webservice/)\n[![Tests](https://github.com/dapodix/dapodik-webservice/workflows/Tests/badge.svg)](https://github.com/dapodix/dapodik-webservice/actions)\n[![codecov](https://codecov.io/gh/dapodix/dapodik-webservice/branch/main/graph/badge.svg?token=2rX7lP6K0C)](https://codecov.io/gh/dapodix/dapodik-webservice)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Mypy](https://img.shields.io/badge/Mypy-enabled-brightgreen)](https://github.com/python/mypy)\n\nSDK Python Web Service aplikasi Dapodik\n_Jangan lupa untuk [donasi](#donasi)_\n\n## Penggunaan\n\n### Aplikasi CLI\n\n1. Download `dapodik-export` dari [halaman rilis](https://github.com/dapodix/dapodik-webservice/releases) file `dapodik-export.zip`.\n2. _Matikan antivirus atau buat pengecualian folder yang sudah diekstrak._\n3. Exstrak `dapodik-export.zip` _(klik kanan Extract Here)_ dan masuk folder dapodik-export.\n4. Buka / open `cmd / windows powershell` di folder tersebut dengan tahan shift + klik kanan di dalam folder _(jangan klik kanan file apapun)_.\n\n#### Contoh penggunaan Aplikasi CLI\n\nBerikut contoh perintah yang bisa dijalankan melalui `cmd / windows powershell`\n\n_Rubah `token saya` menjadi token webservice dari aplikasi DAPODIK bagian pengaturan!_\n\nMengeksport semua data ke dalam file bernama `Sekolahku`\n\n```cmd\ndapodik-export.exe export semua --token "token saya" --npsn "0123456789" "Sekolahku"\n```\n\nMengeksport data peserta didik ke dalam file bernama `Peserta didik`\n\n```cmd\ndapodik-export.exe export peserta-didik --token "token saya" --npsn "0123456789" "Peserta didik"\n```\n\n### Dengan Python\n\nUntuk menggunakan modul ini silahkan buat token Web Service Dapodik terlebih dahulu di pengaturan Dapodik.\n\n```python\nfrom dapodik_webservice import DapodikWebservice\n\ntoken = \'token webservice\'\nnpsn = \'12345678\'\n\ndw = DapodikWebservice(token, npsn)\n\nsekolah = dw.sekolah\n\nprint(sekolah.nama)\n\n```\n\n## Install Dari PIP\n\n_Khusus untuk pengembang python_! Pastikan python 3.6 terinstall, kemudian jalankan perintah di bawah dalam Command Prompt atau Powershell (di Windows + X / klik kanan icon Windows):\n\n```bash\npip install --upgrade dapodik-webservice\n```\n\n## Donasi\n\nJika anda ingin melakukan donasi untuk kami, bisa menghubungi kami melalui [WhatsApp](https://wa.me/6287725780404) ataupun [Telegram](https://t.me/hexatester).\n\n## Legal / Hukum\n\nKode ini sama sekali tidak berafiliasi dengan, diizinkan, dipelihara, disponsori atau didukung oleh Kemdikbud atau afiliasi atau anak organisasinya. Ini adalah perangkat lunak yang independen dan tidak resmi. Gunakan dengan risiko Anda sendiri.\n',
    'author': 'hexatester',
    'author_email': 'habibrohman@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://dapodix.github.io/dapodik-webservice/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
