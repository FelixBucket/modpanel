import time
from django.core.management.base import BaseCommand, CommandError
from ttr.rpc import RPC
from mcp.models import ShardCheckIn

class Command(BaseCommand):
    help = 'Loads shard information and stores it'

    def handle(self, *args, **options):

        # Set up RPC connection and load shard data
        rpc = RPC()
        shards = rpc.client.listShards()
        updated_count = 0

        # Ensure all new records have the same fetched time
        # This will allow us to add up population counts, etc.
        fetched_time = int(time.time())

        # Process each shard we were given information on
        for shard in shards:
            # Pull up the last record we have for this shard
            last_record = ShardCheckIn.objects.filter(district=shard.get('districtName')).order_by('-timestamp')[:1]
            if last_record:
                last_record = last_record[0]

            # If the fresh data isn't newer than the last record's timestamp, ignore it
            if last_record and last_record.timestamp >= shard.get('lastSeen'):
                continue

            # At this point we have fresh data, let's add it
            check_in = ShardCheckIn(district=shard.get('districtName'), district_id=shard.get('districtId'), channel=shard.get('channel'),
                                    frame_rate=shard.get('avg-frame-rate'), invasion=shard.get('invasion'), population=shard.get('population'),
                                    heap_objects=shard.get('heap', {}).get('objects'), heap_garbage=shard.get('heap', {}).get('garbage'),
                                    cpu_usage=str(shard.get('cpu-usage')), mem_usage=shard.get('mem-usage'), timestamp=shard.get('lastSeen'),
                                    fetched=fetched_time)
            check_in.save()
            updated_count += 1

        # For debugging purposes
        print "Added historical data for " + str(updated_count) + " shards. " + str(len(shards)-updated_count) + " shards did not have fresh information."