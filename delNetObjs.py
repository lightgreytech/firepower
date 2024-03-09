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
    # call the token generating function and populate our header
    header = token.get_token(ip, path, u, p)

    # we need to update our path to account for the domain UUID and Object_ID as follows
    path = f"/api/fmc_config/v1/domain/{header['DOMAIN_UUID']}/object/networks/005056BF-7B88-0ed3-0000-012885446194"
    
    
    # now to try and DELETE our network from the list of network objects
    try:
        r = requests.delete(f"https://{ip}/{path}", headers=header, verify=False)

        print(r.request.body)
        print("Headers: " + str(r.headers) + "\n")
        print("Text: " + str(r.text) + "\n")
        print("Status Code: " + str(r.status_code))

    except requests.exceptions.HTTPError as errh:
        raise SystemExit(errh)
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)