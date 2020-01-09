import json
import pandas as pd


def main():
    df = pd.read_csv("gene_table.txt", sep="\t")
    entrez = pd.read_csv("gene_entrezid.txt", sep="\t")

    entrez_2_ensembl = {}
    for index, row in entrez.iterrows():
        ensembl_id = row["ENSEMBL"]
        entrez_id = str(row["ENTREZID"])
        entrez_2_ensembl.setdefault(entrez_id, []).append(ensembl_id)

    with open("go_geneset.json", "rt") as fh:
        go = json.load(fh)
    
    df["go_ids"] = ""
    for go_id, entrez_ids in go.items():
        for entrez_id in entrez_ids:
            ensembl_ids = entrez_2_ensembl.get(entrez_id)
            if not ensembl_ids:
                continue
            for ensembl_id in ensembl_ids:
                df.loc[df["gene_id"] == ensembl_id, "go_ids"] += "|" + go_id

    df.to_csv("gene_table_goids.txt", sep="\t")


if __name__ == "__main__":
    main()
