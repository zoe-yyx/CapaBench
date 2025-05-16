from itertools import combinations
from math import comb
import json
from ast import literal_eval
from math import factorial


# 给定基础和替代特征的组合情况和它们的贡献值
contributions = {
    ('Pd', 'Rd', 'Ad', 'Fd'): 0.4872,
    ('Pt', 'Rt', 'At', 'Ft'): 0.4850,
    ('Pt', 'Rd', 'Ad', 'Fd'): 0.4710,
    ('Pd', 'Rt', 'Ad', 'Fd'): 0.5136,
    ('Pd', 'Rd', 'At', 'Fd'): 0.4885,
    ('Pd', 'Rd', 'Ad', 'Ft'): 0.4928,
    ('Pt', 'Rt', 'Ad', 'Fd'): 0.4846,
    ('Pt', 'Rd', 'At', 'Fd'): 0.5239,
    ('Pt', 'Rd', 'Ad', 'Ft'): 0.4958,
    ('Pd', 'Rt', 'At', 'Fd'): 0.5274,
    ('Pd', 'Rt', 'Ad', 'Ft'): 0.5163,
    ('Pd', 'Rd', 'At', 'Ft'): 0.4982,
    ('Pd', 'Rt', 'At', 'Ft'): 0.4997,
    ('Pt', 'Rd', 'At', 'Ft'): 0.5403,
    ('Pt', 'Rt', 'Ad', 'Ft'): 0.4919,
    ('Pt', 'Rt', 'At', 'Fd'): 0.5004
}

model_names = ["qwen", "Mistral-8X7B", "Mistral-7B", "gpt4-turbo", "glm", "doubao", "claude", "4o-mini"]
for model_name in model_names:

    with open(f"./dialop/shapley_values_new_{model_name}.json", 'r') as f:
        data = json.load(f)
        for key_str, value in data.items():
            key_tuple = literal_eval(key_str)
            contributions[key_tuple] = value

    # 特征组合
    default_features = ['Pd', 'Rd', 'Ad', 'Fd']
    target_features = ['Pt', 'Rt', 'At', 'Ft']

    # 定义一个函数来按照PRAF顺序对组合进行排序
    def sort_by_praf_order(tup):
        order = {'P': 0, 'R': 1, 'A': 2, 'F': 3}
        return tuple(sorted(tup, key=lambda x: order[x[0]]))


    # 计算单个特征的Shapley值
    def calculate_shapley_values(contributions, default_features, target_features):
        def sort_by_praf_order(tup):
            order = {'P': 0, 'R': 1, 'A': 2, 'F': 3}
            return tuple(sorted(tup, key=lambda x: order[x[0]]))

        def calculate_shapley_value(feature):
            total_shapley_value = 0
            n = len(target_features)

            for subset_size in range(n):
                for subset in combinations([f for f in target_features if f != feature], subset_size):
                    subset = list(subset)
                    replaced_subset_before = [
                        default_features[target_features.index(f)] if f not in subset else f
                        for f in target_features
                    ]

                    replaced_subset_after = [
                        feature if f == feature else (default_features[target_features.index(f)] if f not in subset else f)
                        for f in target_features
                    ]

                    subset_before = sort_by_praf_order(replaced_subset_before)
                    subset_after = sort_by_praf_order(replaced_subset_after)

                    marginal_contribution = contributions.get(subset_after, 0) - contributions.get(subset_before, 0)

                    # Shapley 的权重系数：|S|! * (n - |S| - 1)! / n!
                    weight = (factorial(subset_size) *
                            factorial(n - subset_size - 1) /
                            factorial(n))

                    total_shapley_value += weight * marginal_contribution

            return total_shapley_value

        shapley_values = {feature: calculate_shapley_value(feature) for feature in target_features}
        return shapley_values

    # 计算每一个特征的Shapley值
    # shapley_values_corrected = {feature: calculate_shapley_values(contributions, default_features, target_features) for feature in target_features}
    shapley_values_corrected = calculate_shapley_values(contributions, default_features, target_features)

    # 将contributions中的键转化为str类型
    contributions = {str(key): value for key, value in contributions.items()}
    contributions["shapeley values"] = shapley_values_corrected

    with open(f"./dialop/shapley_values_new_{model_name}.json", 'w') as f:
        json.dump(contributions, f, ensure_ascii=False, indent=4)

    # 输出Shapley值
    print(shapley_values_corrected)






# from itertools import combinations
# from math import comb
# import json
# from ast import literal_eval

# # 给定基础和替代特征的组合情况和它们的贡献值
# contributions = {
#     ('Pd', 'Rd', 'Ad', 'Fd'): 0.4872,
#     ('Pt', 'Rt', 'At', 'Ft'): 0.4850,
#     ('Pt', 'Rd', 'Ad', 'Fd'): 0.4710,
#     ('Pd', 'Rt', 'Ad', 'Fd'): 0.5136,
#     ('Pd', 'Rd', 'At', 'Fd'): 0.4885,
#     ('Pd', 'Rd', 'Ad', 'Ft'): 0.4928,
#     ('Pt', 'Rt', 'Ad', 'Fd'): 0.4846,
#     ('Pt', 'Rd', 'At', 'Fd'): 0.5239,
#     ('Pt', 'Rd', 'Ad', 'Ft'): 0.4958,
#     ('Pd', 'Rt', 'At', 'Fd'): 0.5274,
#     ('Pd', 'Rt', 'Ad', 'Ft'): 0.5163,
#     ('Pd', 'Rd', 'At', 'Ft'): 0.4982,
#     ('Pd', 'Rt', 'At', 'Ft'): 0.4997,
#     ('Pt', 'Rd', 'At', 'Ft'): 0.5403,
#     ('Pt', 'Rt', 'Ad', 'Ft'): 0.4919,
#     ('Pt', 'Rt', 'At', 'Fd'): 0.5004
# }

# model_name = "gpt4-turbo"

# with open(f"/home/hadoop-aipnlp/dolphinfs_hdd_hadoop-aipnlp/huhaoyi02/dialop-mediation/dialop/shapley_values_new_{model_name}.json", 'r') as f:
#     data = json.load(f)
#     for key_str, value in data.items():
#         key_tuple = literal_eval(key_str)
#         contributions[key_tuple] = value

# # 特征组合
# default_features = ['Pd', 'Rd', 'Ad', 'Fd']
# target_features = ['Pt', 'Rt', 'At', 'Ft']

# # 定义一个函数来按照PRAF顺序对组合进行排序
# def sort_by_praf_order(tup):
#     order = {'P': 0, 'R': 1, 'A': 2, 'F': 3}
#     return tuple(sorted(tup, key=lambda x: order[x[0]]))

# # 计算单个特征的Shapley值
# def calculate_shapley_value_corrected_order(feature, default_features, target_features, contributions):
#     total_shapley_value = 0
#     n = len(target_features)

#     for subset_size in range(n):  # 考虑从0到n-1的所有子集
#         for subset in combinations([f for f in target_features if f != feature], subset_size):
#             subset = list(subset)
#             # 用默认特征替换目标特征
#             replaced_subset_before = [
#                 default_features[target_features.index(f)] if f not in subset else f
#                 for f in target_features
#             ]
#             replaced_subset_after = [
#                 feature if f == feature else (default_features[target_features.index(f)] if f not in subset else f)
#                 for f in target_features
#             ]

#             # 对组合进行排序以确保顺序一致
#             subset_before = sort_by_praf_order(replaced_subset_before)
#             subset_after = sort_by_praf_order(replaced_subset_after)
#             # print("subset_before", subset_before, contributions.get(subset_before, 0), "subset_after", subset_after, contributions.get(subset_after, 0))
#             # 计算边际贡献
#             marginal_contribution = contributions.get(subset_after, 0) - contributions.get(subset_before, 0)

#             # 根据组合的数量更新边际贡献
#             # weight = comb(n-1, subset_size) / (2 ** (n-1))
#             weight = 1 / (2 ** (n-1))
#             # print("weight", weight)
#             total_shapley_value += weight * marginal_contribution

#     # Shapley值是总贡献的平均值
#     return total_shapley_value

# # 计算每一个特征的Shapley值
# shapley_values_corrected = {feature: calculate_shapley_value_corrected_order(feature, default_features, target_features, contributions) for feature in target_features}

# # 将shapley value存入json文件
# data["shapley value"] = shapley_values_corrected
# with open(f"/home/hadoop-aipnlp/dolphinfs_hdd_hadoop-aipnlp/huhaoyi02/dialop-mediation/dialop/shapley_values_new_{model_name}.json", 'w') as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)

# # 输出Shapley值
# print(shapley_values_corrected)
