import requests

# Set headers with Bearer token and Content-Type
headers = {
    'Authorization': f'Bearer {"2440|XghCSF0H9yq7wEratzvDHMt94J48pfBFktJuBsOG432b5a85"}',
}

# Create a dictionary to simulate multipart/form-data
files = {
    'front': ('image.png', open('/Users/tsepomontsi/scratch/showbuddy/tests/integration/files/business_card_0.png', 'rb')),
}

# Make the POST request with requests
response = requests.post('https://spreadly.app/api/v1/business-card-scans', headers=headers, files=files)

# Handle the response
scan = response.json()
print('Response:', scan)