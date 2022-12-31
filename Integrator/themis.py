from collections import Counter
import rdflib
from rdflib.namespace import RDF, OWL
import requests
import traceback
import os
from . import dolog, tools_conf, build_path_all, get_target_home, log_file_dir, g

THEMIS_URL = "http://themis.linkeddata.es/rest/api/"


def get_themis_results(ontology_url, tests):
    """
    :param ontology_url:
    :param tests:
    :return:
    """
    results_url = THEMIS_URL + 'results'
    j = {
        'ontologies': [ontology_url], 'tests': tests
    }
    r = requests.post(results_url, json=j)
    if r.status_code == 200:
        dolog("Themis APIs is a success for <%s>" % ontology_url)
        raw_results = r.json()
        print(raw_results)
        # num_of_passed = 0
        # parsed_results = []
        # for r in test_results:
        #     parsed_results.append(r['Results'][0]['Result'])
        # c = Counter(parsed_results)
        test_result_pairs = []
        stats = []
        for r in raw_results:
            p = (r['Test'], r['Results'][0]['Result'])
            stats.append(r['Results'][0]['Result'])
            print(p)
            test_result_pairs.append(p)
        c = Counter(stats)
        print(c)
        return test_result_pairs
    else:
        dolog("Error in calling Themis for ontology: <%s>" % ontology_url)
        dolog("API response: ")
        dolog(r.response)
        return None


def generate_test_class_type(gg):
    """
    :param gg: rdflib graph
    :return:
    """
    classes_set = set()
    try:
        # for rdf_type, _ in g.subject_objects(predicate=RDF.type):
        # for _, rdf_type in g.subject_objects(predicate=RDFS.Class):
        for rdf_type in gg.subjects(predicate=RDF.type, object=OWL.Class):
            classes_set.add(rdf_type)
        tests = []
        for c in classes_set:
            t = "%s type Class" % c
            print(t)
            tests.append(t)
        return tests
    except Exception as e:
        dolog("error in generating themis class_type tests")
        dolog(str(e))


def generate_tests(file_abs_dir):
    """
    :param file_abs_dir: the ontology absolute directory
    :return: list of tests (or [] in the case of an error)
    """
    gg = rdflib.Graph()
    formats = ['xml', 'ttl']
    for a_format in formats:
        try:
            gg.parse(file_abs_dir, format=a_format)
            tests = generate_test_class_type(gg)
            print("tests: ")
            print(tests)
            return tests
        except Exception as e:
            print("generate_tests> Exception: " + str(e))
            traceback.print_exc()
    return []


def validate_ontologies(target_repo, changed_files, base_dir):
    """
    :param target_repo:
    :param changed_files:
    :param base_dir:
    :return:
    """
    for f in changed_files:
        validate_ontology(base_dir, target_repo, f)


def validate_ontology(base_dir, target_repo, ontology_rel_dir):
    report_output_dir = os.path.join(base_dir, get_target_home(), ontology_rel_dir, tools_conf['themis']['folder_name'])
    dolog("report output dir: %s" % report_output_dir)
    build_path_all(report_output_dir)
    dolog("path is built")
    tests_file_dir = os.path.join(report_output_dir, tools_conf['themis']['tests_file_name'])
    results_file_dir = os.path.join(report_output_dir, tools_conf['themis']['results_file_name'])
    write_tests(os.path.join(base_dir, ontology_rel_dir), tests_file_dir)
    write_test_results(target_repo, ontology_rel_dir, tests_file_dir, results_file_dir)


def write_test_results(target_repo, ontology_rel_dir, tests_file_dir, results_file_dir):
    ontology_public_url = 'https://raw.githubusercontent.com/%s/master/%s' % (target_repo, ontology_rel_dir)
    f = open(tests_file_dir)
    tests_text = f.read()
    f.close()
    tests = tests_text.split('\n')
    tests_and_results = get_themis_results(ontology_public_url, tests)
    f = open(results_file_dir, 'w')
    for test_text, result_text in tests_and_results:
        line = "%s\t%s\n" % (test_text, result_text)
        f.write(line)
    f.close()


def write_tests(ontology_dir, tests_file_dir):
    """
    Write tests file if it does not exist
    :param ontology_dir: the absolute directory of the ontology
    :param tests_file_dir: the absolute directory of the test file
    :return: None
    """
    if os.path.exists(tests_file_dir):
        dolog("the themis file exists <%s> for the ontology <%s>" % (tests_file_dir, ontology_dir))
    else:
        dolog("the themis does not exist <%s> for the ontology <%s>" % (tests_file_dir, ontology_dir))
        tests = generate_tests(ontology_dir)
        f = open(tests_file_dir, 'w')
        for t in tests:
            f.write(t)
            f.write("\n")
        dolog("write themis tests file <%s> " % tests_file_dir)
        f.close()


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        generate_tests(argv[1])
    else:
        get_themis_results(argv[1], argv[2].split(';'))
