import os
from glob import glob
import json
import pandas as pd
from itertools import combinations
from statsmodels.stats.inter_rater import cohens_kappa, fleiss_kappa
from collections import defaultdict

ROOT_FILE = os.getcwd()

def get_test_annotation(annotation_data):
    return {**annotation_data["test"]}


def average_pairwise_cohen_kapp(df):
    kappas = []
    for col1, col2 in combinations(df.columns, 2):
        # Create a contingency table
        contingency_table = pd.crosstab(df[col1], df[col2])
        kappa = cohens_kappa(contingency_table.values)
        kappas.append(kappa.kappa)
        print(f"Cohen's Kappa between {col1} and {col2}: {kappa.kappa:.2f}")

    # Average pairwise Cohen's Kappa
    average_kappa = sum(kappas) / len(kappas)
    print(f"Average Pairwise Cohen's Kappa: {average_kappa:.2f}")
    return average_kappa


def calculate_fleiss_kappa(df):
    # Convert the DataFrame to the format required by fleiss_kappa
    df = df.apply(pd.Series.value_counts, axis=1).fillna(0)
    kappa = fleiss_kappa(df.values)
    print(f"Fleiss' Kappa: {kappa:.2f}")
    return kappa


def load_annotations(source_dir):
    annotations = []
    for filename in os.listdir(source_dir):
        if filename.endswith(".json"):
            with open(os.path.join(source_dir, filename), "r") as f:
                annotations.append(json.load(f))
    return annotations


def majority_vote(annotations):
    combined = {"test": defaultdict(list)}

    for annotation in annotations:
        for query_id, value in annotation["test"].items():
            combined["test"][query_id].append(1 if value != "0" else 0)

    unified = {"test": {}}
    for query_id, votes in combined["test"].items():
        unified["test"][query_id] = "1" if sum(votes) > len(votes) / 2 else "0"

    return unified


def save_unified_annotations(unified):
    with open("./unified_annotations.json", "w") as f:
        json.dump(unified, f, indent=4)
    print(f"Unified annotations saved to unified_annotations.json")


if __name__ == "__main__":
    # Existing processing logic
    annotation_path = os.path.join(ROOT_FILE, "trec_ikat_2023_new_annotations")
    annotation_files = glob(os.path.join(annotation_path, "*.json"))
    annotations = load_annotations(annotation_path)
    unified = majority_vote(annotations)
    annotation_df = pd.DataFrame()

    for i, file in enumerate(annotation_files):
        file_identifier = os.path.basename(file).split(".")[0]
        with open(file, "r") as f:
            data = json.load(f)

        concat_data = get_test_annotation(data)
        ann_df = pd.DataFrame(
            list(concat_data.items()),
            columns=["problem_number", f"label_{file_identifier}"],
        )

        # Generate binary labels
        ann_df[f"binary_label_{file_identifier}"] = ann_df[
            f"label_{file_identifier}"
        ].apply(lambda x: 1 if x != "0" else 0)
        annotation_df = (
            ann_df
            if annotation_df.empty
            else annotation_df.merge(ann_df, on="problem_number")
        )
    binary_annotation = annotation_df.filter(regex="binary_label*")

    average_pairwise_cohen_kapp(binary_annotation)
    calculate_fleiss_kappa(binary_annotation)
    save_unified_annotations(unified)

    print("Done")
