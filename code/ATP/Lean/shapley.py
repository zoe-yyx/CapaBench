

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


    ## claude-3.5-sonnet
    contributions = {
        ('Pd', 'Rd', 'Ad', 'Fd'): 0,
        ('Pt', 'Rt', 'At', 'Ft'): 0.5495495495495496,
        ('Pt', 'Rd', 'Ad', 'Fd'): 0.009009009009009009,
        ('Pd', 'Rt', 'Ad', 'Fd'): 0.04504504504504504,
        ('Pd', 'Rd', 'At', 'Fd'): 0.3063063063063063,
        ('Pd', 'Rd', 'Ad', 'Ft'): 0.07207207207207207,
        ('Pt', 'Rt', 'Ad', 'Fd'): ...,
        ('Pt', 'Rd', 'At', 'Fd'): 0.38738738738738737,
        ('Pt', 'Rd', 'Ad', 'Ft'): 0.07207207207207207,
        ('Pd', 'Rt', 'At', 'Fd'): 0.3153153153153153,
        ('Pd', 'Rt', 'Ad', 'Ft'): 0.13513513513513514,
        ('Pd', 'Rd', 'At', 'Ft'): 0.5585585585585585,
        ('Pd', 'Rt', 'At', 'Ft'): 0.5495495495495496,
        ('Pt', 'Rd', 'At', 'Ft'): 0.6036036036036037,
        ('Pt', 'Rt', 'Ad', 'Ft'): 0.18018018018018017,
        ('Pt', 'Rt', 'At', 'Fd'): 0.36036036036036034,
    }


    # ## gpt-4o-mini
    contributions = {
        ('Pd', 'Rd', 'Ad', 'Fd'): 0,
        ('Pt', 'Rt', 'At', 'Ft'): ...,
        ('Pt', 'Rd', 'Ad', 'Fd'): ...,
        ('Pd', 'Rt', 'Ad', 'Fd'): ...,
        ('Pd', 'Rd', 'At', 'Fd'): ...,
        ('Pd', 'Rd', 'Ad', 'Ft'): ...,
        ('Pt', 'Rt', 'Ad', 'Fd'): ...,
        ('Pt', 'Rd', 'At', 'Fd'): ...,
        ('Pt', 'Rd', 'Ad', 'Ft'): ...,
        ('Pd', 'Rt', 'At', 'Fd'): ...,
        ('Pd', 'Rt', 'Ad', 'Ft'): ...,
        ('Pd', 'Rd', 'At', 'Ft'): ...,
        ('Pd', 'Rt', 'At', 'Ft'): ...,
        ('Pt', 'Rd', 'At', 'Ft'): ...,
        ('Pt', 'Rt', 'Ad', 'Ft'): ...,
        ('Pt', 'Rt', 'At', 'Fd'): ...
    }

    ## llama3-70b-instruct
    contributions = {
        ('Pd', 'Rd', 'Ad', 'Fd'): 0,
        ('Pt', 'Rt', 'At', 'Ft'): ...,
        ('Pt', 'Rd', 'Ad', 'Fd'): ...,
        ('Pd', 'Rt', 'Ad', 'Fd'): ...,
        ('Pd', 'Rd', 'At', 'Fd'): ...,
        ('Pd', 'Rd', 'Ad', 'Ft'): ...,
        ('Pt', 'Rt', 'Ad', 'Fd'): ...,
        ('Pt', 'Rd', 'At', 'Fd'): ...,
        ('Pt', 'Rd', 'Ad', 'Ft'): ...,
        ('Pd', 'Rt', 'At', 'Fd'): ...,
        ('Pd', 'Rt', 'Ad', 'Ft'): ...,
        ('Pd', 'Rd', 'At', 'Ft'): ...,
        ('Pd', 'Rt', 'At', 'Ft'): ...,
        ('Pt', 'Rd', 'At', 'Ft'): ...,
        ('Pt', 'Rt', 'Ad', 'Ft'): ...,
        ('Pt', 'Rt', 'At', 'Fd'): ...
    }

    # 特征组合
    default_features = ['Pd', 'Rd', 'Ad', 'Fd']
    target_features = ['Pt', 'Rt', 'At', 'Ft']
    print(calculate_shapley_values(contributions, default_features, target_features))
