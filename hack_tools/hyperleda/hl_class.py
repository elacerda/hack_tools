import os.path as p
import pandas as pd
from urllib.request import urlretrieve

_hl_url = 'http://leda.univ-lyon1.fr/ledacat.cgi?o='

class galaxy(object):
    """
    Attributes
    ----------
    name : string
        The galaxy name.
    hl_url : string
        The hyperleda url.
    table : pandas.DataFrame
        The hyperleda galaxy http page converted to `pandas.DataFrame`.
    table_path : string
        The hyperleda galaxy html page path, either online or cached.
    props_table : pandas.DataFrame
        The hyperleda galaxy table with galaxy properties converted to `pandas.DataFrame`.

    Methods
    -------
    cache : Set the hyperleda galaxy html page path, either online or cached.

    """
    def __init__(self, galaxy_name, hl_url=None, cache=False, cache_dir=None, force_cache=False):
        self.name = galaxy_name
        self.hl_url = hl_url
        if self.hl_url is None:
            self.hl_url = _hl_url
        self.cache(cache, cache_dir, force_cache)
        self.tables = pd.read_html(self.table_path)
        self._props()

    def cache(self, cache=False, cache_dir=None, force_cache=False):
        """
        Set the hyperleda galaxy html page path, either online or cached.

        Parameters
        ----------
        cache : bool
            If True downloads the page from hyperleda. Default is False.
        cache_dir : string
            The directory whether will store the downloaded page or point
            to the cached one. Default is None.
        """
        galaxy_hl_url = self.hl_url + self.name
        galaxy_cache_file = f'{cache_dir}/{self.name}_hyperleda_http.html'
        if not p.exists(galaxy_cache_file):
            if cache or force_cache:
                urlretrieve(galaxy_hl_url, galaxy_cache_file)
            else:
                galaxy_cache_file = galaxy_hl_url
        else:
            if force_cache:
                urlretrieve(galaxy_hl_url, galaxy_cache_file)
        self.table_path = galaxy_cache_file

    def _props(self):
        """
        Reads and configures the hyperleda galaxy table with galaxy properties.
        """
        if (len(self.tables) <= 5):
            self.props_table = None
        else:
            df_props = self.tables[5]
            columns = [df_props[i][0] for i in range(len(df_props.columns))]
            df_props.columns = columns
            self.props_table = df_props.drop(df_props.index[0]).set_index('Parameter', drop=True)
