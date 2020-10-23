#!/usr/bin/python3
'''
General-class callsign generator (1x3 and 2x3)

Here is the list of callsigns we will NOT generate:
     1.  KA2AA-KA9ZZ, KC4AAA-KC4AAF, KC4USA-KC4USZ, KG4AA-KG4ZZ,
          KC6AA-KC6ZZ, KL9KAA- KL9KHZ, KX6AA-KX6ZZ;
        regex:
        [kK][aA][2-9][a-zA-Z]{2}\b|[kK][cC]4[aA][aA][a-fA-F]\b|[kK][cC]4[uU][sS][a-zA-Z]\b|[kK][gG]4[a-zA-Z]{2}\b|[kK][cC]6[a-zA-Z]{2}\b|[kK][lL]9[kK][a-hA-H][a-zA-Z]\b|[kK][xX]6[a-zA-Z]{2}\b

     2.  Any call sign having the letters SOS or QRA-QUZ as the suffix;
        regex:
        \d[sS][oO][sS]|\d[qQ][r-uR-U][a-zA-Z]

     3.  Any call sign having the letters AM-AZ as the prefix (these prefixes
          are assigned to other countries by the ITU);
        regex:
        [aA][m-zM-Z]\d

     4.  Any 2-by-3 format call sign having the letter X as the first letter of the suffix;
        regex:
        [a-zA-Z]{2}\d[xX][a-zA-Z]{2}

     5.  Any 2-by-3 format call sign having the letters AF, KF, NF, or WF as the prefix
          and the letters EMA as the suffix (U.S Government FEMA stations);
        regex:
        [aAkKnNwW][fF]\d[eE][mM][aA]

     6.  Any 2-by-3 format call sign having the letters AA-AL as the prefix;
        regex:
        [aA][a-lA-L]\d[a-zA-Z]{3}

     7.  Any 2-by-3 format call sign having the letters NA-NZ as the prefix;
        regex:
        [nN][a-zA-Z]\d[a-zA-Z]{3}

     8.  Any 2-by-3 format call sign having the letters WC, WK, WM, WR, or WT
          as the prefix (Group X call signs);
        regex:
        [wW][cCkKmMrRtT]\d[a-zA-Z]{3}

     9.  Any 2-by-3 format call sign having the letters KP, NP or WP as the prefix
          and the numeral 0, 6, 7, 8 or 9;

    10.  Any 2-by-2 format call sign having the letters KP, NP or WP as the prefix
          and the numeral 0, 6, 7, 8 or 9;

        regex:
        [kKnNwW][pP][06789](?:[a-zA-Z]){2,3}
'''

import io
import os
import re
import rstr
import shutil
import sys
import urllib.request

def sanitizeInput(inputs):
    # if there is more than one command line argument, exit
    if len(inputs) != 2:
        print('Usage: %s  URL of server containing callsigns list.' % inputs[0])
        sys.exit(1)
    # now that we know there is only one argument, save it as our url
    return inputs[1]

# function to download the latest callsigns text file
def get_list(url):
    # if the file doesn't exist, download it to callsigns.txt in the current directory
    if not os.path.exists('./callsigns.txt'):
        print('downloading callsigns.txt')
        file_name = "callsigns.txt"
        with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    else:
        pass

# function to generate the callsigns removing the invalid ones
def generate_callsigns():
    # first generate over 8000 matches
    callsigns = []
    for i in range(8000): #thanksVegeta
        callsign = (rstr.xeger(r'[AKNWaknw][a-zA-Z]{0,1}[0123456789][a-zA-Z]{3}')).upper()
        if callsign not in callsigns:
            callsigns.append(callsign)

    # then remove the invalid callsigns
    invalidCallsignRegex = [r'[kK][aA][2-9][a-zA-Z]{2}',
                            r'[kK][cC]4[aA][aA][a-fA-F]', 
                            r'[kK][cC]4[uU][sS][a-zA-Z]', 
                            r'[kK][gG]4[a-zA-Z]{2}', 
                            r'[kK][cC]6[a-zA-Z]{2}', 
                            r'[kK][lL]9[kK][a-hA-H][a-zA-Z]', 
                            r'[kK][xX]6[a-zA-Z]{2}', 
                            r'\d[sS][oO][sS]|\d[qQ][r-uR-U][a-zA-Z]', 
                            r'[aA][m-zM-Z]\d', 
                            r'[a-zA-Z]{2}\d[xX][a-zA-Z]{2}', 
                            r'[aAkKnNwW][fF]\d[eE][mM][aA]', 
                            r'[aA][a-lA-L]\d[a-zA-Z]{3}', 
                            r'[nN][a-zA-Z]\d[a-zA-Z]{3}', 
                            r'[wW][cCkKmMrRtT]\d[a-zA-Z]{3}', 
                            r'[kKnNwW][pP][06789](?:[a-zA-Z]){2,3}']

    invalidSigns = []
    for invalid in callsigns:
        for regex in invalidCallsignRegex:
            if re.match(regex, invalid):
                invalidSigns.append(invalid)

    print(invalidSigns)
    callsigns = list(set(callsigns) - set(invalidSigns))

    # finally return the list of valid vanity callsigns
    return callsigns

# function to perform the callsign comparo
def available_callsigns(callsigns):
    existingCallsignsFormatted = []
    # first read in and format callsigns.txt
    try:
        fp = open('./callsigns.txt')
        line = fp.readline()
        while line:
            existingCallsignsFormatted.append((line[7:]).rstrip())
            line = fp.readline()
    finally:
        fp.close()

    # then return our list using our generated callsigns minus the existing ones and return
    return list(set(callsigns) - set(existingCallsignsFormatted))


# if this script is called directly, run me!
if __name__ == '__main__':
    url = sanitizeInput(sys.argv)
    get_list(url)
    vanityCall = generate_callsigns()
    print(available_callsigns(vanityCall))