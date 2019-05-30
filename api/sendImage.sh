curl -X POST -S \
	-H 'Accept: application/json' \
	-F "date_of_manufacture=2019-10-28" \
	-F "start_of_manufacture=12:00" \
	-F "end_of_manufacture=13:00" \
	-F "amount_of_soap=2" \
	-F "expected_ph=7" \
	-F "actual_ph=14" \
	-F "oil_quality=GOOD" \
	-F "have_fragrance=True" \
	-F "oil_image=@/home/caionunes/Documentos/image.jpg" \
	http://127.0.0.1:8000/manufacturing/
