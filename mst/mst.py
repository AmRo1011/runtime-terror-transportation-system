# mst/optimizer.py

from shared.data_loader import load_data

def compute_hybrid_mst(
    apply_priority=True,
    population_factor=0.8,
    facility_factor=0.7,
    limit_budget=False,
    max_budget=999999
):
    # تحميل البيانات
    potential = load_data("new_roads")
    neighborhoods = load_data("neighborhoods")
    facilities = load_data("facilities")
    existing = load_data("roads")

    # تحويل IDs إلى str
    neighborhoods["id"] = neighborhoods["id"].astype(str)
    facilities["id"] = facilities["id"].astype(str)
    potential["fromid"] = potential["fromid"].astype(str)
    potential["toid"] = potential["toid"].astype(str)
    existing["from_id"] = existing["from_id"].astype(str)
    existing["to_id"] = existing["to_id"].astype(str)

    # تحضير population map و IDs المرافق
    population_map = dict(zip(neighborhoods["id"], neighborhoods["population"]))
    facility_ids = set(facilities["id"])

    # تحضير الطرق الجديدة
    potential_edges = []
    for _, row in potential.iterrows():
        u = row["fromid"]
        v = row["toid"]
        base_cost = row["construction_costmillion_egp"]

        pop_u = population_map.get(u, 0)
        pop_v = population_map.get(v, 0)
        high_pop = (pop_u > 200000) or (pop_v > 200000)
        connects_facility = (u in facility_ids) or (v in facility_ids)

        factor = 1.0
        if apply_priority:
            if connects_facility:
                factor *= facility_factor
            if high_pop:
                factor *= population_factor

        adjusted_cost = base_cost * factor
        potential_edges.append((adjusted_cost, u, v, True))

    # Disjoint Set
    class DisjointSet:
        def __init__(self, nodes):
            self.parent = {node: node for node in nodes}

        def find(self, node):
            if self.parent[node] != node:
                self.parent[node] = self.find(self.parent[node])
            return self.parent[node]

        def union(self, u, v):
            root_u = self.find(u)
            root_v = self.find(v)
            if root_u != root_v:
                self.parent[root_v] = root_u
                return True
            return False

    # تجميع كل النودز
    all_nodes = set()
    for _, u, v, _ in potential_edges:
        all_nodes.add(u)
        all_nodes.add(v)
    for _, row in existing.iterrows():
        all_nodes.add(row["from_id"])
        all_nodes.add(row["to_id"])

    # تنفيذ MST على الطرق الجديدة
    disjoint = DisjointSet(all_nodes)
    mst = []
    total_cost = 0
    sorted_edges = sorted(potential_edges, key=lambda x: x[0])

    for cost, u, v, is_new in sorted_edges:
        if disjoint.union(u, v):
            if limit_budget and (total_cost + cost > max_budget):
                break
            mst.append((cost, u, v, is_new))
            total_cost += cost

    # إعادة فحص الاتصال الكامل
    disjoint = DisjointSet(all_nodes)
    for cost, u, v, _ in mst:
        disjoint.union(u, v)

    # إضافة الطرق القديمة لتوصيل المتبقي
    extra_edges = []
    for _, row in existing.iterrows():
        u = row["from_id"]
        v = row["to_id"]
        if disjoint.union(u, v):
            extra_edges.append((1.0, u, v, False))

    final_mst = mst + extra_edges
    return final_mst, total_cost, len(extra_edges)
