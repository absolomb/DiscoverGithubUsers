# DiscoverGithubUsers

A small Python script to find company related Github users using the Github API and dump out all of their respective repos to search for possible company secrets.

```
  ____  _                                ____ _ _   _           _       _   _
 |  _ \(_)___  ___ _____   _____ _ __   / ___(_) |_| |__  _   _| |__   | | | |___  ___ _ __ ___
 | | | | / __|/ __/ _ \ \ / / _ \ '__| | |  _| | __| '_ \| | | | '_ \  | | | / __|/ _ \ '__/ __|
 | |_| | \__ \ (_| (_) \ V /  __/ |    | |_| | | |_| | | | |_| | |_) | | |_| \__ \  __/ |  \__ \
 |____/|_|___/\___\___/ \_/ \___|_|     \____|_|\__|_| |_|\__,_|_.__/   \___/|___/\___|_|  |___/

usage: DiscoverGitHubUsers.py [-h] [-k keyword] [-d domain] [-t token] [-g] [-o organization] [--no_filter]

Github Search Arguments.

optional arguments:
  -h, --help       show this help message and exit
  -k keyword       Keyword to search i.e. company name
  -d domain        Company domain name to search i.e company.com
  -t token         Github Personal Access Token
  -g               Output cloneable git URLs
  -o organization  Github Organization name (if different than keyword specified)
  --no_filter      Don't filter to reduce false positives and return all results
```

## Installation

The only requirement is the `PyGithub` module which can be installed with:
```
$ pip install PyGithub
```

## Usage

First you'll want to go create a Github Personal Access Token to avoid the non-authenticated API limits: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

Basic usage includes supplying a keyword with `-k` and a domain name with `-d`. You'll also pass your token value with a `-t`. If you know the organization username you can pass that value with `-o`.

By default all discovered users and their repos will output into `repos.txt` with all URLs. If you want cloneable git URLs pass the `-g` flag.

Also by default, filtering will be done on various fields for each user discovered with the general keyword value to reduce false positives. This includes things like the company, bio, email, and blog fields. By filtering these fields it's much more likely to find users associated with the targeted company. However if you don't have many results or just want to be extra thorough you can disable filtering with `--no_filter`.

Example usage:
```
python3 DiscoverGitHubUsers.py -k "companyname" -d company.com -o orgusername -g -t <TOKEN> 
```

For further use you can leverage discovered repos using the output file and with tools such as `trufflehog` to directly feed repo URLs.

```
for repo in $(cat repos.txt); do echo "[+] Checking $repo";~/tools/trufflehog github --repo=$repo;done
```
