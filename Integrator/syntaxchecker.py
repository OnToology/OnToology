import rdflib
from Integrator import dolog

format_extension_mapping = {
    'rdf': 'xml',
    'owl': 'xml',
    'ttl': 'ttl'
}


def valid_syntax(file_abs_dir):
    g = rdflib.Graph()
    try:
        g.parse(file_abs_dir, format=format_extension_mapping[file_abs_dir[-3:].lower()])
        # print "correct syntax"
        return True
    except Exception as e:
        print "syntax error for the file %s" % str(file_abs_dir)
        print str(e)
        dolog("syntax error for the file %s" % str(file_abs_dir))
        dolog("syntax error: "+str(e))
    return False
