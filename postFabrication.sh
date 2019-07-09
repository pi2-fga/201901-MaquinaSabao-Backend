curl -X POST -S \
	-H 'Accept: application/json' \
	-F "start_of_manufacture=2019-11-21 12:00" \
	-F "end_of_manufacture=2019-11-21 13:00" \
	-F "amount_of_soap=2" \
	-F "actual_ph=14" \
	-F "oil_quality=GOOD" \
	-F "have_fragrance=True" \
  -F "device_id=053622051cf6c1de" \
	http://52.67.39.4/manufacturing/
