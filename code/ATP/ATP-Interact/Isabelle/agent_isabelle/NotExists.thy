theory NotExists
  imports Main
begin

theorem not_exists: "(\<not> (\<exists>x. P x)) \<Longrightarrow> (\<forall>x. \<not> P x)"
proof
  assume H: "\<not> (\<exists>x. P x)"
  fix x
  show "\<not> P x"
  proof
    assume "P x"
    hence "\<exists>x. P x" by auto
    thus False using H by auto
  qed
qed

end
