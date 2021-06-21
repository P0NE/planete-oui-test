#!/bin/env python3

import argparse
import sys

from planete_oui_app.clients.barnsley import Barnsley
from planete_oui_app.clients.hawes import Hawes
from planete_oui_app.clients.hounslow import Hounslow

#Create agruments parser
parser = argparse.ArgumentParser()
parser.add_argument(
    "--from_date",
    "-f",
    type=str,
    default="16-06-2021",
    help="Start date (format: MM-DD-YYYY)",
)

parser.add_argument(
    "--to_date",
    "-t",
    type=str,
    default="17-06-2021",
    help="End date (format: MM-DD-YYYY)",
)

parser.add_argument(
    "--format",
    "-o",
    type=str,
    default="json",
    help="Output format",
)

args = parser.parse_args()

#Verify output format argument
if args.format not in ['json', 'csv']:
    print ("Erreur outpout format, must been csv or json")
    sys.exit()
    
#Call API Client and create dataframe array
hawes = Hawes(args.from_date, args.to_date).call()
barnsley = Barnsley(args.from_date, args.to_date).call()
hounslow = Hounslow(args.from_date, args.to_date).call()
all_responses = [hawes, barnsley, hounslow]

#Merge the response dataframes
dfs = all_responses[0]
for df in all_responses[1:]:
    dfs = dfs.append(df, ignore_index=True)

#1: Groupby by start and end date
#2: Sum the group by values 
result_data = dfs.groupby(['start', 'end']).sum().reset_index()

#Create the output result format wanted
if args.format == 'json':
    print (result_data.to_json(orient='records'))
else:
    print (result_data.to_csv(index=False))


