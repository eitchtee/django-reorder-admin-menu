def get_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request, None)

    if not app_dict:  # No apps
        return

    # Flatten all models from apps
    models_dict = {}
    for app_name, app in app_dict.items():
        for model in app["models"]:
            model_name = "%s.%s" % (app_name, model["object_name"])
            model["model_name"] = model_name
            models_dict[model_name] = model

    new_admin_ordering = []
    if app_label:
        if app_label not in [x["app"] for x in ADMIN_ORDERING]:
            new_admin_ordering.append({"app": app_label})
        else:
            for wanted_app in ADMIN_ORDERING:
                if wanted_app["app"] == app_label:
                    new_admin_ordering.append(wanted_app)

    else:
        for app_key in list(app_dict.keys()):
            if not any(app_key in wantend_app["app"] for wantend_app in ADMIN_ORDERING):
                app_dict.pop(app_key)

    app_list = []
    processed_models = []

    for app in new_admin_ordering or ADMIN_ORDERING:
        app_label, app_name, models = (
            app["app"],
            app.get("label"),
            app.get("models", ["*"]),
        )

        new_app = deepcopy(app_dict[app_label])
        new_app["models"] = []
        if app_name:
            new_app["name"] = app_name

        for model, model_obj in models_dict.items():
            model_app, model_name = model.split(".")
            if model_name in models or model in models:
                new_app["models"].append(model_obj)
                processed_models.append(model_name)
            elif "*" in models and model_app == app_label:
                new_app["models"].append(model_obj)
                processed_models.append(model_name)
            elif (
                "%" in models
                and model_app == app_label
                and model_name not in processed_models
            ):
                new_app["models"].append(model_obj)
                processed_models.append(model_name)

        # Primeiro, ordena a lista alfabeticamente
        new_app["models"].sort(key=lambda x: (x["name"]))
        # Então ordena a lista com base na ordem do ADMIN_ORDERING, colocando os elementos "*" em último (já em ordem
        # alfabética)
        new_app["models"].sort(
            key=lambda x: (
                models.index(x["object_name"])
                if x["object_name"] in models
                else len(models)
            )
        )

        app_list.append(new_app)

    return app_list
