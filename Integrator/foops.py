from collections import Counter
import rdflib
from sys import argv
from rdflib.namespace import RDF, OWL
import requests
import traceback
import os
import json
from . import dolog, tools_conf, build_path_all, get_target_home, log_file_dir, g

FOOPS_URL = "https://foops.linkeddata.es/assessOntology"


def get_ontology_github_url(repo, branch, ontology):
    """
    repo: username/repo_name
    branch: the GitHub branch
    ontology: should start with the /
    """
    return f"https://github.com/{repo}/raw/refs/heads/{branch}{ontology}"


def save_foops_scores(data_path, output_path):
    with open(data_path) as f:
        data = f.read()
    scores = compute_foops_scores(data)
    results_txt = json.dumps(scores)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(results_txt)

    print(f"Scores saved to {output_path}")


def compute_foops_scores(data):
    """
    Compute the scores for each category given foops raw json
    """
    if isinstance(data, dict):
        j = data
    elif isinstance(data, str):
        j = json.loads(data)
    else:
        raise Exception(f"FOOPS SCORES UNKNOWN DATA TYPE {type(data)}")

    scores = {
        "Overall": j["overall_score"]
    }
    fair = dict()
    for check in j["checks"]:
        category = check["category_id"]
        if category not in fair:
            fair[category] = {
                "tests": 0,
                "passed": 0
            }
        fair[category]["tests"] += check["total_tests_run"]
        fair[category]["passed"] += check["total_passed_tests"]

    for category in fair:
        scores[category] = fair[category]["passed"] / fair[category]["tests"] if fair[category]["tests"] > 0 else 0
    return scores


def call_foops_and_save_results(ontology_uri, output_path):
    """
    Call FOOPS API and save the results in output_path
    """
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    payload = {
        "ontologyUri": ontology_uri
    }

    response = requests.post(FOOPS_URL, headers=headers, json=payload, timeout=60 * 3)
    response.raise_for_status()  # Raises an exception for HTTP errors
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"Results saved to {output_path}")


def check_fair_for_ontologies(target_repo, branch, changed_files, base_dir):
    """
    :param target_repo:
    :param changed_files:
    :param base_dir:
    :return:
    """
    for f in changed_files:
        gen_fair_for_ontology(base_dir, target_repo, branch, f)


def gen_fair_for_ontology(base_dir, target_repo, branch, ontology_rel_dir):
    report_output_dir = os.path.join(base_dir, get_target_home(), ontology_rel_dir, tools_conf['foops']['folder_name'])
    dolog("report output dir: %s" % report_output_dir)
    build_path_all(report_output_dir)
    dolog("path is built")
    results_file_dir = os.path.join(report_output_dir, "data.json")
    scores_file_dir = os.path.join(report_output_dir, tools_conf['foops']['scores_file_name'])
    ontology_public_url = get_ontology_github_url(repo=target_repo, branch=branch, ontology=ontology_rel_dir)
    call_foops_and_save_results(ontology_uri=ontology_public_url, output_path=results_file_dir)
    save_foops_scores(data_path=results_file_dir, output_path=scores_file_dir)
