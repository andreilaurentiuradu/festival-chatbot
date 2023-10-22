from flask import Flask, request
from flask_cors import CORS, cross_origin
import os
import googlemaps
import csv
import urllib.request
import json
import re
import math

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'sunt-smecher'
os.environ["OPENAI_API_KEY"] = "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"

csv_file = "output.csv"
place_number = None

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False

query = None

chat_history = []


def distanta_euclidiana(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2 - x1)*2 + (y2 - y1)*2)


def cea_mai_apropiata_locatie(coord_input, vector):
    cel_mai_apropiat = None
    distanta_minima = float('inf')

    for locatie in vector:
        distanta = distanta_euclidiana(coord_input, locatie)
        if distanta < distanta_minima:
            distanta_minima = distanta
            cel_mai_apropiat = locatie

    return str(cel_mai_apropiat(1)) + ',' + str(cel_mai_apropiat(2))


# Vectorii de locații pentru fiecare culoare
vector_albastru = [
    (46.989559, 6.931068),
    (46.991833, 6.932517),
    (46.992036, 6.931065),
    (46.992510, 6.928410)
]

vector_portocaliu = [
    (46.989607, 6.931196),
    (46.991779, 6.932377),
    (46.992079, 6.931182),
    (46.992698, 6.928312),
    (46.990857, 6.927964)
]

# Vectorul de locații pentru toalete
vector_toalete = [
    (46.989743, 6.931046),
    (46.993644, 6.936283),
    (46.993102, 6.936684),
    (46.992743, 6.934873),
    (46.992051, 6.934143),
    (46.992359, 6.935448),
    (46.991828, 6.932504),
    (46.989219, 6.929878),
    (46.989985, 6.929333),
    (46.991120, 6.930404),
    (46.991586, 6.931155),
    (46.990663, 6.928274),
    (46.991048, 6.929443),
    (46.991410, 6.930132),
    (46.992059, 6.931330),
    (46.992218, 6.930620),
    (46.992578, 6.930200),
    (46.992278, 6.928346),
    (46.991708, 6.927578),
    (46.993331, 6.927838),
    (46.993561, 6.927523)
]


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def locatie_in_cod(search_stall_name):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)

        # Search for the stall_name
        for row in reader:
            if row['stall_name'] == search_stall_name:
                place_number = row['place_number']
                break

    centerpoint = None

    with urllib.request.urlopen(
            "https://file.notion.so/f/f/ba535503-9bce-4686-86ed-0e28252f817c/c6dbfe71-86f4-4d16-9f5c-4e74e7bd6d35/fdv_stands20230920.geojson?id=8f098f20-27e5-4aa0-bdf4-da147574c90b&table=block&spaceId=ba535503-9bce-4686-86ed-0e28252f817c&expirationTimestamp=1697990400000&signature=rLPq22BU_LPkc9i_29SJyLK-3YbZihLWBjdiV0io3kg&downloadName=fdv_stands20230920.geojson") as url:
        data = json.loads(url.read().decode())
        features = data['features']
        for feature in features:
            numero = feature['properties']['numero']
            if numero == place_number:
                wrong_centerpoint = feature['properties']['centerpoint'].split(", ")
                centerpoint = wrong_centerpoint[1] + "," + wrong_centerpoint[0]

    print(centerpoint)
    return centerpoint


def obtine_traseu(api_key, start_locatie, destinatie_locatie, mod_transport):
    gmaps = googlemaps.Client(key=api_key)

    aj = start_locatie.split(',')
    start_coord = {'lat': float(aj[0]), 'lng': float(aj[1])}
    print(start_coord)
    aj2 = destinatie_locatie.split(',')
    destinatie_coord = {'lat': float(aj2[0]), 'lng': float(aj2[1])}
    print(destinatie_coord)
    return gmaps.directions(start_coord, destinatie_coord, mode=mod_transport)


@app.route('/chat', methods=["POST"])
@cross_origin()
def answer_chat():
    given_input = request.get_json()
    question = given_input['message']
    query = question
    if PERSIST and os.path.exists("persist"):
        print("Reusing index...\n")
        vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
        index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    else:
        #   loader = TextLoader("data/data.txt") # Use this line if you only need data.txt
        loader = DirectoryLoader("data/")
        if PERSIST:
            index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])
        else:
            index = VectorstoreIndexCreator().from_loaders([loader])

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-3.5-turbo"),
        retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
    )
    if not query:
        print("esti bou")
    result = chain({"question": query, "chat_history": chat_history})
    print(result['answer'])
    chat_history.append((query, result['answer']))
    query = None
    return result['answer']


@app.route("/coordinates", methods=["POST"])
@cross_origin()
def send_directions():
    given_input = request.get_json()
    API_KEY = 'AIzaSyAD1KCCoKf_NpcFpJ1Q0Y5AINHeMRgExpo'
    start_locatie = given_input['x'] + ',' + given_input['y']
    search_stall_name = given_input['location']
    print(search_stall_name)
    mod_transport = 'walking'  # sau 'walking', 'transit', etc.

    if search_stall_name == 'blue bin':
        rezultat_traseu = obtine_traseu(API_KEY, start_locatie, cea_mai_apropiata_locatie((float(given_input['x']), float(given_input['y'])), vector_albastru), mod_transport)
        google_maps_link = f"https://www.google.com/maps/dir/'{start_locatie}'/{start_locatie}/@{cea_mai_apropiata_locatie((float(given_input['x']), float(given_input['y'])), vector_albastru)},19.7z/data=!4m9!4m8!1m5!1m1!1s0x0:0x20462b1222c2eaca!2m2!1d6.9284028!2d46.9904456!1m0!3e2?entry=ttu"
        return {
            'distance': rezultat_traseu[0]['legs'][0]['steps'][0]['distance']['text'],
            'instructions': cleanhtml(rezultat_traseu[0]['legs'][0]['steps'][0]['html_instructions']),
            'duration': rezultat_traseu[0]['legs'][0]['steps'][0]['duration']['text'],
            'maps_link': google_maps_link,
            'destination': cea_mai_apropiata_locatie((float(given_input['x']), float(given_input['y'])), vector_albastru)
        }
    elif search_stall_name == 'orange bin':
        rezultat_traseu = obtine_traseu(API_KEY, start_locatie,
                                        cea_mai_apropiata_locatie((float(given_input['x']), float(given_input['y'])),
                                                                  vector_portocaliu), mod_transport)
        google_maps_link = f"https://www.google.com/maps/dir/'{start_locatie}'/{start_locatie}/@{cea_mai_apropiata_locatie((float(given_input['x']), float(given_input['y'])),vector_portocaliu)},19.7z/data=!4m9!4m8!1m5!1m1!1s0x0:0x20462b1222c2eaca!2m2!1d6.9284028!2d46.9904456!1m0!3e2?entry=ttu"
        return {
            'distance': rezultat_traseu[0]['legs'][0]['steps'][0]['distance']['text'],
            'instructions': cleanhtml(rezultat_traseu[0]['legs'][0]['steps'][0]['html_instructions']),
            'duration': rezultat_traseu[0]['legs'][0]['steps'][0]['duration']['text'],
            'maps_link': google_maps_link,
            'destination': cea_mai_apropiata_locatie((float(given_input['x']), float(given_input['y'])),vector_portocaliu)
        }
    elif search_stall_name == 'toilet':
        rezultat_traseu = obtine_traseu(API_KEY, start_locatie,
                                        cea_mai_apropiata_locatie((float(given_input['x']), float(given_input['y'])),
                                                                  vector_toalete), mod_transport)
        google_maps_link = f"https://www.google.com/maps/dir/'{start_locatie}'/{start_locatie}/@{cea_mai_apropiata_locatie((float(given_input['x']), float(given_input['y'])),vector_toalete)},19.7z/data=!4m9!4m8!1m5!1m1!1s0x0:0x20462b1222c2eaca!2m2!1d6.9284028!2d46.9904456!1m0!3e2?entry=ttu"
        return {
            'distance': rezultat_traseu[0]['legs'][0]['steps'][0]['distance']['text'],
            'instructions': cleanhtml(rezultat_traseu[0]['legs'][0]['steps'][0]['html_instructions']),
            'duration': rezultat_traseu[0]['legs'][0]['steps'][0]['duration']['text'],
            'maps_link': google_maps_link,
            'destination': cea_mai_apropiata_locatie((float(given_input['x']), float(given_input['y'])),vector_toalete)
        }

    destinatie_locatie = locatie_in_cod(search_stall_name)
    print(destinatie_locatie)

    rezultat_traseu = obtine_traseu(API_KEY, start_locatie, destinatie_locatie, mod_transport)
    google_maps_link = f"https://www.google.com/maps/dir/'{start_locatie}'/{start_locatie}/@{destinatie_locatie},19.7z/data=!4m9!4m8!1m5!1m1!1s0x0:0x20462b1222c2eaca!2m2!1d6.9284028!2d46.9904456!1m0!3e2?entry=ttu"
    return {
        'distance': rezultat_traseu[0]['legs'][0]['steps'][0]['distance']['text'],
        'instructions': cleanhtml(rezultat_traseu[0]['legs'][0]['steps'][0]['html_instructions']),
        'duration': rezultat_traseu[0]['legs'][0]['steps'][0]['duration']['text'],
        'maps_link': google_maps_link,
        'destination': destinatie_locatie
    }


if __name__ == "__main__":
    app.run(debug=True)
