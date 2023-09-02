# Examples

This page provides detailed examples of how to use Airdot. Using Airdot is actually quite simple and efficient and that makes it very user friendly, before moving ahead make sure you have correct setup Airdot.

## Local test deployment

### Copy paste following code to your jupyter notebook

```py
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from airdot.deployer import Deployer
from sklearn import datasets
import pandas as pd
import numpy as np

iris = datasets.load_iris()
iris = pd.DataFrame(
    data= np.c_[iris['data'], iris['target']],
    columns= iris['feature_names'] + ['target']
)
X = iris.drop(['target'], axis=1)
X = X.to_numpy()[:, (2,3)]
y = iris['target']
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.5, random_state=42)
log_reg = LogisticRegression()
log_reg.fit(X_train,y_train)

def predict(value):
    return log_reg.predict(value)

deployer_obj = Deployer().run(predict)

!curl -XPOST http://127.0.0.1:8000 -H 'Content-Type: application/json' -d '{"value": [[4.7, 1.2]]}'

```

## Deployment on cluster with seldon-core setup

```py
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from airdot.deployer import Deployer
from sklearn import datasets
import pandas as pd
import numpy as np

iris = datasets.load_iris()
iris = pd.DataFrame(
    data= np.c_[iris['data'], iris['target']],
    columns= iris['feature_names'] + ['target']
)
X = iris.drop(['target'], axis=1)
X = X.to_numpy()[:, (2,3)]
y = iris['target']
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.5, random_state=42)
log_reg = LogisticRegression()
log_reg.fit(X_train,y_train)

def predict(value):
    return log_reg.predict(value)

# this is using default seldon-deployment configuration.
config = {
        'deployment_type':'seldon',
        'bucket_type':'minio',
        'image_uri':'<registry>/target_species:latest',
        }

deployer = Deployer(deployment_configuration=config).run(target_species)

!curl -XPOST <cluster-url> \
-H 'Content-Type: application/json' \
-d '{ "data": {"ndarray":[1,2]} }' \
| json_pp
```

## Deployment on cluster with seldon-core setup

```py
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from airdot.deployer import Deployer
from sklearn import datasets
import pandas as pd
import numpy as np

iris = datasets.load_iris()
iris = pd.DataFrame(
    data= np.c_[iris['data'], iris['target']],
    columns= iris['feature_names'] + ['target']
)
X = iris.drop(['target'], axis=1)
X = X.to_numpy()[:, (2,3)]
y = iris['target']
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.5, random_state=42)
log_reg = LogisticRegression()
log_reg.fit(X_train,y_train)

def predict(value):
    return log_reg.predict(value)

# this is using default seldon-deployment configuration.
config = {
        'deployment_type':'seldon',
        'bucket_type':'minio',
        'image_uri':'<registry>/target_species:latest',
        'seldon_configuration': '' # your custom seldon configuration
        }

deployer = Deployer(deployment_configuration=config).run(target_species)

!curl -XPOST <cluster-url> \
-H 'Content-Type: application/json' \
-d '{ "data": {"ndarray":[1,2]} }' \
| json_pp
```
