# EASIER SDK

Start to interact with EASIER platform by openning a session with the EasierSDK handler using your __MINIO `user` and `password`__, which are the same as your __EASIER credentials__ if you are using an EASIER official platform.  

```
from easierSDK.easier import EasierSDK
from easierSDK.classes.categories import Categories

easier = EasierSDK(minio_url="minio.easier-ai.eu", minio_user="", minio_password="")  
```

You can also connect to your local MINIO repository, but remember to use the proper configuration (`secure` and `region` parameters for MINIO client):

```
easier = EasierSDK(minio_url="", minio_user="", minio_password="", secure=False, region=None)
```

In EASIER, models and datasets can be identified by their parent repository and their category. You can get an overview of the available repositories that you can interact with by using the following function. It also shows how many models and datasets are available in each repository. 

```
easier.show_available_repos()  
```

Set the parameter `deep` to True to get more in-depth information of the content of the repositories: the name of the models and datasets that are inside each repository.

```
models_list, datasets_list = easier.show_available_repos(deep=True)  
```

The function also returns a list of the models and datasets available. 

```
print(models_list)
print(datasets_list)
```

Similarly, you can list the models and datasets by their category. The function behaves as the previous one.

```
easier.show_categories()
models_list, datasets_list = easier.show_categories(deep=True)  
print(models_list)
print(datasets_list)
```

## EASIER internal APIs: Models and Datasets

The EASIER SDK handles two internal APIs: `ModelsAPI` and `DatasetsAPI`. They allow you to interact seamlessly with models and datasets of the platform, respectively. 

### EASIER Models API

You can get an overview of the available models by using this function. It accepts two parameters: one for the parent repository of the models and one for the category of the models. Remember that there exists an enumerator for the categories to help you in identifying them. It was imported as `Categories`. 

```
easier.models.show_models()
easier.models.show_models(repo_name="") 
easier.models.show_models(category=Categories.MISC)  
easier.models.show_models(repo_name="", category=Categories.MISC)  
```

In addition, you can use the following function to get information about any model's metadata (such as features, version, last modified date, etc.), by indicating the parent repository, the category and the model name (which is shown as output of the previous function). It is imporant to mention that __the names are case sensitive__. 

```
easier.models.show_model_info(repo_name="", category=Categories.MISC, model_name="")
```

Similarly, you can get the information about a specific model version by using its experiment identifier.  

```
easier.models.show_model_info(repo_name="", category=Categories.MISC, model_name="", experimentID=1)
```

In addition, the model's configuration and structure can be obtained with the following function. It outputs information as: number of layers, name of each layer, name of optimizers, etc. The experimentID is __mandatory__ in this case. 

```
easier.models.show_model_config(repo_name="", category=Categories.MISC, model_name="", experimentID=1)
```

#### Loading a model

Use this function to load a model directly from the repository. If you don't set the experimentID, the function will load the last version of the model. The function returns a variable of type [`EasierModel`](easierSDK/classes/easier_model.py), check the documentation to get more information about this class. 

```
my_easier_model = easier.models.load_from_repository(repo_name="", category=Categories.MISC, model_name="")
# my_easier_model = easier.models.load_from_repository(repo_name="", category=Categories.MISC, model_name="", experimentID=1)
```

Depending on how the model was saved, it will load either: the entire model, just the weights or just the model configuration. You can indicate which of the load options you would like to use, in case there 
are more than one option, by using the `load_level` parameter. Your options are: `constants.FULL` (default), `constants.WEIGHTS_ONLY` or `constants.CONFIG_ONLY`.

```
my_easier_model = easier.models.load_from_repository(repo_name="", category=Categories.MISC, model_name="", load_level=constants.FULL)
# my_easier_model = easier.models.load_from_repository(repo_name="", category=Categories.MISC, model_name="", experimentID=1, load_level=constants.FULL)
```

You can print the model's information enclosed in its [`ModelMetadata`](easierSDK/classes/model_metadata.py) variable. Every model in EASIER has metadata. Similarly, check the documentation to get more information about this class. 

```
my_easier_model_metadata = my_easier_model.get_metadata()
my_easier_model_metadata.pretty_print()
```

One important attribute of the `ModelMetadata` class is the `features` attribute. If your model was trained using a set of features from tabular data, you are encouraged to save the features as a list on this variable, so that future uses of this model know which features the model was trained with.  

```
print(my_easier_model_metadata.features)
```

Of course, you can create your own model and then assign it to an `EasierModel`. Make sure you check the documentation to see what can you store in this class:

```
# - Create model from scratch
my_tf_model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(28, activation='relu', input_shape=(784,)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10)
  ])

my_tf_model.compile(optimizer='adam',
            loss=tf.keras.losses.categorical_crossentropy,
            metrics=[tf.keras.metrics.mean_squared_error])

# - Create ModelMetadata
metadata = {}
metadata["category"] = Categories.HEALTH.value
metadata["name"] = 'eyedesease-dl'
metadata["last_modified"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
metadata["description"] = 'My Eye Deseases DL implementation'
metadata["version"] = 1
metadata["features"] = ["timestamp","patient-previous-status","patient-post-result"]
mymodel_metadata = ModelMetadata(metadata)

# - Create Easier Model from memory
my_easier_model = EasierModel(mymodel_metadata)
# my_easier_model.set_metadata(mymodel_metadata)
my_easier_model.set_model(my_tf_model)
# my_easier_model.set_scaler(my_scaler)
```

You can also import a model from a local path. In order to use this built-in function, remember that it should follow the [_EASIER file extension guide_](easierSDK/docs/guides/EASIER_file_extension_guide.md) for a proper loading of all the objects. Check the documentation to get more information about how each type of files is managed. If it is not followed, you can also load your objects by hand and then assign it to an `EasierModel` variable, as shown before. 

```
my_easier_model = easier.models.load_from_local(path="", load_level=constants.FULL)
```

#### Compilating a TF model to TF Lite

EASIER SDK has a specific function to compile your TF model to the TF Lite version. You just need to pass the variable of type `EasierModel` and some calibration data (with a few examples is enough) (as a `numpy.array`) which was used to train the model. 

```
easier_models.compile_tflite(model=my_easier_model, calibration_data=x)
```

#### Upload Model

Once you have finished to work with your model, you can upload it to the EASIER platform. Remember to create a `ModelMetadata` variable for your model, and to assign it to the EasierModel before uploading it. Besides, you have the possibility to make it public for other EASIER users (it will be uploaded to your public repository).  

```
my_easier_model.set_metadata(my_easier_model_metadata)
easier.models.upload(category=Categories.MISC, model=my_easier_model, public=False)
```

### EASIER Datasets API

Similar to the Models API, you can get an overview of the available datasets by using this function. It accepts two parameters: one for the parent repository of the datasets and one for the category of the datasets. Remember that there exists an enumerator for the categories to help you in identifying them. It was imported as `Categories`.

```
easier.datasets.show_datasets()  
easier.datasets.show_datasets(repo_name="")  
easier.datasets.show_datasets(category=Categories.MISC)  
easier.datasets.show_datasets(repo_name="", category=Categories.MISC)  
```

In addition, you can use the following function to get more information about a dataset, which is identified by their parent repository, its category and its name (which is shown as output of the previous function).  

```
easier.datasets.show_dataset_info(repo_name="", category=Categories.MISC, dataset_name="")
```

