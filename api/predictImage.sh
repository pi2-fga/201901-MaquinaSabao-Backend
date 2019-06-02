curl -X GET -S \
	-H 'Accept: application/json' \
	-F "oil_image=@/home/caionunes/Documentos/imagePredict.jpg" \
	http://127.0.0.1:8000/predict_oil_quality
