# Auction Scraper

>  Scrape auction data auction sites into a sqlite database

> Currently supports: catawiki, ebay, liveauctioneers

> Can be used as a CLI tool, or interfaced with directly

## Installation

You can [install with pip](https://pypi.org/project/auction-scraper/):

``` 
pip install auction-scraper
```

## New backend support
Want to scrape an auction house not listed above?  Fear not - through our partnership with [Dreaming Spires](dreamingspires.dev), you can request that we build additional backend scrapers to extend the functionality.  Email contact@dreamingspires.dev for more info.

We also accept PRs, so feel free to write your own backend and submit it, if you require.  Instructions for this can be found under the _Building new backends_ section.

## Usage

`auction-scraper` will scrape data from auctions, profiles, and searches on the specified auction site.  Resulting textual data is written to a `sqlite3` database, with images and backup web pages optionally being written to a _data directory_.

The tool is invoked as:

```
Usage: auction-scraper [OPTIONS] DB_PATH BACKEND:[ebay|liveauctioneers]
                       COMMAND [ARGS]...

Options:
  DB_PATH                         The path of the sqlite database file to be
                                  written to  [required]

  BACKEND:[ebay|liveauctioneers]  The auction scraping backend  [required]
  --data-location TEXT            The path additional image and html data is
                                  saved to

  --save-images / --no-save-images
                                  Save images to data-location.  Requires
                                  --data-location  [default: False]

  --save-pages / --no-save-pages  Save pages to data-location. Requires
                                  --data-location  [default: False]

  --verbose / --no-verbose        [default: False]
  --base-uri TEXT                 Override the base url used to resolve the
                                  auction site

  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.

Commands:
  auction  Scrapes an auction site auction page.
  profile  Scrapes an auction site profile page.
  search   Performs a search, returning the top n_results results for each...
```

### Auction mode
In auction mode, an auction must be specified as either a unique _auction ID_ or as a URL.  The textual data is scraped into the `[BACKEND]_auctions` table of `DB_PATH`, the page is scraped into `[data-location]/[BACKEND]/auctions`, and the images into `[data-location]/[BACKEND]/images`.  The `--base-url` option determines the base URL from which to resolve _auction IDs_, _profile IDs_, and search _query strings_ if specified, otherwise defaulting to the default for the specified backend.

Example usage:

```bash
# Scraping an auction by URL
auction-scraper db.db liveauctioneers auction https://www.liveauctioneers.com/item/88566418_cameroon-power-or-reliquary-figure

# Equivalently scraping from an auction ID
auction-scraper db.db liveauctioneers auction 88566418

# Scraping an auction, including all images and the page itself, into data-location
auction-scraper --data-location=./data --save-images --save-pages db.db liveauctioneers auction 88566418
```

### Profile mode
In profile mode, a profile must be specified as either a unique _user ID_ or as a URL.  The textual data is scraped into the `[BACKEND]_profiles` table of `DB_PATH`, and the page is scraped into `[data-location]/[BACKEND]/profiles`.  The `--base-url` option determines the base URL from which to resolve _auction IDs_, _profile IDs_, and search _query strings_ if specified, otherwise defaulting to the default for the specified backend.

Example usage:

```bash
# Scraping a profile by URL
auction-scraper db.db liveauctioneers profile https://www.liveauctioneers.com/auctioneer/197/hindman/

# Equivalently scraping from a profile ID
auction-scraper db.db liveauctioneers auction 197

# Scraping a profile, including the page itself, into data-location
auction-scraper --data-location=./data --save-pages db.db liveauctioneers profile 197
```


### Search mode
In search mode, at least one `QUERY_STRING` must be provided alongside `N_RESULTS`.  It will scrape the auctions pertaining to the top `N_RESULTS` results from the `QUERY_STRING`.  The `--base-url` option determines the base URL from which to resolve the search if specified, otherwise defaulting to the default for the specified backend.

Example usage:
```bash
# Search one result by a single search term
auction-scraper db.db search 1 "mambila art"

# Search ten results by two search terms, scraping images and pages into data-location
auction-scraper --data-location=./data --save-images --save-pages db.db search 10 "mambila" "mambilla"
```

## Running continuously using systemd
`auction-scraper@.service` and `auction-scraper@.timer`, once loaded by systemd, can be used to schedule the running of `auction-scraper` with user-given arguments according to a schedule.

### Running as a systemd root service

Copy `auction-scraper@.service` and `auction-scraper@.timer` to `/etc/systemd/system/`.

Modify `auction-scraper@.timer` to specify the schedule you require.

Reload the system daemons.  As root:
```bash
systemctl daemon-reload
```

Run (start now) and enable (restart on boot) the systemd-timer, specifying the given arguments, within quotes, after the '@'.  For example, as root:
```bash
systemctl enable --now auction-scraper@"db.db liveauctioneers search 10 mambila".timer
```

Find information about your running timers with:
```bash
systemctl list-timers
```

Stop your currently running timer with:
```bash
systemctl stop auction-scraper@"db.db liveauctioneers search 10 mambila".timer
```

Disable your currently running timer with:
```bash
systemctl disable auction-scraper@"db.db liveauctioneers search 10 mambila".timer
```

A new timer is created for each unique argument string, so the arguments must be specified when stopping or disabling the timer.

Some modification may be required to run as a user service, including placing the service and timer files in `~/.local/share/systemd/user/`.

## Building from source

Ensure poetry is [installed](https://python-poetry.org/docs/#installation).  Then from this directory install dependencies into the poetry virtual environment and build:

```bash
poetry install
poetry build
```

Source and wheel files are built into `auction_scraper/dist`.

Install it across your user with `pip`, outside the venv:
```bash
cd ./dist
python3 -m pip install --user ./auction_scraper-0.0.1-py3-none-any.whl
```

or

```bash
cd ./dist
pip install ./auction_scraper-0.0.1-py3-none-any.whl
```

Run `auction-scraper` to invoke the utility.

## Interfacing with the API
Each backend of `auction-scraper` can also be invoked as a Python library to automate its operation.  The backends implement the abstract class `auction_scraper.abstract_scraper.AbstractAuctionScraper`, alongside the abstract SQLAlchemy models `auction_scraper.abstract_models.BaseAuction` and `auction_scraper.abstract_models.BaseProfile`.
The resulting scraper exposes methods to scrape auction, profile, and search pages into these SQLAlchemy model objects, according to the following interface:

```
def scrape_auction(self, auction, save_page=False, save_images=False):
    """
    Scrapes an auction page, specified by either a unique auction ID
    or a URI.  Returns an auction model containing the scraped data.
    If specified by auction ID, constructs the URI using self.base_uri.
    If self.page_save_path is set, writes out the downloaded pages to disk at
    the given path according to the naming convention specified by
    self.auction_save_name.
    Returns a BaseAuction
    """
```

```
def scrape_profile(self, profile, save_page=False):
    """
    Scrapes a profile page, specified by either a unique profile ID
    or a URI.  Returns an profile model containing the scraped data.
    If specified by profile ID, constructs the URI using self.base_uri.
    If self.page_save_path is set, writes out the downloaded pages to disk at
    the given path according to the naming convention specified by
    self.profile_save_name.
    Returns a BaseProfile
    """
```

```
def scrape_search(self, query_string, n_results=None, save_page=False,
        save_images=False):
    """
    Scrapes a search page, specified by either a query_string and n_results,
    or by a unique URI.
    If specified by query_string, de-paginates the results and returns up
    to n_results results.  If n_results is None, returns all results.
    If specified by a search_uri, returns just the results on the page.
    Returns a dict {auction_id: SearchResult}
    """
```

```
def scrape_auction_to_db(self, auction, save_page=False, save_images=False):
    """
    Scrape an auction page, writing the resulting page to the database.
    Returns a BaseAuction
    """
```

```
def scrape_profile_to_db(self, profile, save_page=False):
    """
    Scrape a profile page, writing the resulting profile to the database.
    Returns a BaseProfile
    """
```

```
def scrape_search_to_db(self, query_strings, n_results=None, \
        save_page=False, save_images=False):
    """
    Scrape a set of query_strings, writing the resulting auctions and profiles
    to the database.
    Returns a tuple ([BaseAuction], [BaseProfile])
    """
```

## Building new backends
All backends live at `action_scraper/scrapers` in their own specific directory.  It should implement the abstract class `auction_scraper.abstract_scraper.AbstractAuctionScraper` in a file `scraper.py`, and the abstract SQLAlchemy models `auction_scraper.abstract_models.BaseAuction` and `auction_scraper.abstract_models.BaseProfile` in `models.py`.

The `AuctionScraper` class must extend `AbstractAuctionScraper` and implement the following methods:
```python3
# Given a uri, scrape the auction page into an auction object (of type BaseAuction)
def _scrape_auction_page(self, uri)

# Given a uri, scrape the profile page into an profile object (of type BaseAuction)
def _scrape_profile_page(self, uri)

# Given a uri, scrape the search page into a list of results (of type {auction_id: SearchResult})
def _scrape_search_page(self, uri)
```

It must also supply defaults to the following variables:
```python3
auction_table
profile_table
base_uri
auction_suffix
profile_suffix
search_suffix
backend_name
```

## Authors
Edd Salkield <edd@salkield.uk>  - Main codebase

Mark Todd                       - Liveauctioneers scraper

Jonathan Tanner                 - Catawiki scraper
