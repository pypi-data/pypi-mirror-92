"""Store and update a local compound cache."""
# Written by Kevin Shebek
# August 2020
import shutil
from pathlib import Path
from typing import List, Union

import pandas as pd
import quilt
from equilibrator_cache import Compound, CompoundIdentifier, Registry
from equilibrator_cache.api import create_compound_cache_from_sqlite_file

from .generate_compound import get_or_create_compound


DEFAULT_QUILT_PKG = "equilibrator/cache"
DEFAULT_CACHE_PATH = "./local_cache"


class LocalCompoundCache(object):
    """Read from and update a local compound cache."""

    def __init__(self, ccache_path: str = None):
        """Create a local cache object."""
        self.ccache = None
        self.ccache_path = None
        if ccache_path:
            self.load_cache(ccache_path)

    def load_cache(self, ccache_path: str = DEFAULT_CACHE_PATH) -> None:
        """Load a cache from a .sqlite file locally.

        Load a local cache from a compound.sqlite file derived from
        the equilibrator/cache package.

        Parameters
        ----------
        ccache_path : str
            The location from which to load the cache. Default is "./cache"
        """
        ccache_path = Path(ccache_path)
        self.ccache_path = ccache_path
        sqlite_path = ccache_path / "compounds.sqlite"

        if ccache_path.is_file():
            print("Provided cache path is a file. Please provide a folder.")

        elif ccache_path.is_dir():
            if sqlite_path.is_file():
                print(f"Loading compounds from {ccache_path}")
                if self.ccache:
                    self.ccache.session.close()
                self.ccache = create_compound_cache_from_sqlite_file(
                    sqlite_path
                )
            else:
                print(f"compounds.sqlite not found at {ccache_path}.")

        return None

    def generate_local_cache_from_default_quilt(
        self, ccache_path: str = DEFAULT_CACHE_PATH
    ) -> None:
        """Create a local cache from the default quilt package at a specified location.

        Parameters
        ----------
        ccache_path : str
            The folder to export the cache into. Default is "./cache"
        """
        ccache_path = Path(ccache_path)

        if ccache_path.is_file():
            print("Provided cache path is a file. Please specify a folder.")
            return None
        elif ccache_path.is_dir():
            print(f"{ccache_path} already exists.")
            print("Delete folder and its contents and create new local cache?")

            choice = ""
            while choice.lower() not in ["yes", "no"]:
                choice = input("Proceed? (yes/no):")

            if choice.lower() == "no":
                print("Local cache generation cancelled.")
                return None
            else:
                print(f"Deleting {ccache_path}")
                shutil.rmtree(ccache_path, ignore_errors=True)

        print(
            (
                "Exporting new cache from equilibrator/cache quilt package"
                f" to {ccache_path}\n"
            )
        )
        quilt.install(DEFAULT_QUILT_PKG, force=True)
        quilt.export(DEFAULT_QUILT_PKG, ccache_path)

    def get_compounds(
        self, _mol_strings: Union[str, List[str]], mol_format: str = "smiles"
    ) -> Union[Compound, List[Compound]]:
        """Get and insert compounds to the local cache.

        Get compounds from the local cache by descriptors, or creates them
        if missed. Created compounds are stored in the local cache to
        persist for later access.

        Parameters
        ----------
        _mol_strings : List[str]
            A string or list of strings containing text description of the
            molecule(s) (SMILES or InChI)

        mol_format : str
            The format in which the molecule is given: 'inchi', 'smiles'

        Returns
        -------
        Compound or List[Compound]
            A Compound object or list thereof that is used to calculate
            Gibbs free energy of formation and reactions.

        """
        if not self.ccache:
            print("Please load a cache first with load_cache()")
            return None

        compounds = get_or_create_compound(
            self.ccache, _mol_strings, mol_format
        )

        # Process compound results.
        # If compounds have a negative id do the following
        # for insertion to .sqlite:
        #  1. Delete ID so insertion to db assigns automatic ID
        #  2. change group_vector to a list to avoid pickle issues upon recall
        if type(compounds) == list:
            for compound in compounds:
                if compound.id <= -1:
                    del compound.id
                    compound.group_vector = list(compound.group_vector)
                    # insert compound to local session
                    self.ccache.session.add(compound)
        else:
            if compounds.id <= -1:
                del compounds.id
                compounds.group_vector = list(compounds.group_vector)
                # insert compound to local session
                self.ccache.session.add(compounds)

        self.ccache.session.commit()
        return compounds

    def add_compounds(self, compound_df: pd.DataFrame) -> None:
        """Get and insert compounds to the local cache.

        Add compounds from a dataframe containing both smiles
        and coco_id columns.

        Parameters
        ----------
        compound_df : DataFrame
            A frame with the compound descriptors and IDs for the database.
        """
        # Check if specified coco_id is already in compounds registry
        def in_identifiers(compound, new_identifier):
            for identifier in compound.identifiers:
                if (
                    identifier.registry == new_identifier.registry
                    and identifier.accession == new_identifier.accession
                ):
                    return True
                else:
                    continue
            return False

        coco_registry = (
            self.ccache.session.query(Registry)
            .filter_by(namespace="coco")
            .one()
        )

        # Attempt to add every compound to the local cache
        # Afterwards insert coco_id if not already existing
        compound_df["compound"] = self.get_compounds(
            list(compound_df["smiles"])
        )
        compound_df["coco_id"] = compound_df.coco_id.apply(
            lambda c: CompoundIdentifier(registry=coco_registry, accession=c)
        )

        # Add ids into coco namespace.
        # Adds values into existing compounds if they don't exist.
        for row in compound_df.itertuples(index=False):
            if not in_identifiers(row.compound, row.coco_id):
                row.compound.identifiers.append(row.coco_id)
                self.ccache.session.commit()
            else:
                print(
                    (
                        f"{row.coco_id.accession} already exists"
                        "in the coco namespace."
                    )
                )
