import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import trackers.jobtracker as jobtracker

jt = jobtracker.JobTracker()

context = {
  "identifier": "URN-3:IIIF_DEMO:10001",
  "account": "Placeholder Account",
  "space": "Placeholder Space",
  "iiif_version": "2.1.1",
  "originalLocation": "DRS",
  "manifestLocation": "example.com",
  "mediaType": "image",
  "assetLocation": "AWS",
  "width": 2400,
  "height": 2400,
  "adminMetadata": {
    "title": "Admin Metadata Example 1",
    "category": "Art",
    "description": "A description of admin metadata",
    "items": [
      {
        "name": "Item 1",
        "seq": 1
      },
      {
        "name": "Item 2",
        "seq": 2
      },
      {
        "name": "Item 3",
        "seq": 3
      }
    ]
  },
  "policy": {
    "policyGroupName": "default"
  }
}

initial_tracker_file = jt.init_tracker_file('create_asset', context)
print('Initial job tracker file created')
print(initial_tracker_file)
job_ticket_id = initial_tracker_file.get('job_ticket_id')
tracker_file = jt.get_tracker_file(job_ticket_id)
tracker_file['context']['a_test_property'] = 'A test property appended to the tracker file'
print('Job tracker file updated')
updated_tracker_file = jt.write_tracker_file(tracker_file)
print(updated_tracker_file)
job_ticket_id = updated_tracker_file.get('job_ticket_id')
job_timestamp_file = jt.update_timestamp_file(job_ticket_id)
print('Job timestamp file created')
print(job_timestamp_file)
job_timestamp_file = jt.get_timestamp_file(job_ticket_id)
print('Get job timestamp file')
print(job_timestamp_file)
job_timestamp_file = jt.get_timestamp_file('{}{}'.format(job_ticket_id, 'test'))
print('Test invalid timestamp file')
print(job_timestamp_file)
# TODO: Implement a test library to gracefully catch expected error conditions
initial_tracker_file_invalid = jt.init_tracker_file('invalid_job_name')
print('Test invalid job name')
print(initial_tracker_file_invalid)
job_ticket_id_invalid = jt.get_tracker_file('9311801c-41f8-42ea-b138-3ff455646315')
print('Test invalid ticket id')
print(job_ticket_id_invalid)