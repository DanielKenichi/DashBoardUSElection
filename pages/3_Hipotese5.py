from dataset import get_dataset
from streamlib import st

df_Hip5 = get_dataset().groupby('state')[['2020 Democrat vote %','2020 Republican vote % ','2020 other vote %','Hispanic or Latino percentage','NH-White percentage','NH-Black percentage','NH-American Indian and Alaska Native percentage','NH-Asian percentage','NH-Native Hawaiian and Other Pacific Islander percentage','NH-Some Other Race percentage']]

df_Hip5.head()