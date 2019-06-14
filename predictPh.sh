curl -X POST -S \
	-H 'Accept: application/json' \
	-F "amount_of_soap=2" \
	-F "oil_quality=2" \
	-F "have_fragrance=True" \
	http://127.0.0.1:8000/predict_ph/
