import pandas as pd
import re
from copy import copy

from django.db import transaction

from raspberry_awards.models import Nomination


@transaction.atomic
def read_nominations(filepath):
  df = pd.read_csv(filepath,sep=';')
  row_iter = df.iterrows()
  objs = [
    Nomination(
    	title=row['title'],
    	year=row['year'],
    	producers=row['producers'],
    	studios=row['studios'],
    	winner=(str(row['winner']).strip()=='yes')
    )
    for index, row in row_iter
  ]

  Nomination.objects.all().delete()
  Nomination.objects.bulk_create(objs)

