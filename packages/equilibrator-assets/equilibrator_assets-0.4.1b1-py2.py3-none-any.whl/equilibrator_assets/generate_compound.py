# The MIT License (MIT)
#
# Copyright (c) 2013 The Weizmann Institute of Science.
# Copyright (c) 2018 Institute for Molecular Systems Biology, ETH Zurich.
# Copyright (c) 2018 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


"""Create Compound objects outside of the compound-cache."""
from typing import List, Union

import pandas as pd
from equilibrator_cache import Compound, CompoundCache, CompoundMicrospecies
from openbabel.pybel import readstring

from equilibrator_assets import group_decompose, molecule, thermodynamics


group_decomposer = group_decompose.GroupDecomposer()


def create_compound(
    _mol_strings: Union[str, List[str]], mol_format: str = "smiles"
) -> List[Compound]:
    """
    Generate a Compound object directly from SMILESs or InChIs.

    Parameters
    ----------
    _mol_strings : str or List[str]
        A string or list of strings containing text description of the
        molecule(s) (SMILES or InChI)

    mol_format : str
        The format in which the molecules are given: 'inchi', 'smiles'

    Returns
    -------
    Compound or List[Compound]
        A Compound object or list thereof that can be used to calculate Gibbs
        free energy of formation and reactions.

    """
    if type(_mol_strings) == str:
        mol_strings = [_mol_strings]
    else:
        mol_strings = _mol_strings

    molecules = pd.DataFrame(
        data=[[-1 - i, s] for i, s in enumerate(mol_strings)],
        columns=[
            "id",
            "inchi",
        ],  # note that the "inchi" column can also contain SMILES strings
    )
    molecules["inchi_key"] = molecules.inchi.apply(
        lambda s: readstring(mol_format, s).write("inchikey").strip()
    )
    molecules["compound_dict"] = list(
        thermodynamics.get_compound_mappings(
            molecules, "foo", num_acidic=20, num_basic=20
        )
    )
    molecules["compound"] = molecules.compound_dict.apply(
        lambda d: Compound(**d)
    )

    for row in molecules.itertuples():

        # Specify Compound information not specified in compound_mappings
        row.compound.inchi_key = row.inchi_key

        # Decompose the compounds into the group vectors
        mol = molecule.Molecule.FromSmiles(row.compound.smiles)
        decomposition = group_decomposer.Decompose(
            mol, ignore_protonations=False, raise_exception=True
        )
        row.compound.group_vector = decomposition.AsVector()

        for ms_dict in thermodynamics.create_microspecies_mappings(
            row.compound
        ):
            ms = CompoundMicrospecies(**ms_dict)
            row.compound.microspecies.append(ms)
    if type(_mol_strings) == str:
        return molecules.compound.iat[0]
    else:
        return molecules.compound.tolist()


def get_or_create_compound(
    ccache: CompoundCache,
    _mol_strings: Union[str, List[str]],
    mol_format: str = "smiles",
) -> Union[Compound, List[Compound]]:
    """Get compounds from cache by descriptors, or creates them if missed.

    Parameters
    ----------
    ccache : CompoundCache

    mol_strings : List[str]
        A string or list of strings containing text description of the
        molecule(s) (SMILES or InChI)

    mol_format : str
        The format in which the molecule is given: 'inchi', 'smiles'

    Returns
    -------
    Compound or List[Compound]
        A Compound object or list thereof that is used to calculate Gibbs free
        energy of formation and reactions.

    """
    if type(_mol_strings) == str:
        mol_strings = [_mol_strings]
    else:
        mol_strings = _mol_strings

    data = []
    for s in mol_strings:
        inchi_key = readstring(mol_format, s).write("inchikey").strip()
        cc_search = ccache.search_compound_by_inchi_key(
            inchi_key.rsplit("-", 1)[0]
        )
        if cc_search:
            data.append((s, cc_search[0]))
        else:
            data.append((s, None))

    result_df = pd.DataFrame(data=data, columns=["mol_string", "compound"])
    misses = result_df.loc[pd.isnull(result_df.compound), :].index
    if len(misses) > 0:
        result_df.loc[misses, "compound"] = create_compound(
            result_df.loc[misses, "mol_string"].tolist(), mol_format
        )

    if type(_mol_strings) == str:
        return result_df.compound.iat[0]
    else:
        return result_df.compound.tolist()
