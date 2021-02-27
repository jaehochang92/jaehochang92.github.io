---
title: "Academic Works"
permalink: /academic/api/
author_profile: true
---

## Building Flask API in Python

```python
import flask, json, csv
from flask import request, jsonify


try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen


if __name__ == "__main__":
    # Create API with Flask

    app = flask.Flask(__name__)
    app.config["DEBUG"] = True

    @app.route('/', methods=['GET'])
    def home():
        return(
            '''<h1>3A Machine Learning Prediction Service</h1>
                    <p>Specify MDR Type by</p>
                    <p>/ML?type=MRSA</p>
                    <p>or</p>
                    <p>/ML?type=VRE</p>'''
        )

    @app.route('/ML', methods=['GET'])
    def mainprocedure():
        if 'type' in request.args:
            whatuserwants = request.args['type']

            # whose model do you want to fit?
            mdr = "MDR_TYPE_" + str(whatuserwants)

            # numeric features except use_days
            num_list = ["AGE_YR", "PRIOR_LOS", "OP_VISIT_1YR"]

            # ditinguish data using date
            date = "20180917"

            # Get new data
            url = ("ftp://id:pass@192.168.1.234/")
            js = get_jsonparsed_data(url)

            # address
            pwd = "./" + mdr + "_" + date + "/"

            # Get new data and merge
            jsdf = pd.read_json(js)
            mdrdata = pd.read_csv('./MDR_data/'+date+'_'+whatuserwants+'.csv')
            jsdf = pd.concat([jsdf, mdrdata])
            jsdf.to_csv(pwd + 'newdata.csv', index=False)

            # import data, threshold : nearZeroVar()
            newD = preprocessing(pwd+'newdata.csv', num_list, mdr)
            x_new, y_new = newD.input_data(threshold=None)
            x_new = x_new.iloc[:1,]
            x_new = data.use_scale(x_new)

            # predict input data
            pwd = './' + str(mdr) + "_20180917/normal/lgb_RUS.sav"
            # Get new data from 3A
            temp = pickle.load(open(pwd, 'rb'))
            os.remove(pwd+'newdata.csv')
            return jsonify(list(temp.predict_proba(x_new.iloc[:1, :])[:, 1]))

        else:
            return "Error: No MDR type specified."
    app.run()
```