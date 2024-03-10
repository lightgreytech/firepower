#!/usr/bin/python3
"""
File: getNetObjs.py
Inputs: 
    Username
    Password
    FMC IP Address
Outputs: 
    a list of network objects printed to screen

To use this file as a standalone script, the username, password, & FMC IP
will need to be passed in as command-line arguments.
"""

# include the necessary modules
import argparse
import json
import os
import requests
import requestToken as token



# if we're using this as a stand-alone script, run the following
if __name__ == "__main__":
    # first set up the command line arguments and parse them
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("username", type=str, help ="API username")
    parser.add_argument("password", type=str, help="password of API user")
    parser.add_argument("ip_address", type=str, help="IP of FMC")
    args = parser.parse_args()

    # set needed variables to generate a token
    u = args.username
    p = args.password
    ip = args.ip_address
    path = "/api/fmc_platform/v1/auth/generatetoken"
    header = {} # don't need to instantiate this here, but doing so for clarity

    # call the token generating function and populate our header
    header = token.get_token(ip, path, u, p)

    # # we need to update our path to account for the domain UUID as follows
    # Next line gets the first 25 objects (its the default for FMC)
    path = f"/api/fmc_config/v1/domain/{header['DOMAIN_UUID']}/object/networks"
    # #FILTER: Get the first 100 OBJECTS
    # path = f"/api/fmc_config/v1/domain/{header['DOMAIN_UUID']}/object/networks?offset=0&limit=100"
    # now to try and GET our list of network objects
    try:
        r = requests.get(f"https://{ip}/{path}", headers=header, 
            verify=False) # always verify the SSL cert in prod!
    except requests.exceptions.HTTPError as errh:
        raise SystemExit(errh)
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

    # if it worked, we will have received a list of network objects!
    #output the result to a file in a different folder
    output_path = './outputs/'
    try:
        if not os.path.exists(output_path): #
            os.mkdir(output_path)
        with open('outputs/getNetObjs.txt', 'w') as f:
            print(json.dumps(r.json(), indent=2), file=f)
            # print(json.dumps(r.json(r), indent=2))
    except Exception as err:
        raise SystemExit(err)