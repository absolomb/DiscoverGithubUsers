from github import Github
import pdb
import argparse
import sys

def print_banner():
    banner = """
  ____  _                                ____ _ _   _           _       _   _                   
 |  _ \(_)___  ___ _____   _____ _ __   / ___(_) |_| |__  _   _| |__   | | | |___  ___ _ __ ___ 
 | | | | / __|/ __/ _ \ \ / / _ \ '__| | |  _| | __| '_ \| | | | '_ \  | | | / __|/ _ \ '__/ __|
 | |_| | \__ \ (_| (_) \ V /  __/ |    | |_| | | |_| | | | |_| | |_) | | |_| \__ \  __/ |  \__ \\
 |____/|_|___/\___\___/ \_/ \___|_|     \____|_|\__|_| |_|\__,_|_.__/   \___/|___/\___|_|  |___/
 v0.2
 """
    print(banner)

# find users based off the search keyword
def find_keyword_users(g):
    
    print()
    print("======================================================")
    print("    Gathering Users with Keyword: " + keyword)
    print("======================================================")
    print()
    users=g.search_users(str(keyword))
    print("[+] Total users discovered with keyword '"+ keyword +"': " + str(users.totalCount))
    return users

# get the organization and try to list any public members
# usually not a ton of results here since this is generally private info
def find_org_users(g, orgname):
    
    print_header("Gathering Organizational Information")
    
    if orgname is not None:
        print("[*] Getting organization with username: " + orgname)
        
        try:
            org = g.get_organization(orgname)
        
        except Exception as e:
            print("[-] No organization found with name: " + orgname)
            return None, None

    else:
        print("[*] Organization name not specified, getting organization username with keyword: " + keyword)
        
        try:
            org = g.get_organization(keyword)
        
        except Exception as e:
            print("[-] No organization discovered with keyword: " + keyword)
            return None, None

    if org:
        print("[+] Organization Discovered!")
        print()
        print("    Name: " + org.name)
        print("    Login: " + org.login)
        print()
        users = org.get_public_members()
        print("[+] Total public users discovered in organization '"+ org.name +"': " + str(users.totalCount))

        if users:
            for user in users:
                print("    " + user.login)

        return users, org

# filter results from basic keyword search to reduce false positives
def filter_users(users):

    filtered_users = []
    print("[*] Filtering users further to reduce false positives")
    
    try:
        for user in users:

            if user.company is not None and keyword.lower() in user.company.lower():
                print("[+] " + user.login + " has " + keyword + " in company field!")
                print("    Company: " + user.company)
                print()
                filtered_users.append(user)
                continue
            
            elif user.email is not None and domain.lower() in user.email.lower():
                print("[+] " + user.login + " has " + domain + " in email field!")
                print("    Email: " + user.email)
                print()
                filtered_users.append(user)
                continue
            
            elif user.blog is not None and domain.lower() in user.blog.lower():
                print("[+] " + user.login + " has " + domain + " in blog field!")
                print("    Blog: " + user.blog)
                print()
                filtered_users.append(user)
                continue
            
            elif user.bio is not None and keyword.lower() in user.bio.lower():
                print("[+] " + user.login + " has " + keyword + " in bio field!")
                bio = user.bio.replace('\r\n', '')
                print("    Bio: " + bio)
                print()
                filtered_users.append(user)
                continue
    # if an exception gets hit here, it's probably due to API limits without a token
    except Exception as e:
        print(e)
    
    print()
    print("[+] Total filtered users discovered: " + str(len(filtered_users)))
    write_usernames(filtered_users, "filtered users", False)
    return filtered_users

# prints repos for discovered organization
def get_org_repos(org):

    print_header("Gathering Organization Repositories ")
    print("[*] Listing organization repositories")
    print("[+] Username: " + org.login)
    repos = org.get_repos()
    print("[*] Number of repositories: " + str(repos.totalCount))
    print()

    for repo in repos:
        
        if giturls:
            print("[+] " + repo.clone_url)
            output_repos.add(repo.clone_url)
        else:
            print("[+] " + repo.html_url)
            output_repos.add(repo.html_url)
        if repo.fork == False:
            
            try:
                contribs = repo.get_contributors()
                if contribs.totalCount > 0:
                    print("[*] Non-forked repository, listing " + str(contribs.totalCount) +" contributors:")
                    print()
                    for contrib in contribs:
                        print("      " + contrib.login)
                        contributors.add(contrib)
                    print()

            except Exception as e:
                print("[!] " + str(e))
                continue
            
    print()
    print("[+] Total organizational contributors discovered: " + str(len(contributors)))
    write_usernames(contributors, "contributors", False)

# prints repos for all users discovered
def get_user_repos(users):
    
    for user in users:
        print()
        print("[+] Username: " + user.login)
        repos = user.get_repos()
        print("[*] Number of repositories: " + str(repos.totalCount))
        
        if repos.totalCount < 50:
            print()
            for repo in repos:
                if giturls:
                    print("    " + repo.clone_url)
                    output_repos.add(repo.clone_url)
                else:
                    print("    " + repo.html_url)
                    output_repos.add(repo.html_url)
        else:
            for repo in repos:
                if giturls:
                    output_repos.add(repo.clone_url)
                else:
                    output_repos.add(repo.html_url)


def write_output(repos):
    
    filename = "repos.txt"
    print("\n[*] Writing " + str(len(repos)) + " repos to " + filename)
    # convert to a list so we can sort the output
    repo_list = list(repos)
    repo_list.sort()
    with open(filename, 'a') as repo_file:
        for repo in repo_list:
            repo_file.write("%s\n" % repo)

def write_usernames(users, name, flag):
    
    filename = name + ".txt"
    if flag:
        print("\n[*] Writing " + str(users.totalCount) + " " + name + " to " + filename)
        print()
    else:
        print("\n[*] Writing " + str(len(users)) + " " + name + " to " + filename)
        print()

    with open(filename, 'a') as user_file:
        for user in users:
            user_file.write("%s\n" % user.login)

def print_header(header_string):

    print()
    print("======================================================")
    print("    " + header_string)
    print("======================================================")
    print()

def main():

    print_banner()

    parser = argparse.ArgumentParser(description='Github Search Arguments.')
    parser.add_argument('-k', metavar="keyword", help="Keyword to search i.e. company name", type=str)
    parser.add_argument('-d', metavar="domain", help="Company domain name to search i.e company.com", type=str)
    parser.add_argument('-t', metavar="token", help="Github Personal Access Token", type=str)
    parser.add_argument('-g', help="Output cloneable git URLs", action='store_true')
    parser.add_argument('-o', metavar="organization", help="Github Organization name (if different than keyword specified)", type=str)
    parser.add_argument('--no_filter', help="Don't filter to reduce false positives and return all results", action='store_true')

    args = parser.parse_args()
    if len(sys.argv) == 1:
            parser.print_help()

    global domain
    global keyword
    global output_repos
    global giturls
    global contributors

    # using a set here to prevent duplicate repo values
    output_repos = set()
    contributors = set()
    token = args.t
    domain = args.d 
    keyword = args.k
    org = args.o
    nofilter = args.no_filter
    giturls = args.g


    if not domain or not keyword:
        print("[!] You must specify both a keyword with -k and a domain with -d")
        exit()
    
    # create a Github instance without an access token (not recommended)
    if not token:
        print("[!] Warning queries may be limited and results incomplete without a Github Personal Access Token!")
        g = Github()
    # create a Github instance using an access token
    else:
        g = Github(token)


    org_users, org_object = find_org_users(g, org)

    if org_object:
        get_org_repos(org_object)

    if org_users.totalCount > 0:
        print_header("Gathering Organization Member Repositories")
        get_user_repos(org_users)

    if len(contributors) > 0:
        print_header("Gathering Contributor Repositories")
        get_user_repos(contributors)

    search_users = find_keyword_users(g)
    
    if nofilter:
        write_usernames(search_users, "non-filtered users", True)
        print("[*] Gathering results without filtering, this could result in lots of noise and false positives!")
        print_header("Gathering Non-filtered User Repositories")
        get_user_repos(search_users)
    else:
        filtered = filter_users(search_users)
        print_header("Gathering Filtered User Repositories")
        get_user_repos(filtered)
    

    write_output(output_repos)

if __name__ == "__main__":
    main()
