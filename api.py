from google.cloud import vision
import io
import os

#give the path to the cloud vision key file here
json_path = r"C:\Users\ADMIN\Desktop\FirstKey.json"
################################


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=json_path

#Detects text in the file
def detect_text(path):    
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations


    for text in texts:
        print(text.description)

        #vertices = (['({},{})'.format(vertex.x, vertex.y)
        #            for vertex in text.bounding_poly.vertices])

        #print('bounds: {}'.format(','.join(vertices)))
        break


#image name
file_name = '13.jpg'

detect_text(file_name)