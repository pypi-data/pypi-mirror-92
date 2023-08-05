# cvelib

A library and command line interface for the CVE Project services.

## Installation

```
pip install --user cvelib
```

Python version 3.6 or greater is required.

## CLI Setup and Configuration

Currently, the only supported CVE Project service is the CVE ID Reservation (IDR) service. Each
command executed against IDR requires the user to authenticate. You can provide the
authentication details with the command (using options `-u/--username`, `-o/--org`, and
`-a/--api-key`) or set them in the following environment variables:

```
export CVE_USER=margo
export CVE_ORG=acme
export CVE_API_KEY=<api_key>
```

Additionial options that have an accompanying environment variable include:

* `-e/--environment` or `CVE_ENVIRONMENT`: allows you to configure the deployment environment
  (that is, the URL at which the service is available) to interface with. Allowed values: `prod`,
  `dev`.

* `--idr-url` or `CVE_IDR_URL`: allows you to override the URL for the IDR service that would
  otherwise be determined by the deployment environment you selected. This is useful for local
  testing to point to an IDR instance running on localhost.

* `-i/--interactive` or `CVE_INTERACTIVE`: every create/update action against the IDR service
  will require confirmation before a request is sent.

## CLI Usage

Available options and commands can be displayed by running `cve --help`. The following are
examples of some commonly used operations.

Reserve one CVE ID in the current year (you will be prompted to confirm your action):

```
cve --interactive reserve
```

Reserve three non-sequential CVE IDs for a specific year:

```
cve reserve 3 --year 2021 --random
```

List all rejected CVEs for year 2018:

```
cve list --year 2018 --state reject
```

## Development Setup

```bash
git clone https://github.com/RedHatProductSecurity/cvelib.git
cd cvelib
python3 -m venv venv  # Must be Python 3.6 or later
source venv/bin/activate
pip install --upgrade pip
pip install -e .
pip install tox
```

This project uses the [Black](https://black.readthedocs.io) code formatter. To reformat the entire
code base after you make any changes, run:

```bash
# Reformat code base with Black
pip install black
black .
```

Running tests:

```bash
# Run all tests and format check (also run as a Github action)
tox
# Run format check only
tox -e black
# Run tests against Python 3.6 only
tox -e py36
# Run a single test against Python 3.6 only
tox -e py36 -- tests/test_cli.py::test_cve_show
```

---

[CVE](https://cve.mitre.org/) is a trademark of [The MITRE Corporation](https://www.mitre.org/).
