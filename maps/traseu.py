import googlemaps

def obtine_traseu(api_key, start_locatie, destinatie_locatie, mod_transport):
    gmaps = googlemaps.Client(key=api_key)

    # Obține coordonatele pentru locații
    start_coord = gmaps.geocode(start_locatie)[0]['geometry']['location']
    destinatie_coord = gmaps.geocode(destinatie_locatie)[0]['geometry']['location']

    # Obține traseu
    directii = gmaps.directions(start_coord, destinatie_coord, mode=mod_transport)

    return directii

# Exemplu de utilizare
API_KEY = 'AIzaSyAD1KCCoKf_NpcFpJ1Q0Y5AINHeMRgExpo'
start_locatie = '46.99116252254659,6.933674708596586'
destinatie_locatie = 'Pub 18'
mod_transport = 'driving'  # sau 'walking', 'transit', etc.

rezultat_traseu = obtine_traseu(API_KEY, start_locatie, destinatie_locatie, mod_transport)

print(rezultat_traseu)
