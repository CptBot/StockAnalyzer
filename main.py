import copy
import os
import pdfplumber
import re
import depot.comdirect as dc
import depot.tradeRepublic as dt


BUYS = "buy"

dirpath = 'Z:\\GAR\\attachments'
data = {BUYS: []}
mylist = []
for entry in os.listdir(dirpath):
    filepath = os.path.join(dirpath, entry)
    if os.path.isfile(filepath) and entry.endswith('.pdf'):
        print(entry)
        with pdfplumber.open(filepath) as f:
            if f.metadata.get('Title') == 'Trade Report':
                # bar = dt.analyze(f)
                # mylist.append(copy.deepcopy(bar))
                data[BUYS].append(dt.analyze(f))
                continue
            # for line in text.split('\n'):
            #     if line.lower().__contains__('comdirect'):
            #         dc.analyze(f)
            #         break
            #     if line.lower().__contains__('trade republic'):
            #         dt.analyze(f)
            #         break
                # else:
                #     line2 = re.sub(r"\s+", "", line)
                    # print('no ISIN: ' + line2)

