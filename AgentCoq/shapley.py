

## 计算函数
from itertools import combinations
from math import comb

def calculate_shapley_values(contributions, default_features, target_features):
    # 定义一个函数来按照PRAF顺序对组合进行排序
    def sort_by_praf_order(tup):
        order = {'P': 0, 'R': 1, 'A': 2, 'F': 3}
        return tuple(sorted(tup, key=lambda x: order[x[0]]))

    # 计算单个特征的Shapley值
    def calculate_shapley_value(feature):
        total_shapley_value = 0
        n = len(target_features)

        for subset_size in range(n):  # 考虑从0到n-1的所有子集
            for subset in combinations([f for f in target_features if f != feature], subset_size):
                subset = list(subset)

                # 用默认特征替换目标特征
                replaced_subset_before = [
                    default_features[target_features.index(f)] if f not in subset else f
                    for f in target_features
                ]
                replaced_subset_after = [
                    feature if f == feature else (default_features[target_features.index(f)] if f not in subset else f)
                    for f in target_features
                ]

                # 对组合进行排序以确保顺序一致
                subset_before = sort_by_praf_order(replaced_subset_before)
                subset_after = sort_by_praf_order(replaced_subset_after)

                # 计算边际贡献
                marginal_contribution = contributions.get(subset_after, 0) - contributions.get(subset_before, 0)

                # 根据组合的数量更新边际贡献
                weight = 1 / (2 ** (n-1))
                total_shapley_value += weight * marginal_contribution

        # Shapley值是总贡献的平均值
        return total_shapley_value

    # 计算每一个特征的Shapley值
    shapley_values = {feature: calculate_shapley_value(feature) for feature in target_features}

    return shapley_values

if __name__ == '__main__':
    # 函数输入
    # 给定基础和替代特征的组合情况和它们的贡献值
    # contributions = {
    #     ('Pd', 'Rd', 'Ad', 'Fd'): 0.3144,
    #     ('Pt', 'Rt', 'At', 'Ft'): 0.4054,
    #     ('Pt', 'Rd', 'Ad', 'Fd'): 0.4083,
    #     ('Pd', 'Rt', 'Ad', 'Fd'): 0.4254,
    #     ('Pd', 'Rd', 'At', 'Fd'): 0.3560,
    #     ('Pd', 'Rd', 'Ad', 'Ft'): 0.3347,
    #     ('Pt', 'Rt', 'Ad', 'Fd'): 0.3728,
    #     ('Pt', 'Rd', 'At', 'Fd'): 0.4535,
    #     ('Pt', 'Rd', 'Ad', 'Ft'): 0.4382,
    #     ('Pd', 'Rt', 'At', 'Fd'): 0.3815,
    #     ('Pd', 'Rt', 'Ad', 'Ft'): 0.4018,
    #     ('Pd', 'Rd', 'At', 'Ft'): 0.4523,
    #     ('Pd', 'Rt', 'At', 'Ft'): 0.4618,
    #     ('Pt', 'Rd', 'At', 'Ft'): 0.3408,
    #     ('Pt', 'Rt', 'Ad', 'Ft'): 0.4874,
    #     ('Pt', 'Rt', 'At', 'Fd'): 0.5045
    # }
    contributions = {
        ('Pd', 'Rd', 'Ad', 'Fd'): 0.0431,
        ('Pt', 'Rt', 'At', 'Ft'): 0.8879,
        ('Pt', 'Rd', 'Ad', 'Fd'): 0.0327,
        ('Pd', 'Rt', 'Ad', 'Fd'): 0.0948,
        ('Pd', 'Rd', 'At', 'Fd'): 0.8448,
        ('Pd', 'Rd', 'Ad', 'Ft'): 0.0377,
        ('Pt', 'Rt', 'Ad', 'Fd'): 0.0654,
        ('Pt', 'Rd', 'At', 'Fd'): 0.4535,
        ('Pt', 'Rd', 'Ad', 'Ft'): 0.0948,
        ('Pd', 'Rt', 'At', 'Fd'): 0.8620,
        ('Pd', 'Rt', 'Ad', 'Ft'): 0.2131,
        ('Pd', 'Rd', 'At', 'Ft'): 0.8448,
        ('Pd', 'Rt', 'At', 'Ft'): 0.8879,
        ('Pt', 'Rd', 'At', 'Ft'): 0.9051,
        ('Pt', 'Rt', 'Ad', 'Ft'): 0.1206,
        ('Pt', 'Rt', 'At', 'Fd'): 0.9224
    }
    # 特征组合
    default_features = ['Pd', 'Rd', 'Ad', 'Fd']
    target_features = ['Pt', 'Rt', 'At', 'Ft']
    print(calculate_shapley_values(contributions, default_features, target_features))
