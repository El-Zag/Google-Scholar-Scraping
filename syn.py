import pubchempy as pcp

#function which return a list of synonym(str) for a given name of a molecule or a given pubchem number

def synonyms(mol):

    if type(mol)==int:
        molecule = pcp.Compound.from_cid(mol)
        return molecule.synonyms
    elif type(mol)==str:
        molecule = pcp.get_compounds(mol, 'name')
        return(molecule[0].synonyms)
    else: return ("Veuillez entrer un nom de molécule ou un numéro de référence pubchem svp")


print(synonyms("rutin"))








