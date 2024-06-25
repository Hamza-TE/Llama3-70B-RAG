To create a deployment for serverless Endpoints of LLM models:

    1. Go to Azure Machine Learning studio.

    2. Select the workspace in which you want to deploy your models. To use the serverless API model deployment offering, your workspace must belong to the East US 2 or Sweden Central region.

    3. Choose the model you want to deploy, for example Phi-3-medium-128k-Instruct, from the model catalog.

    4. On the model's overview page in the model catalog, select Deploy and then Serverless API with Azure AI Content Safety.

    5. Alternatively, you can initiate deployment by going to your workspace and selecting Endpoints > Serverless endpoints > Create. Then, you can select a model.

    6. In the deployment wizard, select the Pricing and terms tab to learn about pricing for the selected model.

    7. Give the deployment a name. This name becomes part of the deployment API URL. This URL must be unique in each Azure region.

    8. Select Deploy. Wait until the deployment is ready and you're redirected to the Deployments page. This step requires that your account has the Azure AI Developer role permissions on the resource group, as listed in the prerequisites.

    9. Take note of the Target URI and the secret Key, which you can use to call the deployment and generate completions. For more information on using the APIs, see Reference: Chat Completions.

    10. Select the Test tab to start interacting with the model.

    11. You can always find the endpoint's details, URI, and access keys by navigating to Workspace > Endpoints > Serverless endpoints.

Create a static web app

    1. Now that the repository is created, you can create a static web app from the Azure portal.

      Go to the Azure portal.
      Select Create a Resource.
      Search for Static Web Apps.
      Select Static Web Apps.
      Select Create.

    2. In the Basics section, begin by configuring your new app and linking it to a GitHub repository.

    3. If necessary sign in with GitHub, and enter the following repository information.
    	Setting 	Value
    	Organization 	Select your organization.
	    Repository 	Select my-first-web-static-app.
	    Branch 		Select main.
    4. In the Build Details section, add configuration details specific to your preferred front-end framework.
      From the Build Presets dropdown, select Custom.
      In the App location box, enter ./src.
      Leave the Api location box empty.
      In the Output location box, enter ./src.

    5. Select Review + create.

    6. Select Create.

