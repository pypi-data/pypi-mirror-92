# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opennem',
 'opennem.api',
 'opennem.api.admin',
 'opennem.api.export',
 'opennem.api.facility',
 'opennem.api.geo',
 'opennem.api.photo',
 'opennem.api.revision',
 'opennem.api.station',
 'opennem.api.stats',
 'opennem.api.tasks',
 'opennem.api.weather',
 'opennem.client',
 'opennem.core',
 'opennem.core.facility',
 'opennem.core.parsers',
 'opennem.core.stations',
 'opennem.core.stats',
 'opennem.core.unit',
 'opennem.db',
 'opennem.db.migrations',
 'opennem.db.migrations.versions',
 'opennem.db.models',
 'opennem.diff',
 'opennem.exporter',
 'opennem.geo',
 'opennem.importer',
 'opennem.middlewares',
 'opennem.monitors',
 'opennem.notifications',
 'opennem.pipelines',
 'opennem.pipelines.aemo',
 'opennem.pipelines.aemo.mms',
 'opennem.pipelines.apvi',
 'opennem.pipelines.nem',
 'opennem.pipelines.npi',
 'opennem.pipelines.wem',
 'opennem.scheduler',
 'opennem.schema',
 'opennem.schema.aemo',
 'opennem.settings',
 'opennem.spiders',
 'opennem.spiders.aemo',
 'opennem.spiders.apvi',
 'opennem.spiders.bom',
 'opennem.spiders.nem',
 'opennem.spiders.npi',
 'opennem.spiders.wem',
 'opennem.utils']

package_data = \
{'': ['*'],
 'opennem': ['data/au_cpi.json',
             'data/au_cpi.json',
             'data/au_cpi.json',
             'data/au_cpi.json',
             'data/au_cpi.json',
             'data/au_cpi.json',
             'data/au_cpi.json',
             'data/au_cpi.json',
             'data/au_cpi.json',
             'data/au_cpi.json',
             'data/au_cpi.json',
             'data/au_cpi.json',
             'data/au_cpi.json',
             'data/au_cpi.json',
             'data/au_cpi.json',
             'data/au_cpi.json',
             'data/au_cpi.json',
             'data/au_cpi.json',
             'data/au_cpi.json',
             'data/au_cpi.json',
             'data/bom_capitals.json',
             'data/bom_capitals.json',
             'data/bom_capitals.json',
             'data/bom_capitals.json',
             'data/bom_capitals.json',
             'data/bom_capitals.json',
             'data/bom_capitals.json',
             'data/bom_capitals.json',
             'data/bom_capitals.json',
             'data/bom_capitals.json',
             'data/bom_capitals.json',
             'data/bom_capitals.json',
             'data/bom_capitals.json',
             'data/bom_capitals.json',
             'data/bom_capitals.json',
             'data/bom_capitals.json',
             'data/bom_capitals.json',
             'data/bom_capitals.json',
             'data/bom_capitals.json',
             'data/bom_capitals.json',
             'data/bom_stations.json',
             'data/bom_stations.json',
             'data/bom_stations.json',
             'data/bom_stations.json',
             'data/bom_stations.json',
             'data/bom_stations.json',
             'data/bom_stations.json',
             'data/bom_stations.json',
             'data/bom_stations.json',
             'data/bom_stations.json',
             'data/bom_stations.json',
             'data/bom_stations.json',
             'data/bom_stations.json',
             'data/bom_stations.json',
             'data/bom_stations.json',
             'data/bom_stations.json',
             'data/bom_stations.json',
             'data/bom_stations.json',
             'data/bom_stations.json',
             'data/bom_stations.json',
             'data/diff_report.md',
             'data/diff_report.md',
             'data/diff_report.md',
             'data/diff_report.md',
             'data/diff_report.md',
             'data/diff_report.md',
             'data/diff_report.md',
             'data/diff_report.md',
             'data/diff_report.md',
             'data/diff_report.md',
             'data/diff_report.md',
             'data/diff_report.md',
             'data/diff_report.md',
             'data/diff_report.md',
             'data/diff_report.md',
             'data/diff_report.md',
             'data/diff_report.md',
             'data/diff_report.md',
             'data/diff_report.md',
             'data/diff_report.md',
             'data/mms.json',
             'data/mms.json',
             'data/mms.json',
             'data/mms.json',
             'data/mms.json',
             'data/mms.json',
             'data/mms.json',
             'data/mms.json',
             'data/mms.json',
             'data/mms.json',
             'data/mms.json',
             'data/mms.json',
             'data/mms.json',
             'data/mms.json',
             'data/mms.json',
             'data/mms.json',
             'data/mms.json',
             'data/mms.json',
             'data/mms.json',
             'data/mms.json',
             'data/mms/PUBLIC_DVD_INTERCONNECTOR_202006010000.CSV',
             'data/mms_duid_station_map.json',
             'data/mms_duid_station_map.json',
             'data/mms_duid_station_map.json',
             'data/mms_duid_station_map.json',
             'data/mms_duid_station_map.json',
             'data/mms_duid_station_map.json',
             'data/mms_duid_station_map.json',
             'data/mms_duid_station_map.json',
             'data/mms_duid_station_map.json',
             'data/mms_duid_station_map.json',
             'data/mms_duid_station_map.json',
             'data/mms_duid_station_map.json',
             'data/mms_duid_station_map.json',
             'data/mms_duid_station_map.json',
             'data/mms_duid_station_map.json',
             'data/mms_duid_station_map.json',
             'data/mms_duid_station_map.json',
             'data/mms_duid_station_map.json',
             'data/mms_duid_station_map.json',
             'data/mms_duid_station_map.json',
             'data/nem_emissions.csv',
             'data/nem_emissions.csv',
             'data/nem_emissions.csv',
             'data/nem_emissions.csv',
             'data/nem_emissions.csv',
             'data/nem_emissions.csv',
             'data/nem_emissions.csv',
             'data/nem_emissions.csv',
             'data/nem_emissions.csv',
             'data/nem_emissions.csv',
             'data/nem_emissions.csv',
             'data/nem_emissions.csv',
             'data/nem_emissions.csv',
             'data/nem_emissions.csv',
             'data/nem_emissions.csv',
             'data/nem_emissions.csv',
             'data/nem_emissions.csv',
             'data/nem_emissions.csv',
             'data/nem_emissions.csv',
             'data/nem_emissions.csv',
             'data/nem_gi.json',
             'data/nem_gi.json',
             'data/nem_gi.json',
             'data/nem_gi.json',
             'data/nem_gi.json',
             'data/nem_gi.json',
             'data/nem_gi.json',
             'data/nem_gi.json',
             'data/nem_gi.json',
             'data/nem_gi.json',
             'data/nem_gi.json',
             'data/nem_gi.json',
             'data/nem_gi.json',
             'data/nem_gi.json',
             'data/nem_gi.json',
             'data/nem_gi.json',
             'data/nem_gi.json',
             'data/nem_gi.json',
             'data/nem_gi.json',
             'data/nem_gi.json',
             'data/npi_facilities.json',
             'data/npi_facilities.json',
             'data/npi_facilities.json',
             'data/npi_facilities.json',
             'data/npi_facilities.json',
             'data/npi_facilities.json',
             'data/npi_facilities.json',
             'data/npi_facilities.json',
             'data/npi_facilities.json',
             'data/npi_facilities.json',
             'data/npi_facilities.json',
             'data/npi_facilities.json',
             'data/npi_facilities.json',
             'data/npi_facilities.json',
             'data/npi_facilities.json',
             'data/npi_facilities.json',
             'data/npi_facilities.json',
             'data/npi_facilities.json',
             'data/npi_facilities.json',
             'data/npi_facilities.json',
             'data/opennem.json',
             'data/opennem.json',
             'data/opennem.json',
             'data/opennem.json',
             'data/opennem.json',
             'data/opennem.json',
             'data/opennem.json',
             'data/opennem.json',
             'data/opennem.json',
             'data/opennem.json',
             'data/opennem.json',
             'data/opennem.json',
             'data/opennem.json',
             'data/opennem.json',
             'data/opennem.json',
             'data/opennem.json',
             'data/opennem.json',
             'data/opennem.json',
             'data/opennem.json',
             'data/opennem.json',
             'data/opennem_stations.json',
             'data/opennem_stations.json',
             'data/opennem_stations.json',
             'data/opennem_stations.json',
             'data/opennem_stations.json',
             'data/opennem_stations.json',
             'data/opennem_stations.json',
             'data/opennem_stations.json',
             'data/opennem_stations.json',
             'data/opennem_stations.json',
             'data/opennem_stations.json',
             'data/opennem_stations.json',
             'data/opennem_stations.json',
             'data/opennem_stations.json',
             'data/opennem_stations.json',
             'data/opennem_stations.json',
             'data/opennem_stations.json',
             'data/opennem_stations.json',
             'data/opennem_stations.json',
             'data/opennem_stations.json',
             'data/registry.json',
             'data/registry.json',
             'data/registry.json',
             'data/registry.json',
             'data/registry.json',
             'data/registry.json',
             'data/registry.json',
             'data/registry.json',
             'data/registry.json',
             'data/registry.json',
             'data/registry.json',
             'data/registry.json',
             'data/registry.json',
             'data/registry.json',
             'data/registry.json',
             'data/registry.json',
             'data/registry.json',
             'data/registry.json',
             'data/registry.json',
             'data/registry.json',
             'data/rel.json',
             'data/rel.json',
             'data/rel.json',
             'data/rel.json',
             'data/rel.json',
             'data/rel.json',
             'data/rel.json',
             'data/rel.json',
             'data/rel.json',
             'data/rel.json',
             'data/rel.json',
             'data/rel.json',
             'data/rel.json',
             'data/rel.json',
             'data/rel.json',
             'data/rel.json',
             'data/rel.json',
             'data/rel.json',
             'data/rel.json',
             'data/rel.json',
             'data/stations.csv',
             'data/stations.csv',
             'data/stations.csv',
             'data/stations.csv',
             'data/stations.csv',
             'data/stations.csv',
             'data/stations.csv',
             'data/stations.csv',
             'data/stations.csv',
             'data/stations.csv',
             'data/stations.csv',
             'data/stations.csv',
             'data/stations.csv',
             'data/stations.csv',
             'data/stations.csv',
             'data/stations.csv',
             'data/stations.csv',
             'data/stations.csv',
             'data/stations.csv',
             'data/stations.csv',
             'data/stations.geojson',
             'data/stations.geojson',
             'data/stations.geojson',
             'data/stations.geojson',
             'data/stations.geojson',
             'data/stations.geojson',
             'data/stations.geojson',
             'data/stations.geojson',
             'data/stations.geojson',
             'data/stations.geojson',
             'data/stations.geojson',
             'data/stations.geojson',
             'data/stations.geojson',
             'data/stations.geojson',
             'data/stations.geojson',
             'data/stations.geojson',
             'data/stations.geojson',
             'data/stations.geojson',
             'data/stations.geojson',
             'data/stations.geojson',
             'data/stations.json',
             'data/stations.json',
             'data/stations.json',
             'data/stations.json',
             'data/stations.json',
             'data/stations.json',
             'data/stations.json',
             'data/stations.json',
             'data/stations.json',
             'data/stations.json',
             'data/stations.json',
             'data/stations.json',
             'data/stations.json',
             'data/stations.json',
             'data/stations.json',
             'data/stations.json',
             'data/stations.json',
             'data/stations.json',
             'data/stations.json',
             'data/stations.json',
             'data/wem_emissions.csv',
             'data/wem_emissions.csv',
             'data/wem_emissions.csv',
             'data/wem_emissions.csv',
             'data/wem_emissions.csv',
             'data/wem_emissions.csv',
             'data/wem_emissions.csv',
             'data/wem_emissions.csv',
             'data/wem_emissions.csv',
             'data/wem_emissions.csv',
             'data/wem_emissions.csv',
             'data/wem_emissions.csv',
             'data/wem_emissions.csv',
             'data/wem_emissions.csv',
             'data/wem_emissions.csv',
             'data/wem_emissions.csv',
             'data/wem_emissions.csv',
             'data/wem_emissions.csv',
             'data/wem_emissions.csv',
             'data/wem_emissions.csv',
             'data/wikidata-parsed.json',
             'data/wikidata-parsed.json',
             'data/wikidata-parsed.json',
             'data/wikidata-parsed.json',
             'data/wikidata-parsed.json',
             'data/wikidata-parsed.json',
             'data/wikidata-parsed.json',
             'data/wikidata-parsed.json',
             'data/wikidata-parsed.json',
             'data/wikidata-parsed.json',
             'data/wikidata-parsed.json',
             'data/wikidata-parsed.json',
             'data/wikidata-parsed.json',
             'data/wikidata-parsed.json',
             'data/wikidata-parsed.json',
             'data/wikidata-parsed.json',
             'data/wikidata-parsed.json',
             'data/wikidata-parsed.json',
             'data/wikidata-parsed.json',
             'data/wikidata-parsed.json',
             'data/wikidata-photos.json',
             'data/wikidata-photos.json',
             'data/wikidata-photos.json',
             'data/wikidata-photos.json',
             'data/wikidata-photos.json',
             'data/wikidata-photos.json',
             'data/wikidata-photos.json',
             'data/wikidata-photos.json',
             'data/wikidata-photos.json',
             'data/wikidata-photos.json',
             'data/wikidata-photos.json',
             'data/wikidata-photos.json',
             'data/wikidata-photos.json',
             'data/wikidata-photos.json',
             'data/wikidata-photos.json',
             'data/wikidata-photos.json',
             'data/wikidata-photos.json',
             'data/wikidata-photos.json',
             'data/wikidata-photos.json',
             'data/wikidata-photos.json',
             'data/wikidata.json',
             'data/wikidata.json',
             'data/wikidata.json',
             'data/wikidata.json',
             'data/wikidata.json',
             'data/wikidata.json',
             'data/wikidata.json',
             'data/wikidata.json',
             'data/wikidata.json',
             'data/wikidata.json',
             'data/wikidata.json',
             'data/wikidata.json',
             'data/wikidata.json',
             'data/wikidata.json',
             'data/wikidata.json',
             'data/wikidata.json',
             'data/wikidata.json',
             'data/wikidata.json',
             'data/wikidata.json',
             'data/wikidata.json',
             'static/empty'],
 'opennem.core': ['data/*'],
 'opennem.db': ['fixtures/*', 'views/*']}

install_requires = \
['Pint>=0.16.1,<0.17.0',
 'Wikidata>=0.7.0,<0.8.0',
 'alembic>=1.4.2,<2.0.0',
 'cachetools>=4.2.0,<5.0.0',
 'click>=7.1.2,<8.0.0',
 'databases[postgresql]>=0.4.1,<0.5.0',
 'dictalchemy>=0.1.2,<0.2.0',
 'geoalchemy2>=0.8.4,<0.9.0',
 'geojson-pydantic>=0.2.1,<0.3.0',
 'geojson>=2.5.0,<3.0.0',
 'huey>=2.2.0,<3.0.0',
 'openpyxl>=3.0.4,<4.0.0',
 'pillow>=8.0.1,<9.0.0',
 'prometheus-fastapi-instrumentator>=5.6.0,<6.0.0',
 'pydantic>=1.5.1,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'python-magic>=0.4.18,<0.5.0',
 'pytz>=2020.1,<2021.0',
 'pyyaml>=5.3.1,<6.0.0',
 'redis>=3.5.3,<4.0.0',
 'requests>=2.23.0,<3.0.0',
 'requests_cache>=0.5.2,<0.6.0',
 'scrapy>=2.1.0,<3.0.0',
 'sentry-sdk>=0.19.3,<0.20.0',
 'shapely>=1.7.0,<2.0.0',
 'smart-open[all]>=3.0.0,<4.0.0',
 'sqlalchemy>=1.3.17,<2.0.0',
 'tomlkit>=0.7.0,<0.8.0',
 'validators>=0.18.1,<0.19.0',
 'wikipedia>=1.4.0,<2.0.0',
 'xlrd>=2.0.1,<3.0.0']

extras_require = \
{':extra == "postgres"': ['psycopg2>=2.8.6,<3.0.0'],
 ':extra == "server"': ['uvicorn>=0.12.2,<0.13.0',
                        'fastapi[all]>=0.63.0,<0.64.0']}

entry_points = \
{'console_scripts': ['opennem = opennem.cli:main']}

setup_kwargs = {
    'name': 'opennem',
    'version': '3.6.0a5',
    'description': 'OpenNEM Australian Energy Data',
    'long_description': "# OpenNEM Energy Market Data Access\n\nThe OpenNEM project aims to make the wealth of public National Electricity Market (NEM) data more accessible to a wider audience.\n\nThis toolkit enables downloading, mirroring and accessing energy data from various networks\n\nProject homepage at https://opennem.org.au\n\nAvailable on Docker at https://hub.docker.com/r/opennem/opennem\n\nCurrently supports:\n\n- Australian NEM: https://www.nemweb.com.au/\n- West Australia Energy Market: http://data.wa.aemo.com.au/\n\n## Requirements\n\n * Python 3.7+ (see `.python-version` with `pyenv`)\n * Docker and `docker-compose` if you want to run the local dev stack\n\n## Quickstart\n\nWith poetry:\n\n```sh\n$ poetry install\n$ source .venv/bin/activate\n$ ./init.sh\n```\n\nWith pip + venv:\n\n```sh\n$ pip -m venv .venv\n$ pip install -r requirements.txt\n$ source .venv/bin/activate\n$ ./init.sh\n```\n\n## Install\n\nYou can install this project with python `pip`:\n\n```sh\n$ pip install opennem\n```\n\nOr alternatively with docker:\n\n```\n$ docker pull opennem/opennem\n```\n\nBundled with sqlite support. Other database drivers are optional and not installed by default. Install a supported database driver:\n\nPostgres:\n\n```sh\n$ pip install psycopg2\n```\n\n## Install Extras\n\nThe package contains extra modules that can be installed:\n\n```sh\n$ poetry install -E postgres\n```\n\nThe list of extras are:\n\n * `postgres` - Postgres database drivers\n * `server` - API server\n\n## Usage\n\nList the crawlers\n\n```sh\n$ scrapy list\n```\n\nCrawl\n\n```sh\n$ scrapy crawl au.nem.current.dispatch_scada\n```\n\n## Development\n\nThis project uses the new `pyproject.toml` project and build specification file. To make use of it use the `poetry` tool which can be installed on Windows, MacOS and Linux:\n\nhttps://python-poetry.org/docs/\n\nInstallation instructions for Poetry are at:\n\nhttps://python-poetry.org/docs/#installation\n\nBy default poetry will install virtual environments in your home metadata directory. A good alternative is to install the `venv` locally for each project with the following setting:\n\n```sh\n$ poetry config virtualenvs.in-project true\n```\n\nThis will create the virtual environment within the project folder in a folder called `.venv`. This folder is ignored by git by default.\n\nSetting up a virtual environment and installing requiements using Poetry:\n\n```sh\n$ poetry install\n```\n\nTo activate the virtual environment either run:\n\n```sh\n$ poetry shell\n```\n\nOr you can just activate the standard `venv`\n\n```sh\n$ source .venv/bin/activate\n```\n\nSettings are read from environment variables. Environment variables can be read from a `.env` file in the root of the folder. Setup the environment by copying the `.env.sample` file to `.env`. The defaults in the sample file map to the settings in `docker-compose.yml`\n\nThere is a `docker-compose` file that will bring a local database:\n\n```sh\n$ docker-compose up -d\n```\n\nBring up the database migrations using alembic:\n\n```sh\n$ alembic upgrade head\n```\n\nRun scrapy in the root folder for options:\n\n```sh\n$ scrapy\n```\n\nThe `opennem` cli interface provides other options and settings:\n\n```sh\n$ opennem -h\n```\n\nSettings for Visual Studio Code are stored in `.vscode`. Code is kept formatted and linted using `pylint`, `black` and `isort` with settings defined in `pyproject.toml`\n\n## Testing\n\nTests are in `tests/`\n\nRun tests with:\n\n```sh\n$ pytest\n```\n\nRun background test watcher with\n\n```sh\n$ ptw\n```\n\n## Build Release\n\nThe script `build-release.sh` will tag a new release, build the docker image, tag the git version, push to GitHub and push the latest\nrelease to PyPi\n\n\n## Architecture overview\n\nThis project uses [Scrapy](https://scrapy.org/) to obtain data from supported energy markets and [SQLAlchemy](https://www.sqlalchemy.org/) to store data, and [Alembic](https://alembic.sqlalchemy.org/en/latest/) for database migrations. Database storage has been tested with sqlite, postgres and mysql.\n\nOverview of scrapy architecture:\n\n![](https://docs.scrapy.org/en/latest/_images/scrapy_architecture_02.png)\n\n## Code Navigation\n\n* Spider definitions in `opennem/spiders`\n* Processing pipelines for crawls in `opennem/pipelines`\n* Database models for supported energy markets are stored in `opennem/db/models`\n\n## Deploy Crawlers\n\nYou can deploy the crawlers to the scrapyd server with:\n\n```sh\n$ scrapyd-deploy\n```\n\nIf you don't have that command and it isn't available install it with:\n\n```sh\n$ pip install scrapyd-client\n```\n\nWhich installs the [scrapyd-client](https://github.com/scrapy/scrapyd-client) tools. Project settings are read from `scrapy.cfg`\n",
    'author': 'Dylan McConnell',
    'author_email': 'dylan.mcconnell@unimelb.edu.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://opennem.org.au',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
