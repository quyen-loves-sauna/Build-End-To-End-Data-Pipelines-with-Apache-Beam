delivered_table_spec = "southern-flash-422709:dataset_food_orders.delivered_orders"
other_table_spec = "southern-flash-422709:dataset_food_orders.other_status_orders"

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import argparse
from google.cloud import bigquery

parser = argparse.ArgumentParser()
parser.add_argument('--input',
                                       dest = 'input',
                                       required=True,
                                       help='Input file to process')

path_args, pipeline_args = parser.parse_known_args()

inputs_pattern = path_args.input

options = PipelineOptions(pipeline_args)

p = beam.Pipeline(options = options)

def remove_last_colon(row):
    cols = row.split(', ')
    item = str(cols[4])

    if item.endswith(':'):
        cols[4] = item[:-1]
    return ','.join(cols)

def remove_special_characters(row):
    import re
    cols = row.split(',')
    ret = ''
    for col in cols:
        clean_col = re.sub(r'[?%&]', '', col)
        ret = ret + clean_col + ','
    ret = ret[:-1]
    return ret

def print_row(row):
    print_row()


cleaned_data = (
   p
   | beam.io.ReadFromText(inputs_pattern, skip_header_lines=1)
   | beam.Map(remove_last_colon)
   | beam.Map(lambda row: row.lower())
   | beam.Map(remove_special_characters)
   | beam.Map(lambda  row: row+',1')
   )

delivered_orders = (
    cleaned_data
    | 'delivered filter' >>  beam.Filter(lambda row: row.split(',')[8].lower() == 'delivered')
)

other_orders = (
    cleaned_data
    | 'Undelivered filter' >> beam.Filter(lambda row: row.split(',')[8].lower() != 'delivered')
)

(cleaned_data
 | 'count total' >> beam.combiners.Count.Globally()
 | 'total map'   >> beam.Map(lambda x: 'Total count:' +str(x))
 | 'print total' >>  beam.Map(print_row)
 )

(delivered_orders
 | 'count delivered' >> beam.combiners.Count.Globally()
 | 'delivered map'   >> beam.Map(lambda x: 'Delivered count:' +str(x))
 | 'print delivered count' >>  beam.Map(print_row)
)

(other_orders
 | 'count others' >> beam.combiners.Count.Globally()
 | 'other map'   >> beam.Map(lambda x: 'Others count:' +str(x))
 | 'print undelivered' >>  beam.Map(print_row)
 )

client = bigquery.Client()

dataset_id = '{}.dataset_for_order'.format(client.project)

try:
    client.get_dataset(dataset_id)
    
except:
    dataset = bigquery.Dataset(dataset_id)

    dataset.location = 'US'
    dataset.description = 'data set for food orders'

    dataset_ref = client.create_dataset(dataset, timeout=30)

def to_json(csv_str):
    fields = csv_str.split(',')

    json_str = {"customer_id":fields[0],
                "date": fields[1],
                "timestamp": fields[2],
                "order_id": fields[3],
                "items": fields[4],
                "amount": fields[5],
                "mode": fields[6],
                "restaurant": fields[7],
                "status": fields[8],
                "ratings": fields[9],
                "feedback": fields[10],
                "new_col": fields[11]}
    return json_str

table_schema = 'customer_id:STRING, date: STRING, timestamp: STRING, order_id: STRING, \
items: STRING, amount: STRING, mode: STRING, restaurant: STRING, status: STRING, \
ratings: STRING, feedback: STRING, new_col: STRING'

(delivered_orders
    | 'delivered to json' >> beam.Map(to_json)
    | 'write delivered' >>  beam.io.WriteToBigQuery(
     delivered_table_spec,
     schema=table_schema,
     create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
     write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
     additional_bq_parameters={'timePartitioning': {'type': 'DAY'}}
     )
)


(other_orders
    | 'delivered to json' >> beam.Map(to_json)
    | 'write delivered' >>  beam.io.WriteToBigQuery(
     other_table_spec,
     schema=table_schema,
     create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
     write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
     additional_bq_parameters={'timePartitioning': {'type': 'DAY'}}
     )
)

from apache_beam.runners.runner import  PipelineState
ret = p.run()
if ret.state == PipelineState.DONE:
    print('Success!!!')
else:
    print('Error Running beam Pipeline')

view_name = 'daily_food_orders'
dataset_ref = client.dataset('dataset_food_orders_latest')
view_ref = dataset_ref.table(view_name)
view_to_create = bigquery.Table(view_ref)

view_to_create.view_query = 'select * from southern-flash-422709.dataset_food_orders.delivered_orders where _PARTITIONDATE = DATE(current_date())'
view_to_create.view_use_legacy_sql = False

try:
    client.create_table(view_to_create)
except:
    print ('View already exists')