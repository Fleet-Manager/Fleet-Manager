import csv
import pdb
import datetime
from io import TextIOWrapper
from .models import DataSet, CartFleet, Cart, DataCollection, Fault

def parse_file(fileList, selected_fleet):
    DataCollection.objects.create(name=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for i in fileList:
        file = fileList[i]
        fp = TextIOWrapper(file.open(), encoding='utf-8')
        fp.seek(0)
        content = list(csv.DictReader(fp, delimiter = ',', fieldnames=['time','MCU','number','model name','amp hour','battery volts','hours','miles'], restkey='extrafields'))
        x = 0
        for row in content:
            f = CartFleet.objects.filter(name=selected_fleet)
            c = Cart.objects.create(number=row['number'],cart_fleet=f[0])
            if x == 0:
                DataCol = DataCollection.objects.create(name=row['time'])
            d = DataSet.objects.create(collection=DataCol,collection_date=datetime.datetime.now(),amp_hours=row['amp hour'],mileage=row['miles'],hours=row['hours'],cart=c)
            for column in range(6, len(row['extrafields']), 19):
                if (row['extrafields'][column] != 0):
                    Fault.objects.create(code=row['extrafields'][column],hour=row['extrafields'][column + 2],cart=c)
                else: break
            x = x + 1
            #pdb.set_trace() fieldnames=['time','MCU','serial','number','model name','amp hour','battery volts','hours','miles','mode','status','MCU version','previous mode','prev. mode hour']
