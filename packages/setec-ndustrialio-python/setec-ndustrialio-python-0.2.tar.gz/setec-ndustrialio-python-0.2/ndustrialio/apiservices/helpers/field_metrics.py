from datetime import timedelta, datetime
from scipy import stats
import time
from ndustrialio.apiservices import *
from ndustrialio.apiservices.feeds import FeedsService
import pytz


class FieldMetrics:

    def __init__(self, client_id, client_secret):
        self.feed_service = FeedsService(client_id, client_secret)

    '''
        Main helper method to get field data metrics over a period of time given a time range, an interval between those
        times, and a list of outputs and fields

        Parameters:
        -- start_time_datetime - Start time within the range of time you want metrics
        -- end_time_datetime - End time within the range of time you want metrics
        -- minute_interval - Number of minutes for your bucket size
        -- field_identification_list - List of fields you want to base your metrics on (list of hashmaps
                                        {'output_id': <output_id>,
                                         'field_human_name': <field_human_name>
                                         }

    '''
    def getBatchFieldDataMetrics(self, start_time_datetime, end_time_datetime, minute_interval, field_identification_list):

        if start_time_datetime > end_time_datetime:
            raise Exception('Start time must be less than end time')

        time_array = []
        value_array = []
        aggregate_batch_data = []
        data_request_map = {}
        request_count = 0
        MAX_BATCH_REQUESTS = 20

        num_bins, end_time_datetime = self.calculateNumberOfBinsAndEndTime(start_time_datetime, end_time_datetime, minute_interval)
        start_time_utc = get_epoch_time(start_time_datetime)
        end_time_utc = get_epoch_time(end_time_datetime)

        for field_identification in field_identification_list:

            if 'output_id' in field_identification:
                output_id = field_identification['output_id']
            else:
                raise Exception('output_id not included in field hashmap')
            if 'field_human_name' in field_identification:
                field_human_name = field_identification['field_human_name']
            else:
                raise Exception('field_human_name not included in field hashmap')

            key = "{}.{}".format(output_id, field_human_name)

            data_request = self.feed_service.getData(output_id=output_id,
                                field_human_name=field_human_name,
                                time_end=end_time_datetime,
                                time_start=start_time_datetime,
                                window=60,
                                limit=1000,
                                execute=False)

            data_request_map[key] = {'method': data_request.method(),
                                     'uri': str(data_request)}

            request_count += 1

            if request_count == MAX_BATCH_REQUESTS:
                batch_data = self.feed_service.execute(POST(uri='batch').body(data_request_map), execute=True)
                for key, value in batch_data.items():
                    aggregate_batch_data += value['body']['records']
                request_count = 0
                data_request_map = {}

        batch_data = self.feed_service.execute(POST(uri='batch').body(data_request_map), execute=True)
        for key, value in batch_data.items():
            aggregate_batch_data += value['body']['records']

        for record in aggregate_batch_data:

            timestamp_datetime = datetime.strptime(record['event_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
            timestamp_utc = get_epoch_time(timestamp_datetime.replace(tzinfo=pytz.utc))
            try:
                value_array.append(float(record['value']))
                time_array.append(timestamp_utc)
            except:
                print ('Bad value: {}'.format(record['value']))

        metrics_map = self.calculateMetrics(time_array, value_array, start_time_utc, end_time_utc, num_bins)

        return metrics_map


    '''
        Iterate over the given start and end times to calculate the number of bins we'll need given the
        desired minute interval
    '''
    def calculateNumberOfBinsAndEndTime(self, start_time_datetime, end_time_datetime, minute_interval):

        time_range_minutes = divmod((end_time_datetime - start_time_datetime).total_seconds(), 60)[0]
        interval_timedelta = timedelta(minutes=minute_interval)

        if minute_interval > time_range_minutes:
            raise Exception('Time interval should not be larger than the time range')

        num_bins = 0
        new_end_time_datetime = start_time_datetime

        while True:
            if (new_end_time_datetime + interval_timedelta) > end_time_datetime:
                break
            else:
                new_end_time_datetime += interval_timedelta
                num_bins += 1

        return num_bins, new_end_time_datetime

    '''
        Populate the final format of the bucket, which is a hashmap of datetime (UTC) -> value
    '''
    def populateFinalBucket(self, metric_tuple):
        bucket = {}
        for idx, edge in enumerate(metric_tuple[1][1:]):
            bucket[datetime.utcfromtimestamp(edge).replace(tzinfo=pytz.utc)] = metric_tuple[0][idx]
        return bucket

    '''
        Calculate the metrics we're trying to grab
    '''
    def calculateMetrics(self, time_array, value_array, start_time_utc, end_time_utc, num_bins):

        mean_metric_tuple = stats.binned_statistic(x=time_array,
                                                   values=value_array,
                                                   statistic='mean',
                                                   bins=num_bins,
                                                   range=[(start_time_utc, end_time_utc)])

        min_metric_tuple = stats.binned_statistic(x=time_array,
                                                  values=value_array,
                                                  statistic='min',
                                                  bins=num_bins,
                                                  range=[(start_time_utc, end_time_utc)])

        max_metric_tuple = stats.binned_statistic(x=time_array,
                                                  values=value_array,
                                                  statistic='max',
                                                  bins=num_bins,
                                                  range=[(start_time_utc, end_time_utc)])

        std_metric_tuple = stats.binned_statistic(x=time_array,
                                                  values=value_array,
                                                  statistic='std',
                                                  bins=num_bins,
                                                  range=[(start_time_utc, end_time_utc)])

        return {'mean': self.populateFinalBucket(mean_metric_tuple),
               'minimum': self.populateFinalBucket(min_metric_tuple),
               'maximum': self.populateFinalBucket(max_metric_tuple),
               'standard_deviation': self.populateFinalBucket(std_metric_tuple)
               }
