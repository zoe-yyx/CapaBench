theory DistExistsAnd
  imports Main
begin

theorem dist_exists_and:
  assumes "\<exists>x. P x \<and> Q x"
  shows "(\<exists>x. P x) \<and> (\<exists>x. Q x)"
proof -
  obtain x where x_def: "P x \<and> Q x" using assms by blast
  then have "P x" and "Q x" by blast+
  then show ?thesis using \<open>P x\<close> \<open>Q x\<close> by blast
end
