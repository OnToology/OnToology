import rdflib
from Integrator import dolog

# format_extension_mapping = {
#     'rdf': 'xml',
#     'owl': 'xml',
#     'ttl': 'ttl'
# }
#
#
# def valid_syntax(file_abs_dir):
#     g = rdflib.Graph()
#     try:
#         g.parse(file_abs_dir, format=format_extension_mapping[file_abs_dir[-3:].lower()])
#         return True
#     except Exception as e:
#         dolog("syntax error for the file %s" % str(file_abs_dir))
#         dolog("syntax error: "+str(e))
#     return False

formats = ['xml', 'ttl']


def valid_syntax(file_abs_dir):
    g = rdflib.Graph()
    for a_format in formats:
        try:
            g.parse(file_abs_dir, format=a_format)
            print("correct syntax %s" % a_format)
            return True
        except Exception as e:
            print("syntax error for the file %s format %s" % (str(file_abs_dir), a_format))
            print(str(e))
            dolog("syntax error for the file %s format %s" % (str(file_abs_dir), a_format))
            dolog("syntax error: "+str(e))
    return False
