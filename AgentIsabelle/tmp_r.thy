
proof
fix a
show "mono (\<lambda>x. a)"
proof (unfold mono_def)
  show "\<forall>n m. n \<le> m \<longrightarrow> (\<lambda>x. a) n \<le> (\<lambda>x. a) m"
  proof
    fix n m
    assume "n \<le> m"
    then show "(\<lambda>x. a) n \<le> (\<lambda>x. a) m"
      by simp
  qed
qed
