# Description
This package accepts a nested json as input parameter and provides a flat structured json as output. The output data has additional attributes that help maintaining the relational integrity of the data with parent and child.

# Installation

```
pip install nested-json2rel-data
```


# Usage example

  * ## json file : json_data.json

```
{
"name": "Peter Parker",
"job" : "developer",
"organization": "Daily Bugle",
"address":{"country":"Scotland",
		"state":"Wishaw",
		"city":"Glasgow",
		"pin":"BA1 2FJ"
		},
"email":["peter.parker@gmail.com"
		,"peter_parker@yahoo.com",
		{"primary":"peter.parker@microsoft.com"
		,"secondary":"peter.parker@ibm.com"}],
"education":[
			{"degree": "Bachelor in Media",
			"university":"MIT",
			"school name":"MIT",
			"contact no":[1,2]
			},
			{"degree":"Media and Journalism",
			"university":"oxford",
			"school":"Oxford",
			"contact no":[3,4]
			},
			{"degree":"Social Science",
			"university":"Cambridge",
			"school":"Cambridge",
			"contact no":[5,6]
			}
		],
"other":{"dob":"10-08-2001",
		"parent":{"mother":"Mary Parker",
				"father":"Richard Parker",
				"brother":"Harry Osborn",
				"gardian":{"primary":"self",
							"secondary":"mother"},
				"grandie":{"Uncle":"Ben Parker",
							"auntie" : "Mary Parker"}
				},
		"birth place": "20 Ingram",
		"interest":["football","painting","photography","DIY"]
		},
"social":{"facebook":"yes",
		"instagram":"yes",
		"twitter":"no"
		}
} 
```

  * ## read_json.py
```
import json
from nested_json2rel_data import nested_json_parser as njp

with open('json_data.json') as json_file:
    data = json.load(json_file)
    p = njp.nested_json_parser(data)
    d=p.bucket()
    print("*************dict :")
    print(d)
```

  * ## output
```
*************dict :
[{'root_id': 4, 'root_name': 'address', 'child_of': 'root', 'child_of_id': 0, 'country': 'Scotland', 'state': 'Wishaw', 'city': 'Glasgow', 'pin': 'BA1 2FJ'}, {'root_id': 2, 'root_name': 'email', 'child_of': 'root', 'child_of_id': 0, 'email': 'peter.parker@gmail.com'}, {'root_id': 3, 'root_name': 'email', 'child_of': 'root', 'child_of_id': 0, 'email': 'peter_parker@yahoo.com'}, {'root_id': 12, 'root_name': 'email', 'child_of': 'root', 'child_of_id': 0, 'primary': 'peter.parker@microsoft.com', 'secondary': 'peter.parker@ibm.com'}, {'root_id': 5, 'root_name': 'contact no', 'child_of': 'education', 'child_of_id': 12, 'contact no': 1}, {'root_id': 6, 'root_name': 'contact no', 'child_of': 'education', 'child_of_id': 12, 'contact no': 2}, {'root_id': 12, 'root_name': 'education', 'child_of': 'root', 'child_of_id': 0, 'degree': 'Bachelor in Media', 'university': 'MIT', 'school name': 'MIT'}, {'root_id': 6, 'root_name': 'contact no', 'child_of': 'education', 'child_of_id': 13, 'contact no': 3}, {'root_id': 7, 'root_name': 'contact no', 'child_of': 'education', 'child_of_id': 13, 'contact no': 4}, {'root_id': 13, 'root_name': 'education', 'child_of': 'root', 'child_of_id': 0, 'degree': 'Media and Journalism', 'university': 'oxford', 'school': 'Oxford'}, {'root_id': 7, 'root_name': 'contact no', 'child_of': 'education', 'child_of_id': 15, 'contact no': 5}, {'root_id': 8, 'root_name': 'contact no', 'child_of': 'education', 'child_of_id': 15, 'contact no': 6}, {'root_id': 15, 'root_name': 'education', 'child_of': 'root', 'child_of_id': 0, 'degree': 'Social Science', 'university': 'Cambridge', 'school': 'Cambridge'}, {'root_id': 31, 'root_name': 'gardian', 'child_of': 'parent', 'child_of_id': 27, 'primary': 'self', 'secondary': 'mother'}, {'root_id': 34, 'root_name': 'grandie', 'child_of': 'parent', 'child_of_id': 27, 'Uncle': 'Ben Parker', 'auntie': 'Mary Parker'}, {'root_id': 27, 'root_name': 'parent', 'child_of': 'other', 'child_of_id': 25, 'mother': 'Mary Parker', 'father': 'Richard Parker', 'brother': 'Harry Osborn'}, {'root_id': 5, 'root_name': 'interest', 'child_of': 'other', 'child_of_id': 25, 'interest': 'football'}, {'root_id': 6, 'root_name': 'interest', 'child_of': 'other', 'child_of_id': 25, 'interest': 'painting'}, {'root_id': 7, 'root_name': 'interest', 'child_of': 'other', 'child_of_id': 25, 'interest': 'photography'}, {'root_id': 8, 'root_name': 'interest', 'child_of': 'other', 'child_of_id': 25, 'interest': 'DIY'}, {'root_id': 25, 'root_name': 'other', 'child_of': 'root', 'child_of_id': 0, 'dob': '10-08-2001', 'birth place': '20 Ingram'}, {'root_id': 39, 'root_name': 'social', 'child_of': 'root', 'child_of_id': 0, 'facebook': 'yes', 'instagram': 'yes', 'twitter': 'no'}, {'root_id': 0, 'root_name': 'root', 'child_of': 'root', 'child_of_id': 0, 'name': 'Peter Parker', 'job': 'developer', 'organization': 'Daily Bugle'}]
```
## Definitions
| Attribute       | Parameter     | Description     |
| :------------- | :---------- | :----------- |
|  nested_json_parser.nested_json_parser(data) | data   | Json data    | 
|  p.bucket() | None   | not required    | 
# Source code
[Git Hub Repo](https://github.com/joymaitra/nested-json2rel-data.git)
