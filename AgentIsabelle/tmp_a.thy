theory NotExists
  imports Main
begin

theorem not_exists: "(\<not> (\<exists>x. P x)) \<Longrightarrow> (\<forall>x. \<not> P x)"
  by auto

end
