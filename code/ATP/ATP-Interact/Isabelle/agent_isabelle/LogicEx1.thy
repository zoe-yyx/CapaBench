theory LogicEx1
  imports Main
begin

definition convex :: "(int \<Rightarrow> int) \<Rightarrow> bool" where
  "convex f \<longleftrightarrow> (\<forall> x. f (x - 1) + f (x + 1) \<ge> 2 * f x)"

definition mono :: "(int \<Rightarrow> int) \<Rightarrow> bool" where
  "mono f \<longleftrightarrow> (\<forall> n m. n \<le> m \<longrightarrow> f n \<le> f m)"

theorem logic_ex1:
  assumes "\<forall> f. mono f \<longrightarrow> mono (T f)"
    and "\<forall> f. convex f \<longrightarrow> convex (T f)"
    and "mono f \<and> convex f"
  shows "mono (T f) \<and> convex (T f)"
proof -
  from assms(1) have "mono f \<longrightarrow> mono (T f)" by auto
  from assms(2) have "convex f \<longrightarrow> convex (T f)" by auto
  from assms(3) have "mono f" and "convex f" by auto
  thus "mono (T f) \<and> convex (T f)" using assms by auto
qed

end
