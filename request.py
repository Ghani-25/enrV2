import requests

url = 'http://localhost:5000/results'
r = requests.post(url,json={'occupations': 'Freelance I Editorial  Communication  Social media et fondateur de Histoire de Rue, Social Media Manager | Créateur de contenu, Head of Content & Communication | Content Strategy | Social Media | Digital Communication | French Government | France Televisions, Social Media - Content Manager CentraleSupélec'})

print(r.json())
