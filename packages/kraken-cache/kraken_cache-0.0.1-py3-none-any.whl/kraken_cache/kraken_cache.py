
import datetime
import sys
from datetime import timedelta

class Kraken_cache:

    def __init__(self, expiry = 600, max = 100000):

        '''
        db_value
        db_date: last time it loaded the data
        
        new_value
        new_date: last time it set the data

        last_get_date

        read_count

        '''

        self.struc = ['db_value', 'db_date', 'new_value', 'new_date', 'last_get_date', 'read_count']

        # List of items stored in cache
        self.items = {}

        # Defines time limit and number of record limit before triggering clean-up
        self.expiry = expiry
        self.max = max
        self.last_run = datetime.datetime.now()

        # Monitors number of transactions, clean-up everytime hits trigger
        self.trans = 0
        self.trans_trigger = self.max / 20


    def get(self, record_id):

        self.prune()

        self._init_item(record_id)

        # Increment count and last read time
        self.items[record_id]['last_get_date'] = datetime.datetime.now()

        self.items[record_id]['read_count'] += 1


        # Get new and db value, assumes new is better if exist
        new_value = self.items[record_id]['new_value']

        db_value = self.items[record_id]['db_value']

        if new_value:
            return new_value

        if db_value:
            return db_value

        return None


    def _set_new_date(self, record_id):

        self.items[record_id]['new_date'] = datetime.datetime.now()
        self.items[record_id]['last_get_date'] = datetime.datetime.now()


    def _set_db_date(self, record_id):

        self.items[record_id]['db_date'] = datetime.datetime.now()
        self.items[record_id]['last_get_date'] = datetime.datetime.now()

    def _set_last_run(self, record_id):

        self.last_run = datetime.datetime.now()


    def set(self, record_id, item):
        # Set data to write to db

        self.prune()

        self._init_item(record_id)

        # Store item in cache
        self.items[record_id]['new_value'] = item

        # Resets 
        self._set_new_date(record_id)



    def load(self, record_id, item):
        # Load data to cache from db

        self.prune()

        self._init_item(record_id)

        self.items[record_id]['db_value'] = item
        
        # Resets 
        self._set_db_date(record_id)

        return



    def get_new(self):

        # returns list of records that has been changed

        records = []
        for record_id in self.items:
            new_value = self.items[record_id]['new_value']

            if new_value:
                records.append(new_value)

        return records



    def clear(self, record_id):

        # Assumes all outstanding data has been writtened to db, resets

        new_value = self.items[record_id]['new_value']

        self.items[record_id]['db_value'] = new_value

        self.items[record_id]['new_value'] = None

        # Resets 
        self._set_new_date(record_id)
        self._set_db_date(record_id)

        self.prune()



    def clear_all(self):

        for record_id in self.items:
            self.clear(record_id)

        self.prune()


        return


    def search(self, key, expr):

        records = []

        for record_id in self.items:

            value = self.items[record_id]['new_value'].get(key, None)

            if value == expr:
                records.append(self.items[record_id]['new_value'])
                continue

            value = self.items[record_id]['db_value'].get(key, None)

            if value == expr:
                records.append(self.items[record_id]['db_value'])
                continue

        return records


    @property
    def size(self):

        size=sys.getsizeof(self)  

        return size


    def prune(self):

        # Increment # transactions
        self.trans += 1

        # Cancels if ahaven't reached trigger
        if self.trans < self.trans_trigger:
            return
        
        # Reset and run clean-up
        self.trans = 0

        self.prune_old()
        self.prune_number()


    def prune_number(self):

        # Removes oldest saved and accessed items 

        # Calculate number of items to delete
        items_to_delete = len(self.items) - self.max

        if items_to_delete < 0:
            return


        # Get list of items without new value
        recs = []

        for i in self.items:

            if not self.items[i].get('new_value', None):

                last_date = self.items[i].get('last_get_date', None)

                if not last_date:
                    last_date = datetime.datetime.fromisoformat('1970-01-01')

                rec = {
                    'date': last_date,
                    'id': i
                }

                recs.append(rec)

        # Sort items 
        new_recs = sorted(recs, key=lambda k: k['date']) 


        # Delete items
        count = 0
        for i in new_recs:
            if count >= items_to_delete:
                break
            self.items.pop(i['id'])
            count += 1


        return


    def prune_old(self):


        # Skip if it ran not too long ago

        delta_max =  timedelta(seconds = self.expiry/10)

        delta_actual = datetime.datetime.now() - self.last_run

        if delta_actual < delta_max:
            return

        self._set_last_run()


        # Deletes saved items oder than seconds

        to_delete = []

        for i in self.items:

            if not self.items[i].get('new_value', None):
                
                null_date = datetime.datetime.fromisoformat('1980-01-01')

                last_date = self.items[i].get('last_get_date', None)

                if not last_date:
                    last_date = null_date

                delta_max = timedelta(seconds = self.expiry)

                delta_actual = datetime.datetime.now() - last_date

                if delta_actual > delta_max:
                    to_delete.append(i)

        for i in to_delete:
            self.items.pop(i)

        return


    def _init_item(self, record_id):

        if not self.items.get(record_id, None):
            self.items[record_id] = {}


        for i in self.struc:
            if not self.items[record_id].get(i, None):
                self.items[record_id][i] = None

        if not self.items[record_id]['read_count']:
            self.items[record_id]['read_count'] = 0