from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from PIL import Image, ImageDraw, ImageFont
import os
import colorsys

def black_white(r, g, b):
	brightness = (r * 299 + g * 587 + b * 114) / 1000
	if brightness > 123:
		return (0, 0, 0)
	else:
		return (255, 255, 255)

# Create your views here.
@csrf_exempt
#@require_POST
def index(request):
	file = os.listdir("./colors/static/colors/")
	for f in file:
		os.remove("./colors/static/colors/"+f)

	input_data = json.loads(request.body.decode('utf-8'))

	red = int(input_data["queryResult"]["parameters"]["red"])
	c_red = 255-red
	green = int(input_data["queryResult"]["parameters"]["green"])
	c_green = 255-green
	blue = int(input_data["queryResult"]["parameters"]["blue"])
	c_blue = 255-blue

	intent_name = input_data["queryResult"]["intent"]["displayName"]
	conversation_id = input_data["originalDetectIntentRequest"]["payload"]["conversation"]["conversationId"]

	img = Image.new('RGB', (1280, 720), (red, green, blue))
	d = ImageDraw.Draw(img)
	d.rectangle([640, 0, 1280, 720], (c_red, c_green, c_blue))
	font = ImageFont.truetype(font="./colors/CaviarDreams_Bold.ttf", size=60)

	font_color = black_white(red, green, blue)
	c_font_color = black_white(c_red, c_green, c_blue)

	d.text((50, 100), "RGB({}, {}, {})".format(red, green, blue), font_color, font)
	d.text((690, 100), "RGB({}, {}, {})".format(c_red, c_green, c_blue), c_font_color, font)

	r, g, b = red, green, blue
	r, g, b = r/255.0, g/255.0, b/255.0
	h, l, s = colorsys.rgb_to_hls(r, g, b)
	d.text((50, 250), "HSL({:.2f}, {:.2f}, {:.2f})".format(h, s, l), font_color, font)
	r, g, b = c_red, c_green, c_blue
	r, g, b = r/255.0, g/255.0, b/255.0
	h, l, s = colorsys.rgb_to_hls(r, g, b)
	d.text((690, 250), "HSL({:.2f}, {:.2f}, {:.2f})".format(h, s, l), c_font_color, font)

	hexad = '#%02x%02x%02x' % (red, green, blue)
	c_hexad = '#%02x%02x%02x' % (c_red, c_green, c_blue)
	d.text((50, 400), "HEX "+hexad, font_color, font)
	d.text((690, 400), "HEX "+c_hexad, c_font_color, font)

	d.text((50, 620), "Your Color", font_color, font)
	d.text((690, 620), "It's Complement", c_font_color, font)

	file_path = "./colors/static/colors/" + conversation_id + ".png"
	img.save(file_path)

	current_working_response = {
	  "payload": {
	    "google": {
	      "expectUserResponse": False, #  False means end of conversation, True means waits for user response
	      "richResponse": {
	        "items": [
				{
					"simpleResponse": {
					  "textToSpeech": "Here you go !"
					}
				}, 
				{  
					"basicCard":{  
						"image":{  
								"url":"https://secure-tundra-21259.herokuapp.com/static/colors/"+conversation_id+".png",
								"accessibilityText":"Indigo Taco Color"
							}
					}
				}
	        ]
	      }
	    }
	}}
	#os.remove(file_path)
	return JsonResponse(current_working_response, content_type="application/json")

	"""
	current_working_response = {
	  "payload": {
	    "google": {
	      "expectUserResponse": False, #  False means end of conversation, True means waits for user response
	      "richResponse": {
	        "items": [
				{
					"simpleResponse": {
					  "textToSpeech": "this is a simple response"
					}
				}, 
				{  
					"basicCard":{  
						"image":{  
								"url":"https://storage.googleapis.com/material-design/publish/material_v_12/assets/0BxFyKV4eeNjDN1JRbF9ZMHZsa1k/style-color-uiapplication-palette1.png",
								"accessibilityText":"Indigo Taco Color"
							},
							"imageDisplayOptions":"WHITE"
					}
				}
	        ]
	      }
	    }
	}},"""

"""############ IDEAL RESPONSE FROM FIREBASE FUNCTION ##################


{
  "conversationToken": "[\"_actions_on_google\",\"welcome-color-type-yes-bvalue-followup\"]",
  "finalResponse": {
    "richResponse": {
      "items": [
        {
          "simpleResponse": {
            "textToSpeech": "H is 60 S is 1 V is 48 and"
          }
        },
        {
          "basicCard": {
            "image": {
              "url": "https://storage.googleapis.com/material-design/publish/material_v_12/assets/0BxFyKV4eeNjDN1JRbF9ZMHZsa1k/style-color-uiapplication-palette1.png",
              "accessibilityText": "Indigo Taco Color"
            },
            "imageDisplayOptions": "WHITE"
          }
        }
      ]
    }
  },
  "responseMetadata": {
    "status": {
      "message": "Success (200)"
    },
    "queryMatchInfo": {
      "queryMatched": true,
      "intent": "a6cd04b8-c95f-497e-be07-caf165b99cbf",
      "parameterNames": [
        "color-type-entity"
      ]
    }
  },
  "userStorage": "{\"data\":{}}"
}


testing_response = {"finalResponse": {
    "richResponse": {
      "items": [
        {
          "simpleResponse": {
            "textToSpeech": "H is 60 S is 1 V is 48 and"
          }
        },
        {
          "basicCard": {
            "image": {
              "url": "https://storage.googleapis.com/material-design/publish/material_v_12/assets/0BxFyKV4eeNjDN1JRbF9ZMHZsa1k/style-color-uiapplication-palette1.png",
              "accessibilityText": "Indigo Taco Color"
            },
            "imageDisplayOptions": "WHITE"
          }
        }
      ]
    }
  }}

#####################################################"""