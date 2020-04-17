import pulumi
from pulumi_fastly import Servicev1, ServiceDictionaryItemsv1


def main():
    config = pulumi.Config(name="ghfastly")
    service_config = config.require_object("service")
    dict_names = [{"name": d.get("name", None)} for d in service_config["dictionaries"]]
    service = Servicev1(service_config["name"], name=service_config["name"], domains=service_config["domains"],
                        dictionaries=dict_names, backends=service_config["backends"], activate=False,
                        force_destroy=True)
    pulumi.export("Dictionaries", service.dictionaries)
    di = []
    for dictionary in service_config["dictionaries"]:
        if not pulumi.runtime.is_dry_run():
            dictionary_id = service.dictionaries.apply(
                lambda x: get_dictionary_id(x, dictionary.get("name")))
        else:
            # https://github.com/pulumi/pulumi-azure/issues/192
            dictionary_id = service.dictionaries.apply( lambda dictionary_id: "11111111-1111-1111-1111-111111111111")
        di.append(
            ServiceDictionaryItemsv1(dictionary["name"], opts=pulumi.ResourceOptions(parent=service), service_id=service.id, items=dictionary["items"], dictionary_id=dictionary_id))
        pulumi.export("Dictionary Items", di)

def get_dictionary_id(dictionaries, dict_name):
    for i in dictionaries:
        if dict_name == i["name"]:
            return i.get("dictionary_id")


if __name__ == "__main__":
    main()
