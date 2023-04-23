from pm4py.objects.ocel.importer.xmlocel import importer
from pm4py.objects.ocel.util import *
import pandas as pd
import extrace_case
import src.algorithms.edit_distance as ged

if __name__ == "__main__":
    ocel = importer.apply("..\..\data\\recruiting.xmlocel")
    # print(related_objects.related_objects_dct_per_type(ocel)["applications"])
    # print(ocel.get_summary())
    # print(pm4py.ocel_get_attribute_names(ocel))
    # print(ocel.events)
    # print(ocel.objects)
    # l1 = ocel.objects['ocel:type'].unique()

    # df = flattening.flatten(ocel, "applications")
    # print(df)
    # df1 = df[df['case:concept:name'] == 'Application[770001]']
    # print()
    # print(df[df['case:concept:name'] == 'Application[770001]']['concept:name'].tolist())
    # print(list(ocel.columns.values)
    case_dict = extrace_case.extract_case_with_leading_type(ocel, "applications",['vacancies'])

    # for k1, v1 in case_dict.items():
    #     for k2, v2 in case_dict.items():
    #         if k1 != k2:
    #             for each_node in v1:
    #                 print(v1.nodes[each_node])
    #             path, best_cost = ged.get_ged(v1, v2)
    #             print("\n", v1.edges)
    #             print(v2.edges)
    #             print(path[0], best_cost)




    # # 对于每个obj类型，获取对应的event数目
    # print(events_per_object_type.apply(ocel))
    #
    # # 每个activity的mean max min median
    # print(events_per_type_per_activity.apply(ocel))


    # 获取每个obj对应的event
    # dict1 = related_events.related_events_dct(ocel)
    # for k,v in dict1.items():
    #     for k1, v1 in v.items():
    #         print(k1, " ", v1)

    #
    # dict2 = related_objects.related_objects_dct_per_type(ocel)
    # for k, v in dict2.items():
    #     if k == "vacancies":
    #         for k1, v1 in v.items():
    #             print(k1,v1)

#
    # dict3 = related_objects.related_objects_dct_overall(ocel)
    # for k, v in dict3.items():
    #     print(k, v)
