import pandas as pd
import re
from copy import copy

from raspberry_awards.models import Nomination

def read_nominations(filepath='movielist.csv'):
  df = pd.read_csv(filepath,sep=';')
  row_iter = df.iterrows()
  objs = [
    Nomination(
    	title=row['title'],
    	year=row['year'],
    	producers=row['producers'],
    	studios=row['studios'],
    	winner=(row['winner']=='yes')
    )
    for index, row in row_iter
  ]
  nominations = []
  for obj in objs:
    producers = [p.strip() for p in re.split(',|and ', obj.producers)]
    for producer in producers:
    	if len(producer) > 0:
      	    n = copy(obj)
      	    n.producers = producer
      	    nominations.append(n)

  Nomination.objects.all().delete()
  Nomination.objects.bulk_create(nominations)

