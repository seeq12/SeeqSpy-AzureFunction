# Seeq SPy Facade via Azure Functions and ADF

This example shows the use of an Azure function to provide a SPy-like experience via HTTP POST calls. In this example the SPy Search and SPy pulls are combined, however, this could be broken out and pickled search results could be used instead.

# Deployment
**NOTE:** This function uses a serverless deployment model. Additionally, the function code is kept intentionally simple to demonstrate the concept. 

## Deploy the Azure Function

1. Clone this repo
1. Navigate to your local repo and open the `SpyPull.py` file in `repo/Functions/src/handlers`
1. Find the `spy.login` call on line 26 and replace the `<your_server>` field with the URL of your Seeq server
    * Note that this function has you passing the id and secret as part of the body of the POST, however, this should be read as os.environ variables that are injected from Azure Key Vault [More info here](https://docs.microsoft.com/en-us/azure/app-service/app-service-key-vault-references)
1. If using serverless ensure you have the serverless framework installed [(More info here)](https://www.serverless.com/open-source/). Additionally, have the Azure plugin installed with `npm i --save serverless-azure-functions` [(More information here)](https://www.serverless.com/framework/docs/providers/azure/guide/installation/)
1. Run `sls deploy`
    * In about 5 minutes you should have your function and associated app service completely deployed into a new resource group
1. Navigate to your function within the Azure portal and click on the `App Keys` under `Functions` in the side bar 
1. You can create a new host key or use the `default` key by clicking on the *Hidden value. Click to show value* text. Note this key for the next step

## Deploy the ADF template

1. If you do not already have an Azure Data Factory instance, create one
1. From within the `Author and Monitor` Portal, in the `Factory Resources` sidebar click the plus sign to create a new `Pipeline from template`
1. Select the button at the top of the template grid that says `Use local template`
1. Navigate to the *SpyPull.zip* in `repo/ADF/templates` and click `Open`
1. In the drop down list under SpyPull/AzureFunction, click the `+New` option
1. Call the function `SpyPull` by typing that in the `Name` field
1. Select the function by navigating to the function you created in the section above by choosing the subscription and the Azure Function App URL
1. Paste in the function key from the last step in the section above, or retrieve it from a Key Vault
1. Click create, and the blade will close
1. Click `Use this template` in the bottom left
1. Once you are back in the Pipleine authoring page, you should see the SpyPull Function
1. Click on the function, and click on the `Settings` tab in the sub window under the pipeline diagram
1. Modify the properties in the `Body` to match what you want to search for
1. Click `Debug` above the pipeline diagram
1. After a few seconds (depending on the amount of data) you should see `Succeeded` in the window, and you can see the output of the function that can be passed onto another step.


