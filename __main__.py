import pulumi
from pulumi_fastly import Servicev1, ServiceDictionaryItemsv1
import dumbprovider

def main():
    config = pulumi.Config(name="ghfastly")
    service_config = config.require_object("service")
    dict_names = [{"name": d.get("name", None)} for d in service_config["dictionaries"]]
    service = Servicev1(service_config["name"], name=service_config["name"], domains=service_config["domains"],
                        dictionaries=dict_names, backends=service_config["backends"], activate=True,
                        force_destroy=True)
    print (service.dictionaries)
    #pulumi.export("Dictionaries", service.dictionaries)
    di = []
    for dictionary in service_config["dictionaries"]:
        print("for loop")
        dictionary_name = dictionary['name']
        print("dictionary name in for loop is " + dictionary_name)

        dictionary_id = pulumi.Output.all(service.id, service.dictionaries, dictionary_name).apply(tmp)


        dumbresource = dumbprovider.DumbProviderrResource(dictionary_name, "lukehoban", "todo", dictionary_id)
        dictionary_items_v1 = ServiceDictionaryItemsv1(dictionary_name, service_id=service.id,
                                     items=dictionary["items"],
                                     dictionary_id=dumbresource.dictionary_id)
        print("di")
        print(dictionary_items_v1.items)
        di.append(dictionary_items_v1)




def tmp(lst):
    return get_dictionary_id(lst[1], lst[2])

def get_dictionary_id(dictionaries, dict_name):
    print("get_dictionary_id")
    print("dict_name is " + dict_name)
    print(dictionaries)
    for i in dictionaries:
        print("in dictionary_id for loop")
        if dict_name == i["name"]:
            print("hit the if")
            print(i)
            print(dict_name)
            return i.get("dictionary_id", "sentinel")
        else:
            print("not it " + i["name"])

if __name__ == "__main__":
    main()
