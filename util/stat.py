import sys
import gzip


def is_publish(line):
    return 'GET /profile?repo=' in line and '&name=' in line


def is_bundle(line):
    return 'GET /get_bundle?repo=' in line


def is_api(line):
    return ' /api' in line


def is_update_conf(line):
    return 'POST /update_conf' in line


def is_access_published_docs(line):
    ext = ['.js', '.css', '.png']
    result = False
    if 'GET /publish' in line and '.html' in line and 'index' in line and (line.count('.html') == 1 or line.count('.html') == line.count('.index')):
        for e in ext:
            if e in line:
                return False
        result = True
    return result


def is_content_negotiation(line):
    return 'GET /publish' in line and ('.xml' in line or '.nt' in line or '.ttl' in line)


def perform_stat_count(line, curr_stat_count):
    stat_count = curr_stat_count
    if is_publish(line):
        stat_count['publish'] += 1
    if is_bundle(line):
        stat_count['bundle'] += 1
    if is_api(line):
        stat_count['api'] += 1
    if is_update_conf(line):
        stat_count['update_conf'] += 1
    if is_access_published_docs(line):
        stat_count['doc_access_published'] += 1
    if is_content_negotiation(line):
        # print line
        stat_count['content_negotiation'] += 1
    return stat_count


def parse_text_file(file_name, curr_stat_count):
    #print "parse text file: "+file_name
    f = open(file_name, 'r')
    stat_count = curr_stat_count
    for line in f.readlines():
        stat_count = perform_stat_count(line, stat_count)
    #print stat_count
    return stat_count


def parse_gz_file(file_name, curr_stat_count):
    #print "parse gz file: "+file_name
    f = gzip.open(file_name, 'rb')
    stat_count = curr_stat_count
    for line in f.readlines():
        stat_count = perform_stat_count(line, stat_count)
    #print stat_count
    return stat_count


def parse_files(files):
    stat_count = {
        'publish': 0,
        'bundle': 0,
        'api': 0,
        'update_conf': 0,
        'doc_access_published': 0,
        'content_negotiation': 0,
    }
    for f in files:
        if f[-3:] == '.gz':
            stat_count = parse_gz_file(file_name=f, curr_stat_count=stat_count)
        else:
            stat_count = parse_text_file(file_name=f, curr_stat_count=stat_count)
    print "\nfinal: "
    print stat_count


###################################################################################################
#                           Per repo stats                                                        #
###################################################################################################

def get_text_text_file(f):
    return open(f, 'r').read()


def get_text_gz_file(f):
    return gzip.open(f, 'rb').read()


def get_publish_repo(line):
    if is_publish(line):
        # return line.split("profile?repo=")[1].split(' ')[0]
        return line.split("profile?repo=")[1].split(' ')[0].split('&')[0]
    else:
        return None


def get_bundle_repo(line):
    if is_bundle(line):
        return line.split('GET /get_bundle?repo=')[1].split(' ')[0].split('&')[0]
    else:
        return None


def stat_per_repo(files):
    repos_stat = {}
    for f in files:
        if f[-3:] == '.gz':
            text = get_text_gz_file(f)
        else:
            text = get_text_text_file(f)
        for line in text.split('\n'):
            repo = get_publish_repo(line)
            if repo is not None:
                if repo in repos_stat:
                    repos_stat[repo]['publish'] += 1
                else:
                    repos_stat[repo] = {'publish': 1, 'bundle': 0}
            repo = get_bundle_repo(line)
            if repo is not None:
                if repo in repos_stat:
                    repos_stat[repo]['bundle'] += 1
                else:
                    repos_stat[repo] = {'publish': 0, 'bundle': 1}
    sum_all = {'publish': 0, 'bundle': 0}
    for k in repos_stat:
        print "%60s => %s" % (k, str(repos_stat[k]))
        sum_all['publish'] += repos_stat[k]['publish']
        sum_all['bundle'] += repos_stat[k]['bundle']
    #print repos_stat
    print sum_all
    return repos_stat


def main():
    help_string = """
        python stat.py all FILES
        python stat.py repo FILES
    """
    print len(sys.argv)
    if len(sys.argv) < 3:
        print help_string
        return
    if sys.argv[1] == "all":
        files = sys.argv[2:]
        print files
        parse_files(files)
    elif sys.argv[1] == "repo":
        files = sys.argv[2:]
        print files
        stat_per_repo(files)
    else:
        print help_string

if __name__ == "__main__":
    main()











