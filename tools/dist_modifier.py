import sys
import pandas as pd

def main():
    """
    sample usage: dist_modifier.py<nl_path> <dist_path> <cleaned_output_path>
    """
    nl_path = sys.argv[1]
    dist_path = sys.argv[2]
    cleaned_output_path = sys.argv[3]

    nl = pd.read_csv(nl_path)
    dist = pd.read_csv(dist_path)
    nl_cst = set(nl["country_iso3"].unique())
    dist = dist[dist["iso_o"].isin(nl_cst) & dist["iso_d"].isin(nl_cst)]
    dist = dist.rename(columns={"iso_o": "source", "iso_d": "target"})
    dist.to_csv(cleaned_output_path, index=False) 

if __name__ == '__main__':
    main()
