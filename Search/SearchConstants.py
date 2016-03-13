import sys
sys.path.insert(0, '../MongoCodes')

from VitalConstants import *

INVHEADCOLL = INVIDXCOLL + '_head'
INVBODYCOLL = INVIDXCOLL + '_body'
INVANCHORCOLL = INVIDXCOLL + '_anchor'

HEAD_WT = 0.33
BODY_WT = 0.33
ANCHOR_WT = 0.33